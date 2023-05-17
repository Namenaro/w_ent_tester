from recognise import Recogniser
from prog_ex import load_program_from_file, create_and_save_program, draw_program_to_ax, draw_exemplar_to_ax, draw_exemplars
from common_utils import HtmlLogger, Point
from picture_wrapper import Pic
from w_eval import ProgramWDistrs

import matplotlib.pyplot as plt
import numpy as np



if __name__ == '__main__':
    pic = Pic(need_etalon=True, class_of_pisc=3)
    #create_and_save_program(pic)
    program = load_program_from_file()
    logger = HtmlLogger("test_win_gr")
    wdistrs = ProgramWDistrs(program=program, pic=pic)
    wdistrs.fill()
    wdistr = wdistrs.get_w_distr_for_event(event_id="0")

    point = Point(2, 2)
    program.set_phantome_first_event(phantome_point=point)

    surviving_max = 7
    grid_window_side = 3

    recogniser = Recogniser(program=program, pic=pic, wdistrs=wdistrs)

    sorted_exemplars = recogniser.recognise(surviving_max=surviving_max, len_of_subprog=1)
    best_ws = recogniser.get_best_ws()
    print(best_ws)