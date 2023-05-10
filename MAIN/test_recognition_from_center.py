from recognise import Recogniser
from prog_ex import load_program_from_file, create_and_save_program, draw_program_to_ax, draw_exemplar_to_ax
from common_utils import HtmlLogger
from picture_wrapper import Pic

import matplotlib.pyplot as plt


def run_test():
    logger = HtmlLogger("reco_test_form_center")
    pic = Pic()
    #create_and_save_program(pic)
    program = load_program_from_file()

    logger.add_text("Тест движка распознавания. Распознается программа:")
    fig, ax = plt.subplots()
    draw_program_to_ax(ax, program=program, pic=pic)
    logger.add_fig(fig)

    logger.add_text("Лучший экземпляр:")
    recogniser = Recogniser(program=program, pic=pic)
    sorted_exemplars = recogniser.recognise(surviving_max=5)
    fig, ax = plt.subplots()
    draw_exemplar_to_ax(ax, exemplar=sorted_exemplars[0], program=program, pic=pic)
    logger.add_fig(fig)


if __name__ == '__main__':
    run_test()
