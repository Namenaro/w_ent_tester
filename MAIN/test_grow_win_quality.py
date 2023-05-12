from recognise import Recogniser
from prog_ex import load_program_from_file, create_and_save_program, draw_program_to_ax, draw_exemplar_to_ax, draw_exemplars
from common_utils import HtmlLogger, Point
from picture_wrapper import Pic
from w_eval import ProgramWDistrs

import matplotlib.pyplot as plt
import numpy as np



def run_test(program, pic, grid_window_side, html_name, surviving_max):

    wdistrs = ProgramWDistrs(program=program, pic=pic)

    points = pic.get_grid(grid_window_side)
    points.append(program.get_point_of_event(program.get_event_id_by_i_in_order(0)))

    logger = HtmlLogger(html_name)
    fig, ax = plt.subplots()
    draw_program_to_ax(ax, program=program, pic=pic, surviving_max=surviving_max)
    for point in points:
        ax.scatter(point.x, point.y)
    logger.add_fig(fig)
    logger.add_text(" количество выживающих в каждом поколении = " + str(surviving_max))


    for i in range(1, len(program)):
        test_subprog(len_subprog=i, program=program, points=points, logger=logger, wdistrs=wdistrs, pic=pic)


def test_subprog(len_subprog, program, points, logger, wdistrs, pic, surviving_max):
    fig, ax = plt.subplots()
    numpy_pic = np.zeros(shape=pic.img.shape)
    new_pic = Pic(numpy_pic)
    logger.add_line_little()
    logger.add_text("Длина подпрограммы = "+str(len_subprog))
    for point in points:
        program.set_phantome_first_event(phantome_point=point)
        recogniser = Recogniser(program=program, pic=pic, wdistrs=wdistrs)
        sorted_exemplars = recogniser.recognise(surviving_max=surviving_max, len_of_subprog=len_subprog+1)

        #logger.add_fig(draw_exemplars(sorted_exemplars, pic, program))

        best_ws = recogniser.get_best_ws()
        point_w = best_ws[0]
        new_pic.set_point_val(point, point_w)
        print(str(point) + ", w=" + str(point_w))

    cax = ax.imshow(new_pic.img)
    fig.colorbar(cax)
    logger.add_fig(fig)


if __name__ == '__main__':
    pic = Pic()
    create_and_save_program(pic)
    program = load_program_from_file()
    pic = Pic()
    surviving_max=10
    run_test(program=program, pic=pic, grid_window_side=5, html_name="test_win_gr", surviving_max=surviving_max)