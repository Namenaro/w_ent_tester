from prog import Program
from picture_wrapper import Pic
from common_utils import HtmlLogger, Point


import matplotlib.pyplot as plt
import math
import numpy as np


# правая кропка закрыть
class Creator:
    def __init__(self):
        self.pic = Pic()
        self.program = Program()

        self.fig, self.ax = plt.subplots()
        self.fig.canvas.mpl_connect('button_press_event', self.onclick)

    def onclick(self, event):
        if event.button != 1: # правая кропка закрыть
            plt.close()
            return
        # получаем данные клика
        x = math.ceil(event.xdata)
        y = math.ceil(event.ydata)
        point = Point(x=x, y=y)
        radius = int(input("Радиус облака: "))
        self.ax.clear()
        draw(point, radius, self.ax, self.pic)

        self.fig.canvas.draw()
        self.fig.canvas.flush_events()


    def run(self):
        plt.imshow(self.pic.img, cmap='gray')
        plt.show()
        return self.program

def draw(point, radius, ax, pic):
    pic.draw_to_ax(ax)
    pic.draw_rectangle(ax=ax, point=point, radius=radius)


# накликать программу вручную
# сохранить в файл, если задано его имя
if __name__ == '__main__':
    creator = Creator()
    creator.run()
