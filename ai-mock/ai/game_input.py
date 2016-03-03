from ai import *

def main_input(controller):
    """
    :type controller: Controller
    """
    timelimit = raw_input()
    # print (self.timelimit)
    # 
    # # スキルの定義
    _skill_num = raw_input()
    # self.skills = []
    skills = []
    for _id, _cost in enumerate(raw_input().split(" ")):
        skills.append(int(_cost))
    controller.states[PLAYER].set_skills(skills)

    debug("player")
    player_input(controller, 0)
    debug("rival")
    player_input(controller, 1)
    

def player_input(controller, ninja_id):
    """
    :type controller: Controller
    """
    state = controller.states[ninja_id]
    state.start()

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
    # state.clear_dog()
    for i in range(dog_num):
        i, y, x = map(int, raw_input().split(" "))
        state.set_dog(i, y, x)

    # state.clear_soul()
    soul = int(raw_input())
    for i in range(soul):
        y, x = map(int, raw_input().split(" "))
        state.set_soul(y, x)

    magics = raw_input()