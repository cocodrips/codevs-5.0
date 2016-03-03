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
        return "P({}, {})".format(self.y, self.x)

    def dist(self, other):
        return abs(self.y - other.y) + abs(self.x - other.x)
