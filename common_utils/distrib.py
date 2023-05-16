import numpy as np
import matplotlib.pyplot as plt
from random import choices


class Distr:
    def __init__(self, max, min, sample=None):
        self.max = max
        self.min = min
        self.uniform = False

        if sample is None:
            self.uniform = True

        self.sample = sample

    def get_p_of_val(self, val):
        if self.uniform:
            return 1/self.max
        num_of_target_elements = list(self.sample).count(val)
        return num_of_target_elements/len(self.sample)

    def get_p_of_event(self, val_1, val_2):

        if val_1 < val_2:
            left = val_1
            right = val_2

        elif val_1 > val_2:
            left = val_2
            right = val_1

        elif val_1 == val_2:
            return self.get_p_of_val(val_1)

        if self.uniform:
            return (right - left) / (self.max - self.min)

        counts = [el for el in self.sample if left <= el <= right]

        return len(counts) / len(self.sample)

    def draw(self):
        if not self.uniform:
            fig, ax = plt.subplots()
            ax.hist(self.sample, density=True, edgecolor="black")

        else:

            fig, ax = plt.subplots()
            tmp_sample = np.random.uniform(self.min, self.max, 200)
            ax.hist(tmp_sample, density=True, edgecolor="black")


        return fig

    def get_mean(self):
        if not self.uniform:
            return np.mean(self.sample)
        else:
            return (self.max + self.min) / 2


    def get_sample(self, sample_size):
        if self.sample is not None:
            if sample_size is not None:
                return choices(self.sample, k=sample_size)
            else:
                return self.sample
        if sample_size is None:
            sample_size = 100
        return np.random.choice(255, sample_size)

    def get_p_of_at_least_one_of_n_in_range(self, val1, val2, n):
        # вероятность, что хотя бы 1 значение из n штук случайно взятых, попадет в диапазон
        p_element_not_in_range = 1 - self.get_p_of_event(val1, val2)
        return 1 - (p_element_not_in_range ** n)

    def get_max(self):
        return self.max



