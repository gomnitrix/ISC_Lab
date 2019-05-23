import fire
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from torchnet import meter

import models
from config import opt
from data import DataFlow, TrainDataFlow
from utils import Visualizer


def test(**kwargs):
    opt.parse(kwargs)

    # data
    test_data = TrainDataFlow()
    test_loader = DataLoader(
        test_data,
        batch_size=opt.batch_size,
        shuffle=False,
        # num_workers=opt.num_workers
    )
    results = []

    # model
    model = getattr(models, opt.model)()
    if opt.load_model_path:
        model.load(opt.load_model_path)
    if opt.use_gpu:
        model = model.cuda()

    for ii, (data, path) in enumerate(test_loader):
        input_data = torch.tensor(data)
        if opt.use_gpu:
            input_data = input_data.cuda()
        pred = model(input_data)
        label = pred.max(dim=1)[1].data.tolist()
        results.append(label)
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

        for ii, (x, y) in enumerate(train_loader):
            data = torch.tensor(x)
            label = torch.tensor(y)
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
        if loss_meter.value()[0] > previous_loss:
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
        input_data, label = data
        with torch.no_grad():
            val_input = torch.tensor(input_data)
            val_label = torch.tensor(label.long())
        if opt.use_gpu:
            val_input = val_input.cuda()
            val_label = val_label.cuda()
        out = model(val_input)
        confusion_matrix.add(out.data.squeeze(), label.long())

    model.train()
    cm_value = confusion_matrix.value()
    num = sum([cm_value[x][x] for x in range(opt.cates)])
    accuracy = 100 * num / (cm_value.sum())

    return confusion_matrix, accuracy


def write_csv(results, file):
    import csv
    with open(file, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['id', 'label'])
        writer.writerows(results)
        f.close()


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
    # train(lr=0.3, batch_size=64, max_epoch=15,load_model_path='.\checkpoints\\IdentNet_0522_15_34_03.pth')
