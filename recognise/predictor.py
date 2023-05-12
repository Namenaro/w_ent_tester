from prog_ex import Program


def predict_next_event(exemplar, program):
    if exemplar is None or len(exemplar) == 0:
        return predict_first_event(program)

    i_of_next_event = len(exemplar)
    event_id = program.get_event_id_by_i_in_order(i_of_next_event)

    point = get_predicted_point_for_event(event_id, exemplar, program)

    event = program.get_event(event_id=event_id)
    return event_id, event, point


def get_predicted_point_for_event(event_id, exemplar, program):
    if event_id == program.get_event_id_by_i_in_order(0):
        _, _, point = predict_first_event(program)
        return point
    parent_id = program.get_parent_id(event_id)
    u = program.get_u(start_id=parent_id, end_id=event_id)
    parent_real_point = exemplar.get_point_of_event(parent_id)
    point = parent_real_point + u
    return point


def predict_first_event(program):
    point = program.get_phantome_point()
    event_id = program.order[0]
    event = program.events[event_id]
    if point is not None:
        return event_id, event, point

    point = event.point
    return event_id, event, point

