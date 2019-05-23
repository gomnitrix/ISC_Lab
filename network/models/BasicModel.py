import time

import torch
from torch import nn


class BasicModel(nn.Module):
    def __init__(self):
        super(BasicModel, self).__init__()
        self.model_name = str(type(self))

    def load(self, path):
        if path and self.model_name.startswith('AlexNet'):
            pretrain_dict = torch.load(path)
            alex_dict = self.state_dict()
            pretrain_dict = {k: v for k, v in pretrain_dict.items() if k in alex_dict}
            alex_dict.update(pretrain_dict)
            self.load_state_dict(alex_dict)
            return
        self.load_state_dict(torch.load(path))

    def save(self, name=None):
        prefix = 'C:/Users/omnitrix/PycharmProjects/IC_Secu/network/checkpoints/'
        if not name:
            prefix = prefix + self.model_name + '_'
        else:
            prefix = prefix + name + '_'
        name = time.strftime(prefix + '%m%d_%H_%M_%S.pth')
        torch.save(self.state_dict(), name)
        return name
