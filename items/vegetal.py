import random
import core

from pygame import Vector2


class Vegetal:
    def __init__(self):
        self.position = Vector2(random.randint(0, core.WINDOW_SIZE[0]), random.randint(0, core.WINDOW_SIZE[1]))
        self.type = 'Vegetal'
        self.color = (0, 255, 0)
        self.mort = False

    def show(self):
        if self.mort is True:
            self.color = (138, 138, 138)

        core.Draw.circle(self.color, self.position, 5)
