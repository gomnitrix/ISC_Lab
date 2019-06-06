from torch import nn

from network.config import opt
from .BasicModel import BasicModel


class IdentNet(BasicModel):
    def __init__(self, num_classes=opt.cates):
        super(IdentNet, self).__init__()
        self.model_name = 'IdentNet'
        self.features = nn.Sequential(
            nn.Conv2d(1, 32, kernel_size=3, stride=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(32, 64, kernel_size=3, stride=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2),
            nn.Dropout(0.25),
        )
        self.classifier = nn.Sequential(
            nn.Linear(12544, 128),
            nn.ReLU(inplace=True),
            nn.Dropout(),
            nn.Linear(128, num_classes),
            nn.ReLU(inplace=True),
        )

    def forward(self, x):
        x = self.features(x)
        x = x.view(x.size(0), 12544)
        x = self.classifier(x)
        # x = softmax(x, dim=1)
        return x
