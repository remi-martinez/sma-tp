from pygame import Vector2

import core


class Heart(object):
    def __init__(self):
        self.size = 5
        self.opacity = 255
        self.position = Vector2(100, 100)

    def show(self):
        if self.size < 40:
            self.size += 5

        self.opacity -= 15
        if self.opacity < 0:
            self.opacity = 0

        core.Draw.text((255, 0, 0, self.opacity), '♥', Vector2(self.position.x - self.size / 2,
                                                               self.position.y - self.size / 2),
                       taille=self.size, font='segoeui')
