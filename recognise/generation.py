from prog_ex import Program, Exemplar
from picture_wrapper import Pic
from w_eval import eval_exemplar
from common_utils import measure_win_quality

from collections import namedtuple
from bisect import insort

RealisationEntry = namedtuple('RealisationEntry', ('realisation', 'non_triviality'))


class Generation:
    def __init__(self, pic, program):
        self.entries = []

        self.pic = pic
        self.program = program

    def insert_new_exemplar(self, exemplar):
        w = eval_exemplar(exemplar=exemplar, program=self.program, pic=self.pic)
        entry = RealisationEntry(exemplar, w)
        insort(self.entries, entry, key=lambda x: -x.non_triviality)  # в порядке убывания

    def cut_extra_exemplars(self, surviving_max):
        if len(self.entries) > surviving_max:
            self.entries = self.entries[:surviving_max]

    def get_num_of_ended_exemplars(self):
        num = 0
        for exemplar_entry in self.entries:
            if len(exemplar_entry.realisation) == len(self.program):
                num += 1
        return num

    def __len__(self):
        return len(self.entries)

    def is_empty(self):
        if len(self.entries) == 0:
            return True
        return False

    def get_best_exemplar(self):
        return self.entries[0].realisation

    def get_all_exemplars_sorted(self):
        all_realisations_sorted = []
        for entry in self.entries:
            all_realisations_sorted.append(entry.realisation)
        return all_realisations_sorted

    def get_all_ws_sorted(self):
        all_ws_sorted = []
        for entry in self.entries:
            all_ws_sorted.append(entry.non_triviality)
        return all_ws_sorted

    def get_win_quality(self):
        return measure_win_quality(self.get_all_ws_sorted())


