from recognise import Recogniser
from prog_ex import load_program_from_file, create_and_save_program, draw_program_to_ax, draw_exemplar_to_ax, draw_exemplars
from common_utils import HtmlLogger, Point
from picture_wrapper import Pic
from w_eval import ProgramWDistrs

import matplotlib.pyplot as plt
import numpy as np


def run_test():
    logger = HtmlLogger("test_form_point2")
    pic = Pic()
    #create_and_save_program(pic)
    program = load_program_from_file()

    wdistrs = ProgramWDistrs(program=program, pic=pic)

    points = pic.get_grid(window_side=5)
    points.append(program.get_point_of_event(program.get_event_id_by_i_in_order(0)))


    logger.add_text("Тест движка распознавания из ТОЧЕК. Распознается программа:")
    fig, ax = plt.subplots()
    draw_program_to_ax(ax, program=program, pic=pic)
    for point in points:
        ax.scatter(point.x, point.y)
    logger.add_fig(fig)

    fig, ax = plt.subplots()
    numpy_pic = np.zeros(shape=pic.img.shape)
    new_pic = Pic(numpy_pic)

    for point in points:
        program.set_phantome_first_event(phantome_point=point)
        recogniser = Recogniser(program=program, pic=pic, wdistrs=wdistrs)
        sorted_exemplars = recogniser.recognise(surviving_max=4)

        logger.add_fig(draw_exemplars(sorted_exemplars, pic, program))

        best_ws = recogniser.get_best_ws()
        point_w = best_ws[0]
        new_pic.set_point_val(point, point_w)
        print(str(point) + ", w="+ str(point_w))

    cax=ax.imshow(new_pic.img)
    fig.colorbar(cax)
    logger.add_fig(fig)



if __name__ == '__main__':
    run_test()