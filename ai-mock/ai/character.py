from ai.point import Point

class Character:
    def __init__(self, id, y, x):
        self.point = Point(y, x)

    def __eq__(self, other):
        return self.point == other.point

    def __hash__(self):
        return self.point.__hash__()

    def __repr__(self):
        return self.point.__repr__()