from ai import Point, Character

class State:
    def __init__(self):
        self.field = []
        self.ninjas = [None, None]
        self.dogs = {}
        self.dog_points = set()
        self.power = 0
        self.souls = set()
        self.skills = []
        self.exceptions = set()

    def start(self):
        self.clear_dog()
        self.clear_soul()
        self.exceptions = set()

    def set_field(self, field):
        self.field = field

    def set_ninja(self, i, y, x):
        self.ninjas[i] = Character(i, y, x)

    def clear_dog(self):
        self.dogs = {}
        self.dog_points = set()

    def set_dog(self, i, y, x):
        self.dogs[Point(y, x)] = Character(i, y, x)
        self.dog_points.add(Point(y, x))

    def clear_soul(self):
        self.souls = set()

    def set_soul(self, y, x):
        self.souls.add(Point(y, x))

    def set_skills(self, skills):
        self.skills = skills

    def dist_to_soul(self, point, exceptions):
        return min([point.dist(s) for s in self.souls
                    if s not in exceptions and self.field[s.y][s.x].is_empty])

    def dist_to_dog(self, point):
        if not self.dog_points:
            return 100
        return min([point.dist(dog_point) for dog_point in self.dog_points])

    def get_soul_under_block(self):
        for soul in self.souls:
            if self.field[soul.y][soul.x].is_block:
                return soul

    def get_nearest_block(self, point):
        for i in range(1, 17):
            for r in range(-i, i):
                for c in range(-i, i):
                    if 0 < point.y + r < len(self.field) and 0 < point.x + c < len(self.field[0]):
                        if self.field[point.y + r][point.x + c].is_block:
                            return Point(point.y + r, point.x + c)
        return None