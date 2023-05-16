from recognise import get_predicted_point_for_event
from .w_eval_1px import WEval1px
from common_utils import Point
from picture_wrapper import Pic
from prog_ex import Program, Event, Exemplar


W_KEY = 'w'
WENT_KEY = 'went'


class PointData:
    def __init__(self, point, exemplar, program, pic, program_w_distrs):
        self.point = point
        self.exemplar = exemplar
        self.program = program
        self.pic = pic
        self.program_w_distrs = program_w_distrs
        self.evaluator_1px = WEval1px(self.pic)

        # все три массива индексируются одним индексом
        self.event_ids = []
        self.w_s = []
        self.went_s = []


    def fill(self):
        val_in_point = self.pic.get_val_in_point(self.point)

        for event_id, point in self.exemplar.events_to_points.items():
            point_cloud_of_event = self.exemplar.get_points_cloud_for_id(event_id, self.program)
            if self.point in point_cloud_of_event:
                self.event_ids.append(event_id)

                vet = self.program.get_event(event_id).vet
                w = self.evaluator_1px.get_w(vet=vet, vreal=val_in_point)
                self.w_s.append(w)

                predicted_point = get_predicted_point_for_event(event_id, self.exemplar, self.program)
                went = self.get_went_for_point_by_event(event_id, w, real_point=point, predicted_point=predicted_point)
                self.went_s.append(went)

    def eval(self):
        if len(self.went_s) == 0:
            return 0
        w = max(self.went_s)
        return float(w)

    def get_went_for_point_by_event(self, event_id, w_real, real_point, predicted_point):
        w_distr = self.program_w_distrs.get_w_distr_for_event(event_id)
        err_radius = real_point.dist_to(predicted_point)
        went = self.evaluator_1px.get_went_by_w(w_real=w_real,
                                                w_distr=w_distr,
                                                err_radius=err_radius)
        return went


def eval_exemplar(exemplar, program, pic, wdistrs):
    w = 0

    X, Y = pic.get_max_XY()

    for x in range(X):
        for y in range(Y):
            point = Point(x, y)

            point_data = PointData(point, exemplar=exemplar, program=program, pic=pic, program_w_distrs=wdistrs)
            point_data.fill()
            w_in_point = point_data.eval()

            w+= w_in_point


    return w


