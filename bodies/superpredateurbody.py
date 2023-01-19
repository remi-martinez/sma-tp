import core
import random
from agents.superpredateur import SuperPredateur
from bodies.body import Body

from utils import parametre_aleatoire

class SuperPredateurBody(Body):
    def __init__(self):
        super().__init__()
        self.type = 'SuperPredateur'
        self.vitesse_max = parametre_aleatoire(self.type, 'vitesseMax') or self.vitesse_max
        self.acceleration_max = parametre_aleatoire(self.type, 'accelerationMax') or self.acceleration_max
        self.faim_max = parametre_aleatoire(self.type, 'faimMax') or self.faim_max
        self.reproduction_max = parametre_aleatoire(self.type, 'reproductionMax') or self.reproduction_max
        self.esperance_vie = parametre_aleatoire(self.type, 'esperanceMax') or self.esperance_vie

    def update(self):
        super().update()

    def reproduction(self):
        cloned_body = super().reproduction()
        core.memory('agents').append(SuperPredateur(cloned_body))
