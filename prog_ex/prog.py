class Event:
    def __init__(self, point, cloud_rad, vet, err_rad):
        self.point = point
        self.cloud_rad = cloud_rad
        self.err_rad = err_rad
        self.vet = vet

class Program:
    def __init__(self):
        self.events = {}  # {id: Event}
        self.order = [] # [id_1, ..., id_n]
        self.child_to_parent = {}  # {child_id: parent_id}


    def add_event(self, event, parent_id):
        pass

    def predict(self, exemplar):
        pass

class Exemplar:
    def __init__(self):
        self.events_to_points = {} # {id: point}



# загрузить программу из файла через easygui
def load_program():
    return program

def load_program_by_name(file_name):
    return program

