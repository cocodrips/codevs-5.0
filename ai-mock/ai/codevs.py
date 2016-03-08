# -*- coding: utf-8 -*-

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

def is_valid_point(p):
    return 0 <= p.y < ROW and 0 <= p.x < COL

def dump_field(field):
    for y in range(ROW):
        for x in range(COL):
            print (str(field[y][x])[:2], end="")
        print ("")
                