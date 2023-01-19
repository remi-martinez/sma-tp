import random

from pygame import Vector2

from agents.agent import Agent
from bodies.decomposeurbody import DecomposeurBody
from bodies.herbivorebody import HerbivoreBody
from bodies.superpredateurbody import SuperPredateurBody


class Carnivore(Agent):
    def __init__(self, body):
        super().__init__(body)
        self.body.color = (102, 48, 0)

    def update(self):
        manger, fuir = self.filtrePerception()

        target = Vector2(random.randint(-1, 1), random.randint(-1, 1))
        while target.length() == 0:
            target = Vector2(random.randint(-1, 1), random.randint(-1, 1))

        if len(manger) > 0:
            target = manger[0].position - self.body.position

        if len(fuir) > 0:
            target = self.body.position - fuir[0].position

        self.body.acceleration = self.body.acceleration + target

    def filtrePerception(self):
        manger = []
        fuir = []

        for i in self.body.fustrum.perceptionList:
            i.dist = self.body.position.distance_to(i.position)
            if i.mort is False:
                print(i)
                if i.type == 'Herbivore':
                    manger.append(i)
                if i.type == 'SuperPredateur':
                    fuir.append(i)

        manger.sort(key=lambda x: x.dist, reverse=False)
        return manger, fuir
