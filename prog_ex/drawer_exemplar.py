from picture_wrapper import Pic
from common_utils import Point
from .prog import Program, Event

import matplotlib.pyplot as plt
import numpy as np


def draw_exemplar_to_ax(ax, exemplar, program, pic):
    pic.draw_to_ax(ax)
    for event_id, point in exemplar.events_to_points.items():
        pic.draw_point(ax=ax, point=point, str_for_point=str(event_id))
        if program.is_event_first(event_id) is False:
            point_of_parent = exemplar.get_point_of_parent(event_id, program)
            pic.connect_two_points_by_arrow(ax, point_from=point_of_parent, point_to=point)


def draw_exemplars(exemplars, pic, program):
    num_exemplars = len(exemplars)
    fig, axs = plt.subplots(1, num_exemplars)
    for i in range(num_exemplars):
        draw_exemplar_to_ax(axs[i], exemplars[i], program, pic)
    return fig
