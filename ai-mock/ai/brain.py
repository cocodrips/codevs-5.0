from ai import *
import copy
from queue import PriorityQueue, Queue


class Brain:
    def __init__(self):
        """
        :type state: State
        """
        self.states = [None, None]

    @property
    def state(self):
        return self.states[PLAYER]

    def get_nearest_soul(self, state, ninja_point, exceptions):
        """
        :type state: State
        :return: Point
        """
        field = state.field

        visited = set()
        search_queue = Queue()
        search_queue.put((ninja_point, 0))
        if ninja_point in state.souls:
            return ninja_point, 0

        visited.add(ninja_point)

        while not search_queue.empty():
            point, step = search_queue.get()
            for direction in Direction.directions:
                next = point + direction

                if next in visited:
                    continue
                if not field[next.y][next.x].is_empty or next in state.dog_points:
                    continue

                if next in state.souls:
                    if next not in exceptions:
                        return next, step + 1

                search_queue.put((next, step + 1))
                visited.add(next)

        return None, -1

    def get_dist_to_point(self, me, target, field):
        visited = set()
        search_queue = Queue()
        search_queue.put((me, 0))
        visited.add(me)
        if me == target:
            return 0

        while not search_queue.empty():
            point, step = search_queue.get()
            for direction in Direction.directions:
                next = point + direction
                if next in visited:
                    continue

                if not (0 <= next.y < ROW and 0 <= next.x < COL):
                    continue
                    # print (next) BUG
                if not field[next.y][next.x].is_empty:
                    continue

                if next == target:
                    return step + 1

                search_queue.put((next, step + 1))
                visited.add(next)

        return INF

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


    def check_next(self, ninja_id, _field, current, depth, _score, _directions, nearest_soul, exceptions):
        """
        :type ninja: Character
        :type state: State
        """
        if depth == 0:
            return _score, _directions, nearest_soul, exceptions

        state = self.states[PLAYER]

        base_score = _score
        base_directions = _directions
        base_exceptions = exceptions
        best_exceptions = set()
        best_score = -INF
        best_nearest_soul = None
        best_directions = _directions

        dog_lists = self.get_near_dog_list(state.dog_points, current, _field)
        dog_point = sum(dog_lists)
        nearest_soul, nearest_soul_path = self.get_nearest_soul(PLAYER, current, _field, exceptions)
        for direction in Direction.directions:
            exceptions = base_exceptions
            field = copy.deepcopy(_field)
            score = base_score

            next_pos = current + direction
            next_cell = field[next_pos.y][next_pos.x]

            if next_cell.is_wall:
                continue

            if next_cell.is_block:
                next2_pos = next_pos + direction
                next2_cell = field[next2_pos.y][next2_pos.x]
                if next2_cell.is_empty \
                    and next2_pos != state.ninjas[(ninja_id + 1) % 2].point \
                    and next2_pos not in state.dog_points:

                    # 石がニンジャソウルの上にのる
                    if state.dist_to_soul(next2_pos, exceptions) == 0:
                        score -= 100

                    next2_cell.type = Cell.BLOCK
                    next_cell.type = Cell.EMPTY
                else:
                    continue

            if state.dist_to_dog(next_pos) <= 1:
                if depth > 2:
                    score -= 50
                else:
                    score -= 1000

            new_dog_point = sum(self.get_near_dog_list(state.dog_points, next_pos, _field))
            score += 30 * (dog_point - new_dog_point)
            new_nearest_soul, new_nearest_soul_path = self.get_nearest_soul(PLAYER, next_pos,
                                                                            field, exceptions)
            if new_nearest_soul_path == 0:
                exceptions.add(new_nearest_soul)
                score += 300

            if new_nearest_soul_path < nearest_soul_path:
                score += 10
            else:
                score += 5

            s, ds, soul, exc = self.check_next(ninja_id, field, next_pos, depth - 1, score,
                                               base_directions + [direction], new_nearest_soul, exceptions)
            debug(next_pos.__repr__(), str(s), ds.__repr__())
            if s > best_score:
                best_score = s
                best_directions = ds
                best_nearest_soul = soul
                best_exceptions = exc

        return best_score, best_directions, best_nearest_soul, best_exceptions


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

    def simulate_next_turn(self, _state, step, _score, _dog_score):
        """
        :type _state: State
        """
        best_score = _score
        best_state = _state
        if step == 0:
            return best_score, best_state

        state = copy.deepcopy(_state)

        for n0_direction_1 in Direction.directions:
            if not self.can_move(state, state.ninjas[0].point, n0_direction_1):
                continue
            for n1_direction_1 in Direction.directions:
                if not self.can_move(state, state.ninjas[1].point, n1_direction_1):
                    continue

                next_state = copy.deepcopy(state)

                # ninja0,1の方向決定。移動。
                next_state.ninjas[0].point = self.move(state, next_state.ninjas[0].point, n0_direction_1)
                next_state.ninjas[1].point = self.move(state, next_state.ninjas[1].point, n1_direction_1)

                next_state.steps[0].append(n0_direction_1)
                next_state.steps[1].append(n1_direction_1)
                # 犬判定

                # score
                score = _score

                # 魂にのってるかどうか
                def get_on_soul_score(point, state):
                    if point in next_state.souls:
                        next_state.souls.remove(point)
                        return 100
                    return 0

                score += self.get_on_soul_score(next_state.ninjas[0].point, next_state)
                score += self.get_on_soul_score(next_state.ninjas[1].point, next_state)

                score += self.get_soul_dist_score(0, next_state)
                score += self.get_soul_dist_score(1, next_state)

                if step == 1:
                    score += self.get_dog_score(next_state)

                __score, __state = self.simulate_next_turn(next_state, step - 1, score, _dog_score)
                if best_score < __score:
                    best_score = __score
                    best_state = __state

        return best_score, best_state

    

    def set_next_turn_dog(self, state):
        """
        state: dog_points, dogsが変更される
        """
        steps_from_ninja = state.steps_from_ninja
        
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
        state.steps_from_ninja = steps_from_ninja
        return state

    def get_dog_score(self, state):
        """
        :type state:State
        """
        direction_score = [0, 0, 0, 0] # top, left, right, bottom
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
        
        for direction in Path.relay_points[2][dest_path]: #step
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


    def get_best_destination_score(self, _state):
        """
        :type _state: State 
        :type state: State 
        """
        _state.set_steps_from_ninja()
        # base_soul_point = sum(_state.dist_to_soul()[:2])
        step = 2

        best_score = -INF
        best_paths = []
        for d0 in Path.paths[step]:
            for d1 in Path.paths[step]:
                score = 0
                # 状態を上書きされないようコピー
                state = copy.deepcopy(_state)
                
                state.ninjas[0].point += d0
                state.ninjas[1].point += d1
                if not is_inside_field(state.ninjas[0].point):
                    continue
                if not is_inside_field(state.ninjas[1].point):
                    continue
                    
                state.set_steps_from_ninja()
                self.set_next_turn_dog(state)
                
                score += self.get_dog_score(state)
                
                point0, soul0 = self.try_all_relay_point(state,
                                                          _state.ninjas[0].point, d0)
                if not point0:
                    continue

                point1, soul1 = self.try_all_relay_point(state,
                                                          _state.ninjas[1].point, d1)
                if not point1:
                    continue
                    
                souls = {soul0, soul1}
                souls.remove(None)
                
                score += len(list(souls)) * Evaluation.SOUL_GET_SCORE
                dist_to_soul = state.dist_to_soul(souls)
                for dist in dist_to_soul[:4]:
                    score += Evaluation.SOUL_DIST_SCORE(dist)

                # print (score, [point0, d0-point0], [point1, d1-point1]) 
                if best_score < score:
                    best_score = score
                    best_paths = [[point0, d0-point0], [point1, d1-point1]]
        # print (best_score)
        return best_paths

    def simulate(self, state):
        """
        :type state: State
        """
        return self.get_best_destination_score(state)