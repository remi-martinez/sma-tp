from pygame import Vector2

import core


class Heart(object):
    def __init__(self, position=Vector2()):
        self.size = 5
        self.opacity = 255
        self.position = position

    def show(self):
        if self.size < 40:
            self.size += 5

        self.opacity -= 10
        if self.opacity < 0:
            self.opacity = 0
            core.memory('hearts').remove(self)

        core.Draw.text((255, 0, 0, self.opacity), '♥', Vector2(self.position.x - self.size / 3,
                                                               self.position.y - self.size / 3),
                       taille=self.size, font='segoeui')
