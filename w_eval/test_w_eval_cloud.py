from common_utils import HtmlLogger, Point
from picture_wrapper import Pic, get_point_from_user, get_point_and_radius_from_user
from w_eval_1px import WEval1px
from w_eval_cloud import WEvalCloud


import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib as mpl
import numpy as np


def test_went_around_T__cloud(pic, max_went):
    logger = HtmlLogger("tn")
    eval1px = WEval1px(pic)

    print("Выбрать точку на картинке и радиус окна вокруг нее. Яркость в окне обозначим за vet")

    T, radius = get_point_and_radius_from_user(pic)
    print(T)
    all_cloud_points = pic.get_point_cloud(center_point=T, radius=radius)
    vet = pic.get_mean_val_in_point_cloud(all_cloud_points)
    print ("vet = " + str(vet))
    cloud_size = len(all_cloud_points)

    # рисуем сам клик:
    fig, ax = plt.subplots()
    pic.draw_to_ax(ax)
    pic.draw_point(ax, T, str_for_point=None, color='green')
    logger.add_fig(fig)

    eval_cloud = WEvalCloud(pic, evaluator_1px=eval1px)

    # рисуем гистограмму w
    vet = pic.get_val_in_point(T)
    w_distr = eval_cloud.get_w_distr(vet, cloud_size=cloud_size)
    fig, ax = plt.subplots()
    ax.set_title('w_distr for cloud w')
    ax.hist(w_distr.sample)
    logger.add_fig(fig)


    # рисуем карту активации w_ent для окна данного радиуса вокруг Т, поставленной в точке клика
    numpy_pic = np.zeros(shape=pic.img.shape)
    new_pic = Pic(numpy_pic)
    X, Y = pic.get_max_XY()
    for x in range(X):
        for y in range(Y):
            t = Point(x, y)
            w_ent = eval_cloud.get_went(cloud_center_point=t, all_cloud_points=all_cloud_points,
                                T=T, vet=vet, points_to_exclude=[], w_distr=w_distr)
            new_pic.set_point_val(t, w_ent)

    fig, ax = plt.subplots()
    ax.set_title('T=' + str(T) + ", vet=" + str(vet))
    cmap = cm.coolwarm
    norm = mpl.colors.Normalize(vmin=0, vmax=max_went)  # norm = mpl.colors.TwoSlopeNorm(vmin=0,vcenter=0.5, vmax=1)
    im = ax.imshow(new_pic.img, norm=norm, cmap=cmap)
    plt.colorbar(im)
    logger.add_fig(fig)


if __name__ == '__main__':
    pic = Pic()
    test_went_around_T__cloud(pic, 9)