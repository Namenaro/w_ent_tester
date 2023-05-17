from common_utils import Point

import numpy as np
from PIL import Image


class TrajectoryGenerator:
    def __init__(self, start_point, inner_rad, window_size, stride, level):
        self.start_point = start_point
        self.inner_rad = inner_rad
        self.window_size = window_size
        self.stride = stride
        self.level = level
        self.indent = level * window_size

    def get_mean_value(self, x, y, window, window_size, image, height, width):
        if y <= -window_size or y >= height:
            mean_value = 0.0
        elif x <= -window_size or x >= width:
            mean_value = 0.0
        elif y + window_size > height and x >= 0 and x + window_size <= width:
            N = height - y
            pad_size = window_size - N
            new_window = image[y:height, x:x + window_size]
            extra_pixels = np.pad(new_window, ((0, pad_size), (0, 0)), 'constant')
            mean_value = np.mean(extra_pixels)
        elif y < 0 and x >= 0 and x + window_size <= width:
            N = window_size + y
            pad_size = window_size - N
            new_window = image[0:N, x:x + window_size]
            extra_pixels = np.pad(new_window, ((pad_size, 0), (0, 0)), 'constant')
            mean_value = np.mean(extra_pixels)
        elif x + window_size > width and y >= 0 and y + window_size <= height:
            N = width - x
            pad_size = window_size - N
            new_window = image[y:y + window_size, x:width]
            extra_pixels = np.pad(new_window, ((0, 0), (0, pad_size)), 'constant')
            mean_value = np.mean(extra_pixels)
        elif x < 0 and y >= 0 and y + window_size <= height:
            N = window_size + x
            pad_size = window_size - N
            new_window = image[y:y + window_size, 0:N]
            extra_pixels = np.pad(new_window, ((0, 0), (pad_size, 0)), 'constant')
            mean_value = np.mean(extra_pixels)
        elif x < 0 and y < 0:
            N_x = window_size + x
            N_y = window_size + y
            pad_size_x = window_size - N_x
            pad_size_y = window_size - N_y
            new_window = image[0:N_y, 0:N_x]
            extra_pixels = np.pad(new_window, ((pad_size_y, 0), (pad_size_x, 0)), 'constant')
            mean_value = np.mean(extra_pixels)
        elif x + window_size > width and y + window_size > height:
            N_x = width - x
            N_y = height - y
            pad_size_x = window_size - N_x
            pad_size_y = window_size - N_y
            new_window = image[y:height, x:width]
            extra_pixels = np.pad(new_window, ((0, pad_size_y), (0, pad_size_x)), 'constant')
            mean_value = np.mean(extra_pixels)
        elif x + window_size > width and y < 0:
            N_x = width - x
            N_y = window_size + y
            pad_size_x = window_size - N_x
            pad_size_y = window_size - N_y
            new_window = image[y:height, x:width]
            extra_pixels = np.pad(new_window, ((pad_size_y, 0), (0, pad_size_x)), 'constant')
            mean_value = np.mean(extra_pixels)
        elif x < 0 and y + window_size > height:
            N_x = window_size + x
            N_y = height - y
            pad_size_x = window_size - N_x
            pad_size_y = window_size - N_y
            new_window = image[y:height, x:width]
            extra_pixels = np.pad(new_window, ((0, pad_size_y), (pad_size_x, 0)), 'constant')
            mean_value = np.mean(extra_pixels)

        else:
            mean_value = np.mean(window)

        return mean_value

    def check_for_exception_coords(exception_coords, all_exception_coords, point, x, y, window, window_size, image,
                                   height, width, mean_values, coords):
        mean_value = TrajectoryGenerator.get_mean_value(x, y, window, window_size, image, height, width)

        all_coords = []
        for r in range(y, y + window_size):
            for c in range(x, x + window_size):
                all_coords.append((c, r))

        if exception_coords is not None and any(
                map(lambda v: v in all_exception_coords, all_coords)) is False or exception_coords is None:
            mean_values.append(mean_value)
            coords.append(point)

        return mean_values, coords

    def get_next(self, exception_coords, image):
        height, width = image.shape

        center_x = self.start_point.getX()
        center_y = self.start_point.getY()

        # List to store the mean values of each window
        mean_values = []

        # List to store the coordinates of the center of each window
        coords = []

        if exception_coords is not None:
            all_exception_coords = []
            for pt in exception_coords:
                xmin_pt = pt.getX() - self.window_size
                ymin_pt = pt.getY() - self.window_size
                xmax_pt = pt.getX()
                ymax_pt = pt.getY()

                for r in range(ymin_pt, ymax_pt):
                    for c in range(xmin_pt, xmax_pt):
                        all_exception_coords.append((c, r))

        # Traverse the neighborhood around the initial window using a sliding window

        # top
        for x in range(center_x - self.inner_rad - self.window_size - self.indent,
                       center_x + self.inner_rad + self.indent, self.stride):
            y = center_y - self.inner_rad - self.window_size - self.indent
            coord_x, coord_y = x + self.window_size // 2, y + self.window_size // 2
            point = Point(x=coord_x, y=coord_y)
            if exception_coords is not None and any(elem == point for elem in exception_coords):
                continue
            elif exception_coords is None or all(elem != point for elem in exception_coords):
                window_top = image[y:y + self.window_size, x:x + self.window_size]
                mean_values, coords = TrajectoryGenerator.check_for_exception_coords(exception_coords,
                                                                                     all_exception_coords, point, x, y,
                                                                                     window_top, self.window_size,
                                                                                     image, height, width, mean_values,
                                                                                     coords)

        # right
        for y in range(center_y - self.inner_rad - self.window_size - self.indent,
                       center_y + self.inner_rad + 1 + self.indent, self.stride):
            x = center_x + self.inner_rad + self.indent
            coord_x, coord_y = x + self.window_size // 2, y + self.window_size // 2
            point = Point(x=coord_x, y=coord_y)
            if exception_coords is not None and any(elem == point for elem in exception_coords):
                continue
            elif exception_coords is None or all(elem != point for elem in exception_coords):
                window_right = image[y:y + self.window_size, x:x + self.window_size]
                mean_values, coords = TrajectoryGenerator.check_for_exception_coords(exception_coords,
                                                                                     all_exception_coords, point, x, y,
                                                                                     window_right, self.window_size,
                                                                                     image, height, width, mean_values,
                                                                                     coords)

        # bottom
        for x in range(center_x - self.inner_rad - self.window_size - self.indent,
                       center_x + self.inner_rad + self.indent, self.stride):
            y = center_y + self.inner_rad + self.indent
            coord_x, coord_y = x + self.window_size // 2, y + self.window_size // 2
            point = Point(x=coord_x, y=coord_y)
            if exception_coords is not None and any(elem == point for elem in exception_coords):
                continue
            elif exception_coords is None or all(elem != point for elem in exception_coords):
                window_bottom = image[y:y + self.window_size, x:x + self.window_size]
                mean_values, coords = TrajectoryGenerator.check_for_exception_coords(exception_coords,
                                                                                     all_exception_coords, point, x, y,
                                                                                     window_bottom, self.window_size,
                                                                                     image, height, width, mean_values,
                                                                                     coords)

        #   to calculate missing window
        if x != center_x + self.inner_rad + self.indent:
            x = center_x + self.inner_rad + self.indent
            window_bottom = image[y:y + self.window_size, x:x + self.window_size]
            coord_x, coord_y = x + self.window_size // 2, y + self.window_size // 2
            point = Point(x=coord_x, y=coord_y)
            if exception_coords is not None and all(
                    elem != point for elem in exception_coords) or exception_coords is None:
                mean_values, coords = TrajectoryGenerator.check_for_exception_coords(exception_coords,
                                                                                     all_exception_coords, point, x, y,
                                                                                     window_bottom, self.window_size,
                                                                                     image, height, width, mean_values,
                                                                                     coords)

        # left
        for y in range(center_y - self.inner_rad - self.window_size + self.stride - self.indent,
                       center_y + self.inner_rad + self.indent, self.stride):
            x = center_x - self.inner_rad - self.window_size - self.indent
            coord_x, coord_y = x + self.window_size // 2, y + self.window_size // 2
            point = Point(x=coord_x, y=coord_y)
            if exception_coords is not None and any(elem == point for elem in exception_coords):
                continue
            elif exception_coords is None or all(elem != point for elem in exception_coords):
                window_left = image[y:y + self.window_size, x:x + self.window_size]
                mean_values, coords = TrajectoryGenerator.check_for_exception_coords(exception_coords,
                                                                                     all_exception_coords, point, x, y,
                                                                                     window_left, self.window_size,
                                                                                     image, height, width, mean_values,
                                                                                     coords)

        brightness = mean_values

        return coords, brightness


def main():
    image = np.zeros((50, 50))

    window_size = 5
    inner_rad = 3
    stride = 5

    start_x, start_y = 15, 15
    start_point = Point(x=start_x, y=start_y)
    point_1, point_2, point_3 = Point(x=5, y=5), Point(x=7, y=15), Point(x=23, y=15)
    exception_coords = [point_1, point_2, point_3]
    #     exception_coords = None

    for level in range(4):
        trajectory = TrajectoryGenerator(start_point, inner_rad, window_size, stride, level)
        coords, brightness = trajectory.get_next(exception_coords, image)
        round_brightness = [round(elem, 2) for elem in brightness]
        print('level', level)
        print('brightness: ', round_brightness)
        coords_to_print = []
        for elem in coords:
            coords_to_print.append((elem.getX(), elem.getY()))
        print('coords: ', coords_to_print)


if __name__ == "__main__":
    main()
