from recognise import Recogniser
from prog_ex import load_program_from_file, create_and_save_program, draw_program_to_ax, draw_exemplar_to_ax
from common_utils import HtmlLogger, Point
from picture_wrapper import Pic
from w_eval import ProgramWDistrs

import matplotlib.pyplot as plt
import numpy as np


def run_test():
    logger = HtmlLogger("reco_test_form_points")
    pic = Pic()
    #create_and_save_program(pic)
    program = load_program_from_file()

    wdistrs = ProgramWDistrs(program=program, pic=pic)

    logger.add_text("Тест движка распознавания из ТОЧЕК. Распознается программа:")
    fig, ax = plt.subplots()
    draw_program_to_ax(ax, program=program, pic=pic)
    logger.add_fig(fig)

    fig, ax = plt.subplots()
    numpy_pic = np.zeros(shape=pic.img.shape)
    new_pic = Pic(numpy_pic)
    X, Y = pic.get_max_XY()
    for x in range(20):
        for y in range(3, 17):
            point = Point(x, y)
            print(point)
            program.set_phantome_first_event(phantome_point=point)
            recogniser = Recogniser(program=program, pic=pic, wdistrs=wdistrs)
            sorted_exemplars = recogniser.recognise(surviving_max=4)
            best_ws = recogniser.get_best_ws()
            point_w = best_ws[0]
            new_pic.set_point_val(point, point_w)
    ax.imshow(new_pic.img)
    logger.add_fig(fig)

if __name__ == '__main__':
    run_test()
