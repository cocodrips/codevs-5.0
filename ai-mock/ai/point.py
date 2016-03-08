# -*- coding: utf-8 -*-


class Point:
    def __init__(self, y, x):
        self.y = int(y)
        self.x = int(x)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return self.x + 1000 * self.y

    def __add__(self, other):
        return Point(self.y + other.y, self.x + other.x)

    def __repr__(self):
        arrows = {
            Point(-1, 0): "^",
            Point(0, -1): "<",
            Point(0, 1): ">",
            Point(1, 0): "v",
            Point(0, 0): " ",
        }
        if self in arrows:
            return arrows[self]
        
        return "P({}, {})".format(self.y, self.x)
    
    def __lt__(self, other):
        if self.y == other.y:
            return self.x < other.x
        return self.y < other.y

    def dist(self, other):
        return abs(self.y - other.y) + abs(self.x - other.x)
