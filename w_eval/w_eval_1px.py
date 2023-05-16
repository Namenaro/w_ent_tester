from picture_wrapper import Pic
from common_utils import Distr

class WEval1px:
    def __init__(self, pic):
        self.pic = pic

    def get_w(self, vet, vreal):
        return 1 - self.pic.distr.get_p_of_event(vet, vreal)

    def get_w_distr(self, vet):
        w_sample = []
        v_sample = self.pic.distr.get_sample(sample_size=None)
        for vreal in v_sample:
            w=self.get_w(vreal=vreal, vet=vet)
            w_sample.append(w)
        return Distr(max=1, min=0, sample=w_sample)

    def get_vicinity_size(self, rad):
        return self.pic.get_num_points_in_vicitiny(rad)

    def get_went_by_w(self, w_distr, w_real, err_radius):
        nvals = self.get_vicinity_size(err_radius)
        max_w = w_distr.get_max()
        p = w_distr.get_p_of_at_least_one_of_n_in_range(val1=w_real, val2=max_w, n=nvals)
        return 1 - p

    def get_went_by_v(self, vreal, vet, err_radius, w_distr=None):
        w_real = self.get_w(vet=vet, vreal=vreal)
        if w_distr is None:
            w_distr = self.get_w_distr(vet)
        return self.get_went_by_w(w_distr=w_distr, w_real=w_real, err_radius=err_radius)


