from common_utils import Point


def get_grid_points_one_axis(window_side, pic_side):
    hside= int(window_side/2)
    start= hside +  1
    end = pic_side - (hside+1)

    xs = list(range(start, end, window_side))
    return xs


def get_grid_points(window_side, pic_side_X, pic_side_Y):
    xs = get_grid_points_one_axis(window_side=window_side, pic_side=pic_side_X)
    ys = get_grid_points_one_axis(window_side=window_side, pic_side=pic_side_Y)
    points = []
    for x in xs:
        for y in ys:
            point = Point(x, y=y)
            points.append(point)
    return points

