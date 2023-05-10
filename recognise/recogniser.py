from .predictor import predict_next_event
from .generation import Generation
from prog_ex import Program, Exemplar, Event
from w_eval import ProgramWDistrs

import copy

class Recogniser:
    def __init__(self, pic, program, wdistrs=None):
        self.pic = pic
        self.program = program
        self.generations_list = []
        self.wdistrs = wdistrs
        if self.wdistrs is None:
            self.wdistrs = ProgramWDistrs(program=self.program, pic=self.pic)
        self.wdistrs.fill()

    def recognise(self, surviving_max):
        self._init_first_generation()

        for i in range(1, len(self.program)):
            self._create_next_generaion(surviving_max)

        best_exemplars = self.generations_list[-1].get_all_exemplars_sorted()
        return best_exemplars

    def get_best_ws(self):
        ws = self.generations_list[-1].get_all_ws_sorted()
        return ws

    def _init_first_generation(self):
        first_generation = Generation(pic=self.pic, program=self.program, wdistrs=self.wdistrs)
        event_id, event, point = predict_next_event(exemplar=None, program=self.program)
        start_points_cloud = self.pic.get_point_cloud(center_point=point, radius=event.err_rad)
        for start_point in start_points_cloud:
            exemplar = Exemplar()
            exemplar.add(start_point, event_id=event_id)
            first_generation.insert_new_exemplar(exemplar)
        self.generations_list.append(first_generation)


    def _create_next_generaion(self, surviving_max):
        next_generation = Generation(pic=self.pic, program=self.program, wdistrs=self.wdistrs)
        # предыдущее поколение всегда есть и не пусто
        for exemplar_entry in self.generations_list[-1].entries:
            exemplar = exemplar_entry.realisation
            children_exemplars_list = self._get_children_for_exemplar(exemplar)
            for child_exemplar in children_exemplars_list:
                next_generation.insert_new_exemplar(child_exemplar)
        # обрезаем размер, чтобы избежать взрыва
        next_generation.cut_extra_exemplars(surviving_max)
        self.generations_list.append(next_generation)

    def _get_children_for_exemplar(self, exemplar):
        children_exemplars = []
        event_id, event, point = predict_next_event(exemplar=exemplar, program=self.program)
        start_points_cloud = self.pic.get_point_cloud(center_point=point, radius=event.err_rad)
        for start_point in start_points_cloud:
            exemplar = copy.deepcopy(exemplar)
            exemplar.add(point=start_point, event_id=event_id)
            children_exemplars.append(exemplar)
        return children_exemplars


