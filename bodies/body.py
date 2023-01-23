import random
import time

from numpy import average
from pygame import Vector2

import core
from fustrum import Fustrum
from heart import Heart


class Body(object):
    def __init__(self):
        self.taille_body = 10
        self.position = Vector2(random.randint(0 + self.taille_body, core.WINDOW_SIZE[0] - self.taille_body),
                                random.randint(0 + self.taille_body, core.WINDOW_SIZE[1] - self.taille_body))
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.fustrum = Fustrum(100, self)
        self.label = None
        self.type = None
        self.selection = False

        self.vitesse = Vector2(5, 5)
        self.vitesse_max = 5
        self.acceleration = Vector2()
        self.acceleration_max = 1

        self.valeur_nutritive = 30
        self.faim_max = 100
        self.faim_valeur = 0
        self.affame = False

        self.fatigue_max = 100
        self.fatigue_valeur = 0
        self.dort = False

        self.reproduction_max = 100
        self.reproduction_valeur = 0

        self.date_naissance = time.time()
        self.esperance_vie = 60  # secondes
        self.mort = False
        self.decomposition = 0

    def update(self):
        # Mort
        if self.mort is True:
            self.label = None
            self.color = (138, 138, 138)
            return
        elif self.date_naissance + self.esperance_vie <= time.time():
            self.meurt()

        # Dormir
        if self.dort is True and self.fatigue_valeur > 0:
            self.label = 'Zzz...'
            self.fatigue_valeur -= 0.01 * self.fatigue_max  # Le body perd 10% de fatigue par frame quand il dort
            return

        if self.fatigue_valeur >= self.fatigue_max:
            self.dort = True
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
            self.meurt()

        # Empêcher que la jauge de faim ne tombe en dessous de zéro
        if self.faim_valeur <= 0:
            self.faim_valeur = 0

        # Reproduction
        if self.reproduction_valeur >= self.reproduction_max:
            self.reproduction()
            self.reproduction_valeur = 0

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
        if self.mort is True:
            self.color = (138, 138, 138)

        if self.selection is True:
            self.show_hud()
            core.Draw.circle((255, 255, 255), self.position, self.taille_body + 1, width=1)

        self.show_text()
        core.Draw.circle(self.color, self.position, self.taille_body)

    def show_hud(self):
        pos = self.position

        faim = self.faim_valeur / self.faim_max
        core.Draw.text((255, 255, 255), '🍴', Vector2(pos.x - 40, pos.y + 10), taille=10, font='segoeuiemoji')
        core.Draw.rect((255, 255, 255), (pos.x - 25, pos.y + 15, 50, 6), width=1)
        core.Draw.rect(get_couleur(faim), (pos.x - 24, pos.y + 16, abs(faim * 50), 4), width=0)

        fatigue = self.fatigue_valeur / self.fatigue_max
        core.Draw.text((255, 255, 255), '💤', Vector2(pos.x - 40, pos.y + 28), taille=10, font='segoeuiemoji')
        core.Draw.rect((255, 255, 255), (pos.x - 25, pos.y + 30, 50, 6), width=1)
        core.Draw.rect(get_couleur(fatigue), (pos.x - 24, pos.y + 31, abs(fatigue * 50), 4), width=0)

        reproduction = self.reproduction_valeur / self.reproduction_max
        core.Draw.text((255, 255, 255), '♥', Vector2(pos.x - 40, pos.y + 46), taille=10, font='segoeuiemoji')
        core.Draw.rect((255, 255, 255), (pos.x - 25, pos.y + 45, 50, 6), width=1)
        core.Draw.rect(get_couleur(reproduction), (pos.x - 24, pos.y + 46, abs(reproduction * 50), 4), width=0)

    def show_text(self):
        if self.mort is False or self.decomposition > 0:
            core.Draw.text(self.color, self.label, Vector2(self.position.x - 15, self.position.y - 30), taille=15)

    def edge(self):
        borders = [Vector2(0, self.position.y),
                   Vector2(core.WINDOW_SIZE[0], self.position.y),
                   Vector2(self.position.x, core.WINDOW_SIZE[1]),
                   Vector2(self.position.x, 0)]

        # Pour fuir les bords
        for edge_position in borders:
            if edge_position.distance_to(self.position) < self.fustrum.radius / 2:
                self.acceleration = self.position - edge_position

        # Pour revenir si le body sort de la fenêtre
        if self.position.x <= self.taille_body:
            self.vitesse.x *= -1
        if self.position.x + self.taille_body >= core.WINDOW_SIZE[0]:
            self.vitesse.x *= -1
        if self.position.y <= self.taille_body:
            self.vitesse.y *= -1
        if self.position.y + self.taille_body >= core.WINDOW_SIZE[1]:
            self.vitesse.y *= -1

    def meurt(self):
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

    def moyenne_genetique(self):
        """
        :return: Moyenne pondérée de la génétique de l'individu
        """
        return average([self.vitesse_max,
                        self.acceleration_max,
                        self.faim_max,
                        self.fatigue_max,
                        self.esperance_vie], weights=[4, 4, 2, 3, 4])


def get_couleur(val):
    """
    :param val: Valeur de jauge mappée entre 0 et 1
    :return: Couleur correspondante pour l'affichage des jauges sur le HUD
    """
    if val <= 0.25:
        return 'green'
    elif val <= 0.5:
        return 'yellow'
    elif val <= 0.75:
        return 'orange'
    else:
        return 'red'
