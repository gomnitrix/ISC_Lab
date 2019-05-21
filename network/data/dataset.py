import os

import numpy as np
import torch
# from scapy.all import *
from scapy.utils import PcapReader
from torch.utils import data


def pretreatment():
    # classes = [os.path.join(opt.raw_data_root, file) for file in os.listdir(opt.raw_data_root)]
    # for cls in classes:
    cls = "./raw/icmp.pcapng"
    with PcapReader(cls) as reader:
        idx = 1
        for item in reader:
            load = bytes(item['IPv6'])[:1024]
            length = len(load)
            temp = []
            for i in range(length):
                temp.append(load[i])
            length = len(temp)
            temp.extend([0] * (1024 - length))
            formed_array = (np.array(temp, dtype='f')).reshape((1, 32, 32))
            amin, amax = formed_array.min(), formed_array.max()
            formed_array = (formed_array - amin) / (amax - amin)
            filename = cls.split("/")[-1].split(".")[0] + "_" + str(idx)
            path = "./train/" + filename
            np.save(path, formed_array)
            idx += 1


class DataFlow(data.Dataset):
    def __init__(self, root, train=True, test=False):
        self.test = test
        files = [os.path.join(root, img) for img in os.listdir(root)]

        files = sorted(files, key=lambda x: int((x.split('\\')[-1]).split('.')[-2].split('_')[-1]))

        files_num = len(files)

        # shuffle
        np.random.seed(100)
        files = np.random.permutation(files)

        if self.test:
            self.files = files
        elif train:
            self.files = files[:int(0.9 * files_num)]
        else:
            self.files = files[int(0.9 * files_num):]

        self.label_map = {"ssl": 0, "ssh": 1, "smtp": 2, "http": 3, "gvsp": 4, "ftp": 5, "dns": 6, "skype": 7,
                          "wow": 8, "pop3": 9}
        # # Image preprocessing
        # normalize = T.Normalize(mean=[0.485, 0.456, 0.406],
        #                         std=[0.229, 0.224, 0.225])
        # self.transfrom = T.Compose([
        #     normalize
        # ])

    def __getitem__(self, index):
        file = self.files[index]
        label = self.label_map[(file.split('\\')[-1]).split('_')[0]]
        file = np.load(file)
        return file, label

    def __len__(self):
        return len(self.files)


if __name__ == '__main__':
    pretreatment()
