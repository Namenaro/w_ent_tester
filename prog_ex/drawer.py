from picture_wrapper import Pic
from common_utils import Point
from prog import Program, Event


def draw_program_to_ax(ax, pic, program):
    for i in range(len(program.order)):
        event_id = program.order[i]
        draw_event(event_id, pic, ax, program)
        if i == 0:
            continue
        draw_arrow_to_event(event_id, program, ax)


def draw_event(event_id, pic, ax, program):
    event = program.get_event(event_id)
    pic.draw_rectangle(ax=ax, radius=event.cloud_rad, point=event.point)
    pic.draw_point(point=event.point, str_for_point=str(event_id))


def draw_arrow_to_event(event_id, program, pic, ax):
    parent_point = program.get_parent_point(event_id)
    event = program.get_event(event_id)
    pic.connect_two_points_by_arrow(ax, point_from=parent_point, point_to=event.point)