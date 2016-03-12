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
        self.steps = [[], []]
        self.doppelganger = None
        self._prev_ninjas = None
        self._steps_from_ninja = None
        self._steps_from_doppelganger = None
        self._prev_doppel_point = None

    @property
    def steps_from_ninja(self):
        """
        忍者から各マスへの最短経路
        """
        ninjas_hash = hash(self.ninjas[0]) + hash(self.ninjas[1]) * 2
        if (not self._prev_ninjas or 
                ninjas_hash != self._prev_ninjas):
            self._prev_ninjas = ninjas_hash
            self._steps_from_ninja = self.steps_from_points([
                self.ninjas[0].point,
                self.ninjas[1].point
            ])
        return self._steps_from_ninja
    
    @property
    def steps_from_doppelganger(self):
        """
        影武者から各マスへの距離
        """
        if not self.doppelganger:
            return self.steps_from_ninja
        if not self._prev_doppel_point or self._prev_doppel_point != self.doppelganger:
            self._prev_doppel_point = self.doppelganger
            self._steps_from_doppelganger = self.steps_from_points([self.doppelganger])
        return self._steps_from_doppelganger
            

    def start(self):
        self.clear_dog()
        self.clear_soul()
        self.doppelganger = None
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

    def get_soul_under_block(self):
        for soul in self.souls:
            if self.field[soul.y][soul.x].is_block:
                return soul

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
                print(w, end="")
            print("")

    def steps_from_points(self, points):
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

        steps_from_points = [[INF for _ in range(COL)] for _ in range(ROW)]
        visited = set()

        queue = PriorityQueue()
        for point in points:
            queue.put(NinjaPoint(0, point))
            visited.add(point)

        while not queue.empty():
            q = queue.get()
            steps_from_points[q.point.y][q.point.x] = q.step

            for direction in Direction.directions:
                point = q.point + direction
                if not self.field[point.y][point.x].is_empty:
                    continue

                if point not in visited:
                    visited.add(point)
                    queue.put(NinjaPoint(q.step + 1, point))

        return steps_from_points