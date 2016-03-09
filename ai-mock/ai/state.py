from queue import PriorityQueue

from ai import *

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
        self.steps = [[],[]]
        self.steps_from_ninja = []

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
        
    def dist_to_ninjas(self, point):
        return set([ninja.point.dist(point) for ninja in self.ninjas])

    def dist_to_soul(self, exceptions):
        if not self.steps_from_ninja:
            return []
        souls_dist = []
        for soul in self.souls:
            if not self.field[soul.y][soul.x].is_empty:
                continue
            if soul in exceptions:
                continue
            souls_dist.append(self.steps_from_ninja[soul.y][soul.x])
        return sorted(souls_dist)

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
    
    def dump_field(self):
        for r in range(ROW):
            for c in range(COL):
                w = ' '
                if self.field[r][c].is_wall:
                    w = 'W'
                if self.field[r][c].is_block:
                    w = 'O'
                if Point(r, c) in self.dog_points:
                    w = 'X'
                if Point(r, c) == self.ninjas[0].point:
                    w = '1'
                if Point(r, c) == self.ninjas[1].point:
                    w = '2'
                print (w, end="")
            print ("")
            
    def set_steps_from_ninja(self):
        class NinjaPoint:
            """
            PriorityQueueに入れる用
            """
        
            def __init__(self, dist, point):
                self.step = dist
                self.point = point
        
            def __lt__(self, other):
                if self.step == other.step:
                    return self.point < other.point
                return self.step < other.step
            
        steps_from_ninja = [[INF for _ in range(COL)] for _ in range(ROW)]
        visited = set()

        queue = PriorityQueue()

        queue.put(NinjaPoint(0, self.ninjas[0].point))
        visited.add(self.ninjas[0].point)

        queue.put(NinjaPoint(0, self.ninjas[1].point))
        visited.add(self.ninjas[1].point)

        while not queue.empty():
            q = queue.get()
            steps_from_ninja[q.point.y][q.point.x] = q.step

            for direction in Direction.directions:
                point = q.point + direction
                if not self.field[point.y][point.x].is_empty:
                    continue

                if point not in visited:
                    visited.add(point)
                    queue.put(NinjaPoint(q.step + 1, point))
        
        self.steps_from_ninja = steps_from_ninja