from prog_ex import Program, Event
from .w_eval_1px import WEval1px

class ProgramWDistrs:
    def __init__(self, pic, program):
        self.pic = pic
        self.program = program
        self.ids_to_distrs = {} # event_id: w_distr
        self.evaluator = WEval1px(self.pic)

    def fill(self):
        for event_id, event in self.program.events.items():
            vet = event.vet
            w_distr = self.evaluator.get_w_distr(vet=vet)
            self.ids_to_distrs[event_id] = w_distr

    def get_w_distr_for_event(self, event_id):
        return self.ids_to_distrs[event_id]