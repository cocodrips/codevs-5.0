from ai.point import *
import sys

def direction_to_word(point):
    if point == Point(-1, 0):
        return "U"
    if point == Point(0, -1):
        return "L"
    if point == Point(0, 1):
        return "R"
    if point == Point(1, 0):
        return "D"
    return "N"


def main_output(controller):
    skill = controller.skill()
    if skill:
        print(3)
        print(*skill)
    else:
        print(2)
    
    paths = controller.think()
    print(''.join([direction_to_word(d) for d in paths[0]]))
    print(''.join([direction_to_word(d) for d in paths[1]]))
    sys.stdout.flush()
    

