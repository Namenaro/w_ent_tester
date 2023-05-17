from picture_wrapper.pic import Pic


import numpy as np
import random
import torchvision.datasets as datasets
import os
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.patches as mpatches
import matplotlib
from math import ceil
import random

np.random.seed(0)
random.seed(0)

class PicGetter:
    def __init__(self, class_of_pisc=3):
        self.class_of_pisc = class_of_pisc
        dir_path = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(dir_path, '../MNIST')
        self.dataset = datasets.MNIST(root=path, train=True, download=True, transform=None)

    def get_train_targets(self, n=10):
        pics = []
        for element in self.dataset:
            if element[1] == self.class_of_pisc:
                img = np.array(element[0])
                pics.append(Pic(numpy_pic=img))
                if len(pics) == n+1:
                    break
        return pics[1:]

    def get_train_contrasts(self, n=10):
        pics = []
        while True:
            if len(pics) == n:
                break
            index = random.choice(range(0, len(self.dataset)))
            element = self.dataset[index]
            if element[1] != self.class_of_pisc:
                img = np.array(element[0])
                pics.append(Pic(numpy_pic=img))

        return pics

if __name__ == '__main__':
    pic_getter = PicGetter(class_of_pisc=3)
    contrast_pics = pic_getter.get_train_contrasts()

    fig, ax = plt.subplots()
    pic = contrast_pics[3]
    pic.draw_to_ax(ax)
    center_point = pic.get_center_point()
    pic.annotate_point(ax, center_point, 'НЕцелевой класс')
    plt.show()
    plt.close(fig)

    target_pics = pic_getter.get_train_targets()
    fig, ax = plt.subplots()
    pic = target_pics[1]
    pic.draw_to_ax(ax)
    center_point = pic.get_center_point()
    pic.annotate_point(ax, center_point, 'целевой класс')
    plt.show()
    plt.close(fig)