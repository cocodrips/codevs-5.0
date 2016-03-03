# -*- coding: utf-8 -*-
from ai import *

class AI:
    def __init__(self, name):
        self.name = name
        self.controller = Controller()

    def think(self):
        print(self.name)
        sys.stdout.flush()

        while 1:
            main_input(self.controller)
            main_output(self.controller)

ai = AI("cocodrips")
ai.think()
