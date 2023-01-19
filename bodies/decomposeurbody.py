from pygame import Vector2

import core
from agents.decomposeur import Decomposeur
from bodies.body import Body

from utils import parametre_aleatoire

class DecomposeurBody(Body):
    def __init__(self):
        super().__init__()
        self.type = 'Decomposeur'
        self.vitesse_max = parametre_aleatoire(self.type, 'vitesseMax') or self.vitesse_max
        self.acceleration_max = parametre_aleatoire(self.type, 'accelerationMax') or self.acceleration_max
        self.faim_max = parametre_aleatoire(self.type, 'faimMax') or self.faim_max
        self.reproduction_max = parametre_aleatoire(self.type, 'reproductionMax') or self.reproduction_max
        self.esperance_vie = parametre_aleatoire(self.type, 'esperanceMax') or self.esperance_vie

    def update(self):
        super().update()

    def show(self):
        super().show_text()
        a = 0 - self.vitesse.angle_to(Vector2(0, 1))

        p1 = self.position + Vector2(-5, 0).rotate(a)
        p2 = self.position + Vector2(0, 15).rotate(a)
        p3 = self.position + Vector2(5, 0).rotate(a)

        core.Draw.polygon(self.color, (p1, p2, p3))

    def reproduction(self):
        cloned_body = super().reproduction()
        core.memory('agents').append(Decomposeur(cloned_body))
