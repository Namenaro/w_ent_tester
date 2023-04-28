from common_utils import HtmlLogger, Point
from picture_wrapper import Pic, get_point_from_user
from w_eval_1px import WEval1px


import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib as mpl
import numpy as np

def test_went_around_T__1(pic):
    logger = HtmlLogger("t1")
    eval1px = WEval1px(pic)

    print("сделать один клик: выберется T, а яркость в ней обозначаем vet")
    T = get_point_from_user(pic)
    
    # рисуем сам клик:
    fig, ax = plt.subplots()
    pic.draw_to_ax(ax)
    pic.draw_point(ax, T, str_for_point=None, color='green')
    logger.add_fig(fig)

    # рисуем гистограмму w
    vet = pic.get_val_in_point(T)
    w_distr = eval1px.get_w_distr(vet)
    fig, ax = plt.subplots()
    ax.set_title('w_distr')
    ax.hist(w_distr.sample)
    logger.add_fig(fig)


    numpy_pic = np.zeros(shape=pic.img.shape)
    new_pic = Pic(numpy_pic)
    X, Y = pic.get_max_XY()
    for x in range(X):
        for y in range(Y):
            t = Point(x, y)
            vreal = pic.get_val_in_point(t)
            err_radius = t.dist_to(T)
            w_ent = eval1px.get_went_by_v(vreal=vreal, vet=vet, err_radius=err_radius, w_distr=w_distr)
            new_pic.set_point_val(t, w_ent)


    fig, ax = plt.subplots()
    ax.set_title('T=' + str(T) + ", vet=" + str(vet))
    cmap = cm.coolwarm
    norm = mpl.colors.Normalize(vmin=0, vmax=1)  # norm = mpl.colors.TwoSlopeNorm(vmin=0,vcenter=0.5, vmax=1)
    im = ax.imshow(new_pic.img, norm=norm, cmap=cmap)
    plt.colorbar(im)
    logger.add_fig(fig)

if __name__ == '__main__':
    pic = Pic()
    test_went_around_T__1(pic)