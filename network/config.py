import warnings


class DefaultConfig(object):
    env = 'default'
    model = 'IdentNet'

    raw_data_root = './data/raw'
    train_data_root = './data/train'
    test_data_root = './data/test'
<<<<<<< HEAD
    load_model_path = '/home/ljw/PycharmProjects/lsc/network/checkpoints/IdentNet_0522_21_59_26.pth'
=======
    load_model_path = 'C:/Users/omnitrix/PycharmProjects/IC_Secu/network/checkpoints/IdentNet_0522_21_59_26.pth'
>>>>>>> c6aecf92fcadd19d9fa78c7d01491ae148a31389

    batch_size = 32
    use_gpu = False
    num_workers = 5
    print_freq = 10

    result_file = './checkpoints/result.csv'

    max_epoch = 10
    lr = 0.2
    lr_decay = 0.85
    weight_decay = 1e-4

    cates = 5
    classes_dict = {"ssl": 0, "ssh": 1, "http": 2, "dns": 3, "ftp": 4}
    threshold = 7


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
