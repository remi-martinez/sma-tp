import math

from pygame import Vector2

import core
from agents.decomposeur import Decomposeur
from bodies.body import Body


class DecomposeurBody(Body):
    def __init__(self):
        super().__init__()
        self.type = 'Decomposeur'
        self.fatigue_max = 99999999999
        self.reproduction_max = 99999999999
        self.faim_max = 99999999999

    def update(self):
        super().update()

    def show(self):
        a = 0 - self.vitesse.angle_to(Vector2(0, 1))

        p1 = self.position + Vector2(-5, 0).rotate(a)
        p2 = self.position + Vector2(0, 15).rotate(a)
        p3 = self.position + Vector2(5, 0).rotate(a)

        core.Draw.polygon(self.color, (p1, p2, p3))

    def reproduction(self):
        cloned_body = super().reproduction()
        core.memory('agents').append(Decomposeur(cloned_body))
