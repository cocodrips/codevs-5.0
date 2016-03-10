from ai import *
import copy
from queue import PriorityQueue, Queue


class Brain:
    def __init__(self):
        """
        :type state: State
        """
        self.states = [None, None]


    def get_near_dog_list(self, dog_points, player_point, field):
        dists = []
        for dog in dog_points:
            if player_point.dist(dog) > 3:
                continue
            dist = self.get_dist_to_point(dog, player_point, field)
            if dist <= 3:
                dists.append(dist)

        return dists

    def path(self, me, target, field=None, is_avoid_dog=False):
        """
        :type state: State
        :return: Point

        """
        if not field:
            field = self.state.field
        search_queue = Queue()
        visited = set()

        search_queue.put((me, []))
        visited.add(me)
        if me == target:
            return me, []

        while not search_queue.empty():
            point, step = search_queue.get()
            for direction in Direction.directions:
                next = point + direction

                if next in visited:
                    continue

                if not field[next.y][next.x].is_empty:
                    continue

                if next == target:
                    return next, step

                step.append(next)
                search_queue.put((next, step))

                visited.add(next)

        return None


    def can_move(self, state, me, direction, can_move_block=True):
        """
        :type state: model.State 
        :type cell: Cell
        :type next_block_cell: Cell
        """
        next_pos = me + direction
        cell = state.field[next_pos.y][next_pos.x]
        if cell.is_wall:
            return False

        if cell.is_block:
            if not can_move_block:
                return False

            next_block_pos = next_pos + direction
            next_block_cell = state.field[next_block_pos.y][next_block_pos.x]
            if not next_block_cell.is_empty:
                return False
            if 0 in state.dist_to_ninjas(next_block_pos):
                return False

            # 犬がいるときもだめ
            next_block_cell.type = Cell.BLOCK
            cell.type = Cell.EMPTY

        return True

    def move(self, state, me, direction):
        next_pos = me + direction
        cell = state.field[next_pos.y][next_pos.x]
        if (cell.is_block):
            next_block_pos = next_pos + direction
            next_block_cell = state.field[next_block_pos.y][next_block_pos.x]

            next_block_cell.type = Cell.BLOCK
            cell.type = Cell.EMPTY
        return next_pos


    # 次の魂への距離
    def get_soul_dist_score(self, pos, state):
        soul, dist = self.get_nearest_soul(state, pos, [])
        return (100 / dist)

    def get_on_soul_score(self, point, state, change_state=False):
        if point in state.souls:
            if change_state:
                state.souls.remove(point)
            return 100
        return 0

    def get_dog_score(self, ninja_id, state):
        score = 0
        dogs = self.get_near_dog_list(state.dogs, state.ninjas[ninja_id].point, state.field)
        score -= sum([3 - dog for dog in dogs]) * 50
        for dog in dogs:
            if dog < 2:
                score -= 10000

        return score


    def get_destination_score(self, _state, step, ninja_pos, ninja_id):
        destinations = []
        for d in Path.paths[step]:
            p = ninja_pos + d
            if not is_valid_point(p):
                continue
            if _state.field[p.y][p.x].is_wall:
                continue

            dog_score = self.get_dog_score(ninja_id, _state)
            soul_score = self.get_soul_dist_score(ninja_pos, _state)
            relay_soul_score = max([self.get_on_soul_score(point, _state) for point in Path.relay_points[step][d]])
            destinations.append((dog_score + soul_score + relay_soul_score, d))

        return sorted(destinations, reverse=True)


    def set_next_turn_dog(self, state):
        """
        :type state:State dog_points, dogsが変更される
        """
        steps_from_ninja = state.steps_from_ninja
        if state.doppelganger:
            steps_from_ninja = state.steps_from_doppelganger
            
        new_dogs = {}
        new_dog_points = set()

        for dog in state.dogs.values():
            new_dog = copy.deepcopy(dog)
            best_direction = Direction.directions[4]
            best_step = INF
            for direction in Direction.directions:
                point = dog.point + direction
                step = steps_from_ninja[point.y][point.x]
                if point in new_dog_points:
                    continue
                if step < best_step:
                    best_direction = direction
                    best_step = step

            new_dog.point += best_direction
            new_dog_points.add(new_dog.point)
            new_dogs[new_dog.point] = new_dog

        state.dogs = new_dogs
        state.dog_points = new_dog_points
        return state

    def get_dog_score(self, state):
        """
        :type state:State
        """
        direction_score = [0, 0, 0, 0]  # top, left, right, bottom
        score = 0
        for dog in state.dog_points:
            step = state.steps_from_ninja[dog.y][dog.x]
            if step > Evaluation.DOG_STEP_THRESHOLD:
                continue
            score += Evaluation.DOG_DIST_SCORE(step)
            direction_score[0] += dog.y if dog.y > 0 else 0
            direction_score[1] += dog.x if dog.y > 0 else 0
            direction_score[2] += dog.x if dog.y < 0 else 0
            direction_score[3] += dog.y if dog.y < 0 else 0
        score += Evaluation.DOG_DIRECTION_SCORE(len([d for d in direction_score if d > 0]))
        return score


    def try_all_relay_point(self, state, me, dest_path):
        _field = copy.deepcopy(state.field)
        best_score = -INF
        best_relay_point = None
        best_soul_point = None

        for direction in Path.relay_points[2][dest_path]:  # step
            state.field = copy.deepcopy(_field)
            score = 0
            soul_point = None
            if not self.can_move(state, me, direction):
                continue
            me = self.move(state, me, direction)
            if me in state.souls:
                soul_point = me

            next_direction = dest_path - direction
            if not self.can_move(state, me, next_direction):
                continue

            # 目的の場所に行くことが可能
            if best_score < score:
                best_score = score
                best_relay_point = direction
                best_soul_point = soul_point

        return best_relay_point, best_soul_point

    def doppelganger(self, _state):
        # ALL pattern
        if _state.power < _state.skills[Skill.DoppelMe.value]:
            return None

        state = copy.deepcopy(_state)
        state.doppelganger = None
        _dog_score = self.get_dog_score(state)

        best_dog_score = -INF
        best_doppel_point = None

        # 忍者からの距離を保存
        for y in range(ROW)[:-1]:
            for x in range(COL):
                if not state.field[y][x].is_empty:
                    continue
                state.doppelganger = Point(y, x)

                # 影分身へ向かって犬が移動
                self.set_next_turn_dog(state)
                dog_score = self.get_dog_score(state)

                if best_dog_score < dog_score:
                    best_dog_score = dog_score
                    best_doppel_point = Point(y, x)
                    return best_doppel_point  # TODO : DELETE test

        if (best_dog_score - _dog_score) > Evaluation.DOG_STEP_THRESHOLD:
            _state.power -= _state.skills[Skill.DoppelMe.value]
            return best_doppel_point

        return None


    def get_best_destination_score(self, _state):
        """
        :type _state: State 
        :type state: State 
        """
        cache = _state.steps_from_doppelganger
        
        # _state.set_steps_from_ninja(doppel_point)
        # base_soul_point = sum(_state.dist_to_soul()[:2])
        step = 2

        best_score = -INF
        best_paths = []
        for d0 in Path.paths[step]:
            for d1 in Path.paths[step]:
                score = 0
                # 状態を上書きされないようコピー
                state = copy.deepcopy(_state)

                # 忍者を移動済みにする
                state.ninjas[0].point += d0
                state.ninjas[1].point += d1
                if not is_inside_field(state.ninjas[0].point):
                    continue
                if not is_inside_field(state.ninjas[1].point):
                    continue

                point0, soul0 = self.try_all_relay_point(state,
                                                         _state.ninjas[0].point, d0)
                if not point0:
                    continue

                point1, soul1 = self.try_all_relay_point(state,
                                                         _state.ninjas[1].point, d1)
                if not point1:
                    continue

                # 忍者の位置からのソウルポイント
                souls = {soul0, soul1}
                if None in souls:
                    souls.remove(None)

                soul_point = 0
                soul_point += len(list(souls)) * Evaluation.SOUL_GET_SCORE
                dist_to_soul = state.dist_to_soul(souls)
                for dist in dist_to_soul[:4]:
                    soul_point += Evaluation.SOUL_DIST_SCORE(dist)

                score += soul_point

                # 犬を移動させる
                self.set_next_turn_dog(state)

                # Doppel合ってもなくてもここから下はいっしょ
                dog_point = self.get_dog_score(state)
                score += dog_point


                print(int(score), "\t", int(soul_point), "\t",
                      int(dog_point), [point0, d0 - point0], [point1, d1 - point1], dist_to_soul)
                if best_score < score:
                    best_score = score
                    best_paths = [[point0, d0 - point0], [point1, d1 - point1]]
        # print (best_score)
        return best_paths

    def simulate(self, state):
        """
        :type state: State
        """
        dog_point = self.get_dog_score(state)
        if dog_point < -200: 
            state.doppelganger = state.ninjas[0].point
        
        skill = None
        if state.doppelganger:
            skill = (Skill.DoppelMe.value, state.doppelganger.y, state.doppelganger.x)
        return skill, self.get_best_destination_score(state)