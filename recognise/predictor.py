from prog_ex import Program, Exemplar, Event


def predict_next_event(exemplar, program):
    if exemplar is None:
        return predict_first_event(program)

    i_of_next_event = len(exemplar) + 1
    event_id = program.get_event_id_by_i_in_order(i_of_next_event)

    parent_id = program.get_parent_id(event_id)
    u = program.get_u(start_id=parent_id, end_id=event_id)
    parent_real_point = exemplar.get_point_of_event(parent_id)
    point = parent_real_point + u

    event = program.get_event(event_id=event_id)
    return event_id, event, point

def predict_first_event(program):
    event_id = program.order[0]
    event = program.events[event_id]
    point = event.point
    return event_id, event, point

