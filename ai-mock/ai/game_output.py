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
    
    d1, d2 = controller.think(0)
    print(direction_to_word(d1) + direction_to_word(d2))
    d1, d2 = controller.think(1)
    print(direction_to_word(d1) + direction_to_word(d2))
    sys.stdout.flush()
    

