# -*- coding: utf-8 -*-
import copy
import sys
import queue

raw_input = lambda: sys.stdin.readline().strip()
debug = lambda *args: sys.stderr.write(" ".join(args) + "\n")

PLAYER = 0
ENEMY = 1

INF = 10000000


class Cell:
    EMPTY = '_'
    BLOCK = 'O'
    WALL = 'W'

    def __init__(self, c):
        self.type = c

    @property
    def is_wall(self):
        return self.type == Cell.WALL

    @property
    def is_block(self):
        return self.type == Cell.BLOCK

    @property
    def is_empty(self):
        return self.type == Cell.EMPTY


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


class Character:
    def __init__(self, id, y, x):
        self.point = Point(y, x)

    def __eq__(self, other):
        return self.point == other.point

    def __hash__(self):
        return self.point.__hash__()

    def __repr__(self):
        return self.point.__repr__()


directions = [Point(-1, 0), Point(0, -1), Point(0, 1), Point(1, 0), Point(0, 0)]


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


Moves = [Point(-1, 0), Point(0, -1), Point(0, 1), Point(1, 0),
         Point(-2, 0), Point(0, -2), Point(0, 2), Point(2, 0),
         Point(-1, -1), Point(1, -1), Point(-1, 1), Point(1, 1)]


class Brain:
    def __init__(self):
        self.states = [None, None]

    def get_nearest_soul(self, player, ninja_point, field):
        """
        :type state: State
        :return: Point
        """
        state = self.states[PLAYER]

        visited = set()
        search_queue = queue.Queue()
        search_queue.put((ninja_point, 0))
        if ninja_point in state.souls:
            return ninja_point, 0

        visited.add(ninja_point)

        while not search_queue.empty():
            point, step = search_queue.get()
            for direction in directions:
                next = point + direction
                if next in visited:
                    continue
                if not field[next.y][next.x].is_empty or next in state.dog_points:
                    continue

                if next in state.souls:
                    return next, step + 1

                search_queue.put((next, step + 1))
                visited.add(next)

        return None, -1


    def checkNext(self, ninja_id, _field, current, depth, _score, _directions, exceptions):
        """
        :type ninja: Character
        :type state: State
        """
        if depth == 0:
            return _score, _directions

        state = self.states[PLAYER]

        base_score = _score
        base_directions = _directions
        best_score = -INF
        best_directions = _directions

        nearest_soul, nearest_soul_path = self.get_nearest_soul(PLAYER, current, _field)
        for direction in directions:
            field = copy.deepcopy(_field)
            score = base_score

            next_pos = current + direction
            next_cell = field[next_pos.y][next_pos.x]

            if next_cell.is_wall:
                continue

            if next_cell.is_block:
                next2_pos = next_pos + direction
                next2_cell = field[next2_pos.y][next2_pos.x]
                if next2_cell.is_empty:
                    # 石がニンジャソウルの上にのる
                    if state.dist_to_soul(next2_pos, exceptions) == 0:
                        score -= 100

                    next_cell.type = Cell.BLOCK
                    next_cell.type = Cell.EMPTY
                else:
                    continue

            if state.dist_to_dog(next_pos) == 1:
                score -= 1000

            new_nearest_soul, new_nearest_soul_path = self.get_nearest_soul(PLAYER, next_pos, field)
            if new_nearest_soul_path == 0:
                score += 100

            if new_nearest_soul_path < nearest_soul_path:
                score += 10

            s, ds = self.checkNext(ninja_id, field, next_pos, depth - 1, score, base_directions + [direction],
                                   exceptions)
            if s > best_score:
                best_score = s
                best_directions = ds

        return best_score, best_directions


    def simulate(self, ninja_id, state):
        """
        :type state: State
        """
        self.states[ninja_id] = state
        ninja = state.ninjas[ninja_id]
        score, _directions = self.checkNext(ninja_id, state.field, ninja.point, 2, 0, [], [])
        return _directions


class State:
    def __init__(self):
        self.field = []
        self.ninjas = [None, None]
        self.dogs = {}
        self.dog_points = set()
        self.power = 0
        self.souls = set()
        self.skills = []

    def set_field(self, field):
        self.field = field

    def set_ninja(self, i, y, x):
        self.ninjas[i] = Character(i, y, x)

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


class Controller:
    def __init__(self):
        self.states = [State(), State()]
        self.brain = Brain()

    def think(self, ninja_id):
        return self.brain.simulate(ninja_id, self.states[0])

    def skill(self):
        if self.states[PLAYER].power > self.states[PLAYER].skills[7]:
            if self.states[PLAYER].dist_to_dog(self.states[PLAYER].ninjas[0].point) == 1:
                return (7, 0)
            if self.states[PLAYER].dist_to_dog(self.states[PLAYER].ninjas[1].point) == 1:
                return (7, 1)


class AI:
    def __init__(self, name):
        self.name = name
        self.controller = Controller()

    def player_input(self, i):
        state = self.controller.states[i]

        state.power = int(raw_input())
        row, col = map(int, raw_input().split(" "))

        field = [[None for _ in range(col)] for _ in range(row)]
        for r in range(row):
            for c, character in enumerate(raw_input()):
                field[r][c] = Cell(character)
        state.set_field(field)

        ninja_num = int(raw_input())
        for i in range(ninja_num):
            i, y, x = map(int, raw_input().split(" "))
            state.set_ninja(i, y, x)

        dog_num = int(raw_input())
        for i in range(dog_num):
            i, y, x = map(int, raw_input().split(" "))
            state.set_dog(i, y, x)

        state.clear_soul()
        soul = int(raw_input())
        for i in range(soul):
            y, x = map(int, raw_input().split(" "))
            state.set_soul(y, x)

        magics = raw_input()

    def think(self):
        print(self.name)
        sys.stdout.flush()

        while 1:
            self.timelimit = raw_input()
            # print (self.timelimit)
            # 
            # # スキルの定義
            _skill_num = raw_input()
            # self.skills = []
            skills = []
            for _id, _cost in enumerate(raw_input().split(" ")):
                skills.append(int(_cost))
            self.controller.states[PLAYER].set_skills(skills)

            debug("player")
            self.player_input(0)
            debug("rival")
            self.player_input(1)

            skill = self.controller.skill()
            if skill:
                print(3)
                print(*skill)
            print(2)
            d1, d2 = self.controller.think(0)
            print(direction_to_word(d1) + direction_to_word(d2))
            d1, d2 = self.controller.think(1)
            print(direction_to_word(d1) + direction_to_word(d2))
            sys.stdout.flush()


# 起動
ai = AI("SampleAI.py")
ai.think()
