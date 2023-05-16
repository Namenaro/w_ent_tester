from recognise import Recogniser
from prog_ex import load_program_from_file, create_and_save_program, draw_program_to_ax, draw_exemplar_to_ax, draw_exemplars
from common_utils import HtmlLogger, Point
from picture_wrapper import Pic
from w_eval import ProgramWDistrs

import matplotlib.pyplot as plt
import numpy as np



def run_test(program, pic, grid_window_side, logger, surviving_max, wdistrs):
    points = pic.get_grid(grid_window_side)
    #points.append(program.get_point_of_event(program.get_event_id_by_i_in_order(0)))

    fig, ax = plt.subplots()
    draw_program_to_ax(ax, program=program, pic=pic)
    for point in points:
        ax.scatter(point.x, point.y)
    logger.add_fig(fig)
    logger.add_text(" количество выживающих в каждом поколении = " + str(surviving_max))


    for i in range(0, len(program)):
        all_best_exemplars, all_best_ws = test_subprog(len_subprog=i, program=program, points=points, logger=logger, wdistrs=wdistrs, pic=pic, surviving_max=surviving_max)

    m = 4
    best_m_indices = sorted(range(len(all_best_ws)), key=lambda i: all_best_ws[i], reverse=True)[:m]


    for i in best_m_indices:
        fig, ax = plt.subplots()
        exemplar = all_best_exemplars[i]
        logger.add_text("'экземпляр w = "+ str(all_best_ws[i]))
        draw_exemplar_to_ax(ax, exemplar=exemplar, program=program, pic=pic)
        logger.add_fig(fig)

    logger.add_text("Гистограмма значений w в экземплярах:")
    fig, ax = plt.subplots()
    ax.hist(all_best_ws)
    logger.add_fig(fig)

def test_subprog(len_subprog, program, points, logger, wdistrs, pic, surviving_max):
    fig, ax = plt.subplots()
    numpy_pic = np.zeros(shape=pic.img.shape)
    new_pic = Pic(numpy_pic)
    logger.add_line_little()
    logger.add_text("Длина подпрограммы = "+str(len_subprog+1))
    all_best_exemplars = []
    all_best_ws = []
    for point in points:
        program.set_phantome_first_event(phantome_point=point)
        recogniser = Recogniser(program=program, pic=pic, wdistrs=wdistrs)

        sorted_exemplars = recogniser.recognise(surviving_max=surviving_max, len_of_subprog=len_subprog+1)
        best_ws = recogniser.get_best_ws()
        top_N = 3
        all_best_exemplars += sorted_exemplars[:top_N]
        #logger.add_fig(draw_exemplars(sorted_exemplars, pic, program))

        point_w = best_ws[0]
        all_best_ws += best_ws[:top_N]
        new_pic.set_point_val(point, point_w)
        new_pic.draw_point(ax,point=point, str_for_point=str(float("{:.2f}".format(point_w))))
        print(str(point) + ", w=" + str(point_w))

    cax = ax.imshow(new_pic.img)
    fig.colorbar(cax)
    logger.add_fig(fig)
    return all_best_exemplars, all_best_ws


if __name__ == '__main__':
    pic = Pic(need_etalon=True, class_of_pisc=3)
    create_and_save_program(pic)
    program = load_program_from_file()
    logger = HtmlLogger("test_win_gr")
    wdistrs = ProgramWDistrs(program=program, pic=pic)
    wdistrs.fill()
    wdistr = wdistrs.get_w_distr_for_event(event_id="0")
    fig, ax = plt.subplots()
    ax.hist(wdistr.sample, density=True, edgecolor="black")
    logger.add_fig(fig)
    plt.clf()


    surviving_max = 7
    grid_window_side = 3

    logger.add_text("Запуск на эталоне")
    pic = Pic()
    run_test(program=program, pic=pic, grid_window_side=grid_window_side, logger=logger, surviving_max=surviving_max, wdistrs=wdistrs)

    logger.add_line_big()
    logger.add_text("Запуск той же программы, но на неэталонной картинке")
    pic = Pic(need_etalon=False, class_of_pisc=3)
    run_test(program=program, pic=pic, grid_window_side=grid_window_side, logger=logger, surviving_max=surviving_max, wdistrs=wdistrs)