import time

import torch
from torch import nn
from config import root_path


class BasicModel(nn.Module):
    def __init__(self):
        super(BasicModel, self).__init__()
        self.model_name = str(type(self))

    def load(self, path):
        self.load_state_dict(torch.load(path))

    def save(self, name=None):
        prefix = root_path + "\checkpoints\\"

        if not name:
            prefix = prefix + self.model_name + '_'
        else:
            prefix = prefix + name + '_'
        name = time.strftime(prefix + '%m%d_%H_%M_%S.pth')
        torch.save(self.state_dict(), name)
        return name
