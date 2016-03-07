from ai import *

class Controller:
    def __init__(self):
        self.states = [State(), State()]
        self.brain = Brain()

    def think(self):
        return self.brain.simulate(self.states[0])

    def is_pinch(self, ninja_id):
        ninja = self.states[PLAYER].ninjas[ninja_id]
        state = self.states[PLAYER]
        cnt = 0
        block = None
        for d in Direction.directions:
            p = ninja.point + d
            p2 = p + d
            if p in state.dog_points:
                cnt += 1

            if state.field[p.y][p.x].is_block:
                if is_valid_point(p2) and not state.field[p2.y][p2.x].is_empty:
                    cnt += 1
                    block = p

        if cnt >= 2:
            return block
        return False

    def skill(self):
        for i in range(2):
            p = self.is_pinch(0)
            if p:
                return self.delete_block(p)

        if self.states[PLAYER].power > self.states[PLAYER].skills[3]:
            p = self.states[PLAYER].get_soul_under_block()
            if p:
                return self.delete_block(p)
        return None

    def delete_block(self, p):
        self.states[PLAYER].field[p.y][p.x] = Cell(Cell.EMPTY)
        return (3, p.y, p.x)
