import math

from pygame import Vector2

import core
from bodies.body import Body


class DecomposeurBody(Body):
    def __init__(self):
        super().__init__()
        self.fatigue_max = 99999999999

    def update(self):
        super().update()

    def show(self):
        a = 0 - self.vitesse.angle_to(Vector2(0, 1))

        p1 = self.position + Vector2(-5, 0).rotate(a)
        p2 = self.position + Vector2(0, 15).rotate(a)
        p3 = self.position + Vector2(5, 0).rotate(a)

        core.Draw.polygon(self.color, ((p1), (p2), (p3)))
