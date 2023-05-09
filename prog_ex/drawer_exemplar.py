from picture_wrapper import Pic
from common_utils import Point
from prog import Program, Event


def draw_exemplar_to_ax(ax, exemplar, program, pic):
    pic.draw_to_ax(ax)
    for event_id, point in exemplar.events_to_points.items():
        pic.draw_point(ax=ax, point=point, str_for_point=str(event_id))
        if program.is_event_first(event_id) is False:
            point_of_parent = exemplar.get_point_of_parent(event_id, program)
            pic.connect_two_points_by_arrow(ax, point_from=point_of_parent, point_to=point)
