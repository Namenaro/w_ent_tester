from w_eval_cloud import WEvalCloud
from w_eval_1px import WEval1px
from common_utils import Point
from picture_wrapper import Pic
from prog_ex import Program, Event, Exemplar


W_KEY = 'w'
WENT_KEY = 'went'


class PointData:
    def __init__(self, point, exemplar, program):
        pass

    def get_winner_id_by_w(self):
        return w_winner_id

    def get_went_by_event_id(self, event_id):
        return

    def fill(self):
        return True

    def eval(self):

def eval_exemplar(exemplar, program, pic):
    w = 0
    X, Y = pic.get_max_XY()
    for x in range(X):
        for y in range(Y):
            point = Point(x, y)
            point_data = PointData(point, exemplar=exemplar, program=program)
            point_data.fill()
            w += point_data.eval()

    return w


