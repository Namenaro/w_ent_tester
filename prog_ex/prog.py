from common_utils import Point, IdsGenerator
from picture_wrapper import Pic


class Event:
    def __init__(self, point, cloud_rad, vet, err_rad):
        self.point = point
        self.cloud_rad = cloud_rad
        self.err_rad = err_rad
        self.vet = vet


class Program:
    def __init__(self):
        self.events = {}  # {id: Event}
        self.order = [] # [id_1, ..., id_n]
        self.child_to_parent = {}  # {child_id: parent_id}

        self.ids_gen = IdsGenerator()

    def is_empty(self):
        return len(self.order) == 0

    def add_event(self, event, parent_id):
        event_id = str(self.ids_gen.generate_id())
        self.order.append(event_id)
        self.events[event_id] = event
        if parent_id is not None:
            self.child_to_parent[event_id] = parent_id

    def get_event(self, event_id):
        return self.events[event_id]

    def get_event_id_by_i_in_order(self, i):
        return self.order[i]

    def get_parent_point(self, event_id):
        parent_id = self.child_to_parent[event_id]
        parent_event = self.events[parent_id]
        return parent_event.point

    def get_point_of_event(self, event_id):
        return self.events[event_id].point

    def get_parent_id(self, event_id):
        return self.child_to_parent[event_id]

    def get_u(self, start_id, end_id):
        start_point = self.get_point_of_event(start_id)
        end_point = self.get_point_of_event(end_id)
        u = end_point - start_point
        return u

    def is_event_first(self, event_id):
        return event_id == self.order[0]

    def __len__(self):
        return len(self.order)

    def reset_first_event(self, new_point, new_errad):
        first_id = self.get_event_id_by_i_in_order(i=0)
        self.events[first_id].point = new_point
        self.events[first_id].err_rad = new_errad

class Exemplar:
    def __init__(self):
        self.events_to_points = {}  # {id: point}

    def add(self, point, event_id):
        self.events_to_points[event_id] = point

    def __len__(self):
        return len(self.events_to_points)

    def get_point_of_event(self, event_id):
        return self.events_to_points[event_id]

    def get_points_cloud_for_id(self, event_id, program):
        cloud_rad = program.get_event(event_id).cloud_rad
        point = self.get_point_of_event(event_id)
        point_cloud = Pic.get_point_cloud(point, cloud_rad)
        return point_cloud

    def get_point_of_parent(self, event_id, program):
        parent_id = program.get_parent_id(event_id)
        point_of_parent = self.events_to_points[parent_id]
        return point_of_parent



