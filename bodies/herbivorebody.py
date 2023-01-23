import core
from agents.herbivore import Herbivore
from bodies.body import Body

from utils import parametre_aleatoire


class HerbivoreBody(Body):
    def __init__(self):
        super().__init__()
        self.type = 'Herbivore'
        self.vitesse_max = parametre_aleatoire(self.type, 'vitesseMax') or self.vitesse_max
        self.acceleration_max = parametre_aleatoire(self.type, 'accelerationMax') or self.acceleration_max
        self.faim_max = parametre_aleatoire(self.type, 'faimMax') or self.faim_max
        self.reproduction_max = parametre_aleatoire(self.type, 'reproductionMax') or self.reproduction_max
        self.esperance_vie = parametre_aleatoire(self.type, 'esperanceMax') or self.esperance_vie

    def update(self):
        super().update()

    def reproduction(self):
        cloned_body = super().reproduction()
        core.memory('agents').append(Herbivore(cloned_body))

    def manger(self, other_body):
        if other_body.type == 'Vegetal':
            super().manger(other_body)
