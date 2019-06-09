import fire
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from torchnet import meter

from network import models
from network.config import opt
from network.data import DataFlow, TestDataFlow, EncTestDataFlow
from network.utils import Visualizer


def test(uq_opt=opt, **kwargs):
    uq_opt.parse(kwargs)
    uq_opt.if_print = False
    flag = (uq_opt.model == "IdentNet")
    threshold = uq_opt.net1_threshold if flag else uq_opt.net2_threshold

    # model
    model = getattr(models, uq_opt.model)()
    if uq_opt.load_model_path:
        model.load(uq_opt.load_model_path)
    if uq_opt.use_gpu:
        model = model.cuda()

    # data
    test_data = TestDataFlow() if flag else EncTestDataFlow()
    test_loader = DataLoader(
        test_data,
        batch_size=uq_opt.batch_size,
        shuffle=False
    )
    results = []

    for ii, (input_data, path) in enumerate(test_loader):
        if uq_opt.use_gpu:
            input_data = input_data.cuda()
        pred = model(input_data)
        max_pre = pred.max(dim=1)
        probability = max_pre[0]
        label = max_pre[1].data.tolist()
        for i in range(len(probability)):
            if probability[i] < threshold:
                label[i] = uq_opt.cates
        results.extend(label)
    return results


def train(**kwargs):
    opt.parse(kwargs)
    vis = Visualizer(opt.env)

    # model
    model = getattr(models, opt.model)()
    if opt.load_model_path:
        model.load(opt.load_model_path)
    if opt.use_gpu:
        model.cuda()

    # data
    train_data = DataFlow(train=True)
    val_data = DataFlow(train=False)
    train_loader = DataLoader(
        train_data,
        opt.batch_size,
        shuffle=True,
        # num_workers=opt.num_workers
    )
    val_loader = DataLoader(
        val_data,
        opt.batch_size,
        shuffle=False,
        # num_workers=opt.num_workers
    )
    criterion = nn.CrossEntropyLoss()
    lr = opt.lr
    optimizer = torch.optim.SGD(model.parameters(),
                                lr,
                                weight_decay=opt.weight_decay)

    # step4
    loss_meter = meter.AverageValueMeter()
    confusion_matrix = meter.ConfusionMeter(opt.cates)
    previous_loss = 1e5

    # training
    for epoch in range(opt.max_epoch):
        loss_meter.reset()
        confusion_matrix.reset()

        for ii, (data, label) in enumerate(train_loader):
            if opt.use_gpu:
                data = data.cuda()
                label = label.cuda()
            out = model.forward(data)
            loss = criterion(out, label.long())

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            loss_meter.add(loss.item())
            confusion_matrix.add(out.data, label.detach())

            if ii % opt.print_freq == 0:
                vis.plot('loss', loss_meter.value()[0])

        model.save()
        val_cm, val_accuracy = val(model, val_loader)

        vis.plot('val_accuracy', val_accuracy)
        vis.log(
            'epoch:{epoch},lr:{lr},loss:{loss},train_cm:{train_cm},val_cm:{val_cm}'
                .format(epoch=epoch,
                        loss=loss_meter.value()[0],
                        val_cm=str(val_cm.value()),
                        train_cm=str(confusion_matrix.value()),
                        lr=lr))
        if loss_meter.value()[0] > previous_loss * 0.95:
            lr = lr * opt.lr_decay
            for param_group in optimizer.param_groups:
                param_group['lr'] = lr

        previous_loss = loss_meter.value()[0]
    train_data.conn.close()
    val_data.conn.close()


def val(model, dataloader):
    model.eval()
    confusion_matrix = meter.ConfusionMeter(opt.cates)
    for ii, data in enumerate(dataloader):
        with torch.no_grad():
            val_input, val_label = data
        if opt.use_gpu:
            val_input = val_input.cuda()
            val_label = val_label.cuda()
        out = model(val_input)
        confusion_matrix.add(out.data.squeeze(), val_label.long())

    model.train()
    cm_value = confusion_matrix.value()
    num = sum([cm_value[x][x] for x in range(opt.cates)])
    accuracy = 100 * num / (cm_value.sum())

    return confusion_matrix, accuracy


def myhelp():
    print('''
        usage : python file.py <function> [--args=value]
        <function> := train | test | help
        example: 
                python {0} train --env='env0701' --lr=0.01
                python {0} test --dataset='path/to/dataset/root/'
                python {0} help
        avaiable args:'''.format(__file__))
    from inspect import getsource
    source = (getsource(opt.__class__))
    print(source)
    return


if __name__ == '__main__':
    fire.Fire()
    # train(lr=0.05, batch_size=64, max_epoch=15,
    #       print_freq=10, model="IdentNet", load_model_path=opt.net1_model)
