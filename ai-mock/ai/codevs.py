# -*- coding: utf-8 -*-
import enum
import sys
from ai.point import Point
###

PLAYER = 0
ENEMY = 1

INF = 10000000
ROW = 17
COL = 14

debug = lambda *args: sys.stderr.write(" ".join(args) + "\n")
raw_input = lambda: sys.stdin.readline().strip()

class Evaluation:
    DOG_STEP_THRESHOLD = 5
    DOG_DIST_SCORE = lambda dist: -1000 if dist == 0 else -100 / dist
    DOG_DIRECTION_SCORE = lambda dir_num: 0 #-1 * pow(2, dir_num)
    SOUL_GET_SCORE = 100
    DOPPEL_THRESHOLD = 50
    
    @staticmethod
    def SOUL_DIST_SCORE(dist):
        if dist == 0:
            return Evaluation.SOUL_GET_SCORE 
        return Evaluation.SOUL_GET_SCORE / 2 / dist

class Skill(enum.Enum):
    Speed = 0
    DropBlockMe = 1
    DropBlockEnemy = 2
    DeleteBlockMe = 3
    DeleteBlockEnemy = 4
    DoppelMe = 5
    DoppelEnemy = 6
    SendDog = 7


def is_valid_point(p):
    return 0 <= p.y < ROW and 0 <= p.x < COL

def is_inside_field(p):
    return 1 <= p.y < ROW - 1 and 1 <= p.x < COL - 1

def dump_field(field):
    for y in range(ROW):
        for x in range(COL):
            print (str(field[y][x])[:2], end="")
        print ("")
                
                
                