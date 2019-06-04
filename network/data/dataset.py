import time

import numpy as np
from torch.utils import data

from catch_package.catch_packet import Queue
from config import opt
from utils import DBHelper as Db


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

        self.label_map = opt.classes_dict

    def __getitem__(self, index):
        file = self.files[index]
        label = self.label_map[file.split('_')[0]]
        file = self.db_helper.read_data(file, self.conn)
        return file, label

    def __len__(self):
        return len(self.files)


class TestDataFlow(data.Dataset):
    def __init__(self):
        self.queue = Queue

    def __getitem__(self, index):
        if self.queue.empty():
            print("empty!!")
            time.sleep(3)
        return self.queue.get(), "test"

    def __len__(self):
        return self.queue.qsize()
