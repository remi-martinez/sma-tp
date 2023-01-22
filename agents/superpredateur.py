import random

from pygame import Vector2

from agents.agent import Agent


class SuperPredateur(Agent):
    def __init__(self, body):
        super().__init__(body)
        self.body.color = (235, 0, 0)

    def update(self):
        super().update()

    def filtrePerception(self):
        super().filtrePerception()
        manger = []
        fuir = []
        symbiose = []

        for i in self.body.fustrum.perceptionList:
            i.dist = self.body.position.distance_to(i.position)
            if i.mort is False:
                if i.type == 'Carnivore':
                    manger.append(i)

        return manger, fuir, symbiose
