import random
import time

from pygame import Vector2

import core
from fustrum import Fustrum
from heart import Heart


class Body(object):
    def __init__(self):
        self.position = Vector2(random.randint(0, core.WINDOW_SIZE[0]), random.randint(0, core.WINDOW_SIZE[1]))
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.fustrum = Fustrum(100, self)
        self.label = None
        self.type = None

        self.vitesse = Vector2(5, 5)
        self.vitesse_max = 5
        self.acceleration = Vector2()
        self.acceleration_max = 1
        self.taille_body = 10

        self.faim_max = 100
        self.faim_valeur = 0
        self.affame = False

        self.fatigue_max = 100
        self.fatigue_valeur = 0
        self.dort = False

        self.reproduction_max = 100
        self.reproduction_valeur = 0
        self.reproduire = False

        self.date_naissance = time.time()
        self.esperance_vie = 60  # secondes
        self.mort = False
        self.decomposition = 0

    def update(self):
        # Mort
        if self.mort is True:
            self.label = None
            return
        elif self.date_naissance + self.esperance_vie <= time.time():
            self.mort = True
            self.color = (138, 138, 138)

        # Dormir
        if self.dort is True and self.fatigue_valeur > 0:
            self.fatigue_valeur -= 1
            return

        if self.fatigue_valeur >= self.fatigue_max:
            self.dort = True
            self.label = 'Zzz...'
            return
        else:
            self.dort = False
            self.label = None

        # Affamé à partir de 80%
        if self.faim_valeur >= self.faim_max * 0.80:
            self.affame = True
            self.label = 'AFFAMÉ'

        # Affamé à 100% = mort
        if self.faim_valeur >= self.faim_max:
            self.kill()

        # Reproduction
        if self.reproduction_valeur >= self.reproduction_max:
            self.reproduction()
            self.reproduction_valeur = 0
            self.reproduire = True

        # Jauges
        if self.faim_valeur < self.faim_max:
            self.faim_valeur += 1
        if self.fatigue_valeur < self.fatigue_max:
            self.fatigue_valeur += 1
        if self.reproduction_valeur < self.reproduction_max:
            self.reproduction_valeur += 1

        # Déplacements
        if self.acceleration.length() > self.acceleration_max:
            self.acceleration.scale_to_length(self.acceleration_max)

        self.vitesse += self.acceleration
        if self.vitesse.length() > self.vitesse_max:
            self.vitesse.scale_to_length(self.vitesse_max)

        self.acceleration = Vector2(0, 0)
        self.position += self.vitesse
        self.edge()

    def show(self):
        if self.mort is False or self.decomposition > 0:
            core.Draw.text(self.color, self.label, Vector2(self.position.x - 10, self.position.y - 30), taille=15)
        else:
            self.color = (138, 138, 138)
        core.Draw.circle(self.color, self.position, self.taille_body)

    def edge(self):
        if self.position.x <= self.taille_body:
            self.vitesse.x *= -1
        if self.position.x + self.taille_body >= core.WINDOW_SIZE[0]:
            self.vitesse.x *= -1
        if self.position.y <= self.taille_body:
            self.vitesse.y *= -1
        if self.position.y + self.taille_body >= core.WINDOW_SIZE[1]:
            self.vitesse.y *= -1

    def kill(self):
        self.label = None
        self.mort = True

    def reproduction(self):
        cloned_body = type(self)()
        cloned_body.position.x = self.position.x
        cloned_body.position.y = self.position.y

        heart = Heart(Vector2(self.position.x, self.position.y))
        core.memory('hearts').append(heart)

        return cloned_body

    def decomposer(self):
        self.decomposition += 1
        if self.decomposition > 100:
            self.decomposition = 0

