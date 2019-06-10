import warnings
import os

root_path = os.path.dirname(__file__)


class DefaultConfig(object):
    env = 'default'
    model = 'IdentNet'

    raw_data_root = './data/raw'
    train_data_root = './data/train'
    test_data_root = './data/test'
    load_model_path = ""

    batch_size = 32
    use_gpu = False
    num_workers = 5
    print_freq = 10

    model_file = root_path + '/checkpoints/'

    max_epoch = 10
    lr = 0.2
    lr_decay = 0.85
    weight_decay = 1e-4

    classes_dict = {"ssl": 0, "ssh": 1, "http": 2, "dns": 3, "ftp": 4, "mysql": 5}
    app_dict = {"QQ": 0, "WeChat": 1, "iqy": 2, "Thunder": 3, "NetEase": 4}
    cates = len(classes_dict)
    net1_threshold = 7
    net2_threshold = 9

    if_print = True
    capture_num = 100

    net1_model = model_file + "IdentNet_0604_16_03_24.pth"
    net2_model = model_file + "EncIdentNet_0608_19_08_10.pth"

    def parse(self, kwargs):
        for k, v in kwargs.items():
            if not hasattr(self, k):
                warnings.warn('warning:DefualtConfig has no attribut %s' % k)
            setattr(self, k, v)
        if self.model != "IdentNet":
            self.cates = len(self.app_dict)
        self.print_opt()
        # print('user config:')

    def print_opt(self):
        for k, v in self.__class__.__dict__.items():
            if not k.startswith('__') and self.if_print:
                print(k, getattr(self, k))


opt = DefaultConfig()
