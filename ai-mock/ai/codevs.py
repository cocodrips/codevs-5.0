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
    return 0 <= p.y < COL and 0 <= p.x < ROW