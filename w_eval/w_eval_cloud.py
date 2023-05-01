from w_eval_1px import WEval1px
from common_utils import Distr, Point

class WEvalCloud:
    def __init__(self, pic, evaluator_1px):
        self.pic = pic
        self.evaluator_1_px = evaluator_1px

    def get_w(self, vet, vreals):
        w = 0
        for vreal in vreals:
            w += self.evaluator_1_px.get_w(vet=vet, vreal=vreal)
        return w

    def get_w_distr(self, vet, cloud_size, sample_len=100):
        w_sample = []
        for i in range(sample_len):
            v_sample = self.pic.distr.get_sample(sample_size=cloud_size)
            w_sample.append(self.get_w(vet=vet, vreals=v_sample))
        return Distr(max=cloud_size, min=0, sample=w_sample)

    #-----------------------------------------------------------------------
    #ОСНОВНОЙ МЕТОД---------------------------------------------------------
    # went для центра облака считаем относительно T, а went-ы
    # остальных точек облака cчитаем относительно центра. Все went-ы складываем
    def get_went(self, cloud_center_point, all_cloud_points, T, vet, points_to_exclude, w_distr_1px=None):
        went = 0

        if cloud_center_point not in points_to_exclude:
            err_radius_for_center = T.dist_to(cloud_center_point)
            v_in_center = self.pic.get_val_in_point(cloud_center_point)
            went_for_center = self.evaluator_1_px.get_went_by_v(vreal=v_in_center, vet=vet,
                                                                err_radius=err_radius_for_center,
                                                                w_distr=w_distr_1px)
            went += went_for_center

        for point in all_cloud_points:
            if point == cloud_center_point:
                continue
            if point in points_to_exclude:
                continue
            err_radius_for_point = cloud_center_point.dist_to(point)
            v_in_point = self.pic.get_val_in_point(point)
            went_for_point = self.evaluator_1_px.get_went_by_v(vreal=v_in_point, vet=vet,
                                                               err_radius=err_radius_for_point,
                                                               w_distr=w_distr_1px)
            went += went_for_point


        return went



