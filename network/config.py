import warnings


class DefaultConfig(object):
    env = 'default'
    model = 'AlexNet'

    raw_data_root = './data/raw'
    train_data_root = '.\data\\train'
    test_data_root = '.\data\\test'
    load_model_path = ''  # './checkpoints/model.pth'

    batch_size = 128
    use_gpu = False
    num_workers = 5
    print_freq = 10

    debug_file = '\\tmp\debug'
    result_file = '.\checkpoints\\result.csv'

    max_epoch = 10
    lr = 0.1
    lr_decay = 0.85
    weight_decay = 1e-4

    cates = 5

def parse(self, kwargs):
    for k, v in kwargs.items():
        if not hasattr(self, k):
            warnings.warn('warning:DefualtConfig has no attribut %s' % k)
        setattr(self, k, v)

    print('user config:')
    for k, v in self.__class__.__dict__.items():
        if not k.startswith('__'):
            print(k, getattr(self, k))


DefaultConfig.parse = parse
opt = DefaultConfig()
# opt.parse=parse
