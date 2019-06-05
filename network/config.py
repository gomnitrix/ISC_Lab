import warnings
import os

root_path = os.path.dirname(__file__)


class DefaultConfig(object):
    env = 'default'
    model = 'IdentNet'

    raw_data_root = './data/raw'
    train_data_root = './data/train'
    test_data_root = './data/test'
    load_model_path = root_path + '/checkpoints/IdentNet_0603_11_04_37.pth'

    batch_size = 32
    use_gpu = False
    num_workers = 5
    print_freq = 10

    result_file = './checkpoints/result.csv'

    max_epoch = 10
    lr = 0.2
    lr_decay = 0.85
    weight_decay = 1e-4

    classes_dict = {"ssl": 0, "ssh": 1, "http": 2, "dns": 3, "ftp": 4, "mysql": 5}
    cates = len(classes_dict)
    threshold = 7

    if_print = True
    capture_num = 100

    def parse(self, kwargs):
        for k, v in kwargs.items():
            if not hasattr(self, k):
                warnings.warn('warning:DefualtConfig has no attribut %s' % k)
            setattr(self, k, v)

        print('user config:')
        for k, v in self.__class__.__dict__.items():
            if not k.startswith('__') and self.if_print:
                print(k, getattr(self, k))


opt = DefaultConfig()
