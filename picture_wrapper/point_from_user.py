from .pic import Pic

def get_point_from_user(pic):
    data = pic.select_in_hand_mode_without_radiuses()
    return data.points[0]

def get_point_and_radius_from_user(pic):
    data = pic.select_in_hand_mode_with_radiuses()
    return data.points[0], data.radiuses[0]