from prog_ex.prog import Program, Event
from prog_ex.drawer_program import draw_program_to_ax
from picture_wrapper import Pic
from common_utils import Point

import jsonpickle
import matplotlib.pyplot as plt
import math
import numpy as np

def create_program(pic):
    creator = Creator(pic)
    program = creator.run()
    return program

def create_and_save_program(pic, filename='default_pro'):
    program = create_program(pic)
    with open(filename, "w") as write_file:
        write_file.write(jsonpickle.encode(program))

def load_program_from_file(filename='default_pro'):
    with open(filename, "r") as read_file:
        return jsonpickle.decode(read_file.read())

# правая кропка закрыть
class Creator:
    def __init__(self, pic):
        self.pic = pic
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

        # заполняем эталон события
        point = Point(x=x, y=y)
        cloud_radius = int(input("Радиус облака: "))
        err_radius = int(input("Радиус адаптации:"))

        parent_id = None
        if not self.program.is_empty():
            parent_id = str(input("Номер родителя: "))

        vet = self.pic.get_mean_val_around_point(point, cloud_radius)
        event = Event(point=point, cloud_rad=cloud_radius, err_rad=err_radius, vet=vet)
        self.program.add_event(event=event, parent_id=parent_id)

        # перерисовываем картинку
        self.ax.clear()
        draw_program_to_ax(self.ax, self.pic, self.program)
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

    def run(self):
        plt.imshow(self.pic.img, cmap='gray')
        plt.show()
        return self.program


# накликать программу вручную
# сохранить в файл, если задано его имя
if __name__ == '__main__':
    pic = Pic()
    filename = "ident_pro"
    create_and_save_program(pic)

    print("Отрисуем сохраненнную ранее программу:")
    program = load_program_from_file()
    fig, ax = plt.subplots()
    draw_program_to_ax(ax, program=program, pic=pic)
    plt.show()
