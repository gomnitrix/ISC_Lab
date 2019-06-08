import time

import numpy as np
from torch.utils import data

from identify.global_queue import net1_pretation
from catch_package.catch_pkt import raw_data_queue
from network.config import opt
from network.utils import DBHelper as Db


class DataFlow(data.Dataset):
    def __init__(self, train=True):
        self.db_helper = Db()
        self.conn = self.db_helper.get_con(False)
        files = self.db_helper.get_files(self.conn)
        files = [x[0] for x in files]
        files = sorted(files, key=lambda x: int(x.split('_')[-1]))

        files_num = len(files)

        # shuffle
        np.random.seed(100)
        np.random.shuffle(files)

        if train:
            self.files = files[:int(0.9 * files_num)]
        else:
            self.files = files[int(0.9 * files_num):]

        self.label_map = opt.classes_dict if opt.model == "IdentNet" else opt.app_dict

    def __getitem__(self, index):
        file = self.files[index]
        # label = self.label_map[file.split('_')[0]]
        data, label = self.db_helper.read_data(file, self.conn)
        label = self.label_map[label]
        return data, label

    def __len__(self):
        return len(self.files)


class TestDataFlow(data.Dataset):
    def __init__(self):
        self.queue = raw_data_queue

    def __getitem__(self, index):
        if self.queue.empty():
            print("empty!!")
            time.sleep(3)
        return self.queue.get(), "test"

    def __len__(self):
        return self.queue.qsize()


class EncTestDataFlow(data.Dataset):
    def __init__(self):
        self.queue = net1_pretation

    def __getitem__(self, index):
        if self.queue.empty():
            print("empty!!")
            time.sleep(3)
        item = self.queue.get()
        return item[0], item[1]+'_'+item[2]

    def __len__(self):
        return self.queue.qsize()
