from common_utils import Point, IdsGenerator

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

    def predict(self, exemplar):
        pass

class Exemplar:
    def __init__(self):
        self.events_to_points = {}  # {id: point}

    def add(self, point, event_id):
        self.events_to_points[event_id] = point




