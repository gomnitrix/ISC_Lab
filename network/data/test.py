from PIL import Image
import os
from torch.utils import data
from torchvision import transforms as T
import numpy as np


class DogCat(data.Dataset):
    def __init__(self, root, transform=None, train=True, test=False):
        self.test = test
        imgs = [os.path.join(root, img) for img in os.listdir(root)]

        # test1: data\\test1\\8973.jpg
        # train: data\\train\\cat.10004.jpg
        if test:
            imgs = sorted(imgs, key=lambda x: int((x.split('\\')[-1]).split('.')[-2]))
        else:
            imgs = sorted(imgs, key=lambda x: int(x.split('.')[-2]))

        imgs_num = len(imgs)

        # shuffle
        np.random.seed(100)
        imgs = np.random.permutation(imgs)

        if self.test:
            self.imgs = imgs
        elif train:
            self.imgs = imgs[:int(0.9 * imgs_num)]
        else:
            self.imgs = imgs[int(0.9 * imgs_num):]

        # Image preprocessing
        if transform is None:
            normalize = T.Normalize(mean=[0.485, 0.456, 0.406],
                                    std=[0.229, 0.224, 0.225])
            if self.test or not train:
                self.transfrom = T.Compose([
                    T.Scale(227),
                    T.CenterCrop(227),
                    T.ToTensor(),
                    normalize
                ])
            else:
                self.transfrom = T.Compose([
                    T.Scale(256),
                    T.RandomSizedCrop(227),
                    T.RandomHorizontalFlip(),
                    T.ToTensor(),
                    normalize
                ])

    def __getitem__(self, index):
        img = self.imgs[index]
        if self.test:
            label = int((img.split('\\')[-1]).split('.')[-2])
        else:
            label = 1 if 'dog' in img else 0
        img = Image.open(img)
        data = self.transfrom(img)
        return data, label

    def __len__(self):
        return len(self.imgs)

