import os

import numpy as np
import torch
from scapy.all import *
from config import opt
from scapy.utils import PcapReader
from torch.utils import data
from utils import DBHelper as db


def pretreatment():
    classes = [os.path.join("./raw/", file) for file in os.listdir("./raw/")]
    helper = db()
    conn = helper.get_con()
    for cls in classes:
        with PcapReader(cls) as reader:
            idx = 1
            file_prefix = cls.split("/")[-1].split(".")[0] + "_"
            for item in reader:
                if 'TCP' in item:
                    load = item['TCP']
                elif 'UDP' in item:
                    load = item['UDP']
                else:
                    load = item['IPv6']
                load = bytes(load)[:1024]
                length = len(load)
                temp = []
                for i in range(length):
                    temp.append(load[i])
                length = len(temp)
                temp.extend([0] * (1024 - length))
                formed_array = (np.array(temp, dtype='f')).reshape((1, 32, 32))
                amin, amax = formed_array.min(), formed_array.max()
                formed_array = (formed_array - amin) / (amax - amin)
                name = file_prefix + str(idx)
                helper.write_data(name, formed_array.tostring(), conn)
                idx += 1
                if idx >= 7000:
                    break


class DataFlow(data.Dataset):
    def __init__(self, root, train=True, test=False):
        self.test = test
        self.db_helper = db()
        self.conn = self.db_helper.get_con(False)
        files = self.db_helper.get_files(self.conn)
        files = [x[0] for x in files]
        files = sorted(files, key=lambda x: int(x.split('_')[-1]))

        files_num = len(files)

        # shuffle
        np.random.seed(100)
        np.random.shuffle(files)

        if self.test:
            self.files = files
        elif train:
            self.files = files[:int(0.9 * files_num)]
        else:
            self.files = files[int(0.9 * files_num):]

        self.label_map = {"ssl": 0, "ssh": 1, "http": 2, "dns": 3, "skype": 4}
        # {"ssl": 0, "ssh": 1, "smtp": 2, "http": 3, "gvsp": 4, "ftp": 5, "dns": 6, "skype": 7,"wow": 8, "pop3": 9}

    def __getitem__(self, index):
        file = self.files[index]
        label = self.label_map[file.split('_')[0]]
        file = self.db_helper.read_data(file, self.conn)
        return file, label

    def __len__(self):
        return len(self.files)


if __name__ == '__main__':
    # pretreatment()
    h = db()
    conn = h.get_con(False)
    files = h.get_files(conn)
    print(len(files))
    data = h.read_data(files[0][0], conn)
    print(data)
    print(data.shape)
