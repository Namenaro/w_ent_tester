from test_w_eval_cloud import test_went_around_T__cloud
from test_w_eval_1px import test_went_around_T__1

from common_utils import Point
from picture_wrapper import Pic

if __name__ == '__main__':
    pic = Pic()
    max_went = 9
    test_went_around_T__1(pic, max_went)
    test_went_around_T__cloud(pic, max_went)