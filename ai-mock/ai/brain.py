from ai import *
import copy
import queue

class Brain:
    def __init__(self):
        """
        :type state: State
        """
        self.states = [None, None]
        
    @property
    def state(self):
        return self.states[PLAYER]

    def get_nearest_soul(self, player, ninja_point, field, exceptions):
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
                    if next not in exceptions:
                        return next, step + 1

                search_queue.put((next, step + 1))
                visited.add(next)

        return None, -1

    def get_dist_to_point(self, me, target, field):
        visited = set()
        search_queue = queue.Queue()
        search_queue.put((me, 0))
        visited.add(me)
        if me == target:
            return 0

        while not search_queue.empty():
            point, step = search_queue.get()
            for direction in directions:
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

    def path(self, me, target, field=None, is_avoid_dog = False):
        """
        :type state: State
        :return: Point

        """
        if not field:
            field = self.state.field
        search_queue = queue.Queue()    
        visited = set()
            
        search_queue.put((me, []))
        visited.add(me)
        if me == target:
            return me, []
            
        while not search_queue.empty():
            point, step = search_queue.get()
            for direction in directions:
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


    # def next_dogs(self, ninja1, ninja2): 
    #     state = copy.deepcopy(self.states[PLAYER])




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
        for direction in directions:
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
            debug (next_pos.__repr__(), str(s), ds.__repr__())
            if s > best_score:
                best_score = s
                best_directions = ds
                best_nearest_soul = soul
                best_exceptions = exc


        return best_score, best_directions, best_nearest_soul, best_exceptions


    def simulate(self, ninja_id, state):
        """
        :type state: State
        """
        self.states[ninja_id] = state
        ninja = state.ninjas[ninja_id]
        score, _directions, target_soul, exceptions = self.check_next(ninja_id, state.field, ninja.point, 2,
                                                                      0, [], None, self.states[0].exceptions)
        exceptions.add(target_soul)
        self.states[ninja_id].exceptions = exceptions


        return _directions
    