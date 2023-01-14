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
        manger, fuir, symbiose = self.filtrePerception()

        target = Vector2(random.randint(-1, 1), random.randint(-1, 1))
        while target.length() == 0:
            target = Vector2(random.randint(-1, 1), random.randint(-1, 1))

        if len(symbiose) > 0:
            target = symbiose[0].position - self.body.position

        if len(manger) > 0:
            target = manger[0].position - self.body.position

        if len(fuir) > 0:
            target = self.body.position - fuir[0].position


        self.body.acceleration = self.body.acceleration + target

    def filtrePerception(self):
        manger = []
        fuir = []
        symbiose = []

        for i in self.body.fustrum.perceptionList:
            i.dist = self.body.position.distance_to(i.position)
            if i.mort is False:
                if isinstance(i, HerbivoreBody):
                    manger.append(i)
                if isinstance(i, SuperPredateurBody):
                    fuir.append(i)
                # if isinstance(i, DecomposeurBody):
                #     symbiose.append(i)

        manger.sort(key=lambda x: x.dist, reverse=False)
        return manger, fuir, symbiose


