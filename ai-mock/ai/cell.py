# -*- coding: utf-8 -*-

class Cell:
    EMPTY = '_'
    BLOCK = 'O'
    WALL = 'W'

    def __init__(self, c):
        self.type = c

    def __repr__(self):
        return self.type

    @property
    def is_wall(self):
        return self.type == Cell.WALL

    @property
    def is_block(self):
        return self.type == Cell.BLOCK

    @property
    def is_empty(self):
        return self.type == Cell.EMPTY
