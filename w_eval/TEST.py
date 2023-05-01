from test_w_eval_cloud import test_went_around_T__cloud, test_went_around_T__cloud_
from test_w_eval_1px import test_went_around_T__1, test_went_around_T__1_

from common_utils import Point, HtmlLogger
from picture_wrapper import Pic

if __name__ == '__main__':
    pic = Pic()

    max_went = 9
    T = Point(x=14, y=14)

    logger = HtmlLogger("t3")
    test_went_around_T__cloud_(pic=pic, radius=3, T=T, max_went=max_went, logger=logger)

    logger = HtmlLogger("t2")
    test_went_around_T__cloud_(pic=pic, radius=2, T=T,  max_went=max_went, logger=logger)


    test_went_around_T__1_(pic=pic, max_went=max_went, T=T)
