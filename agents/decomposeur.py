import core

from agents.agent import Agent
from items.vegetal import Vegetal


class Decomposeur(Agent):
    def __init__(self, body):
        super().__init__(body)
        self.body.color = (194, 168, 19)

    def update(self):
        super().update()
        if self.body.mort is True:
            core.memory('agents').remove(self)
            nouveau_vegetal = Vegetal()
            nouveau_vegetal.position = self.body.position
            core.memory('items').append(nouveau_vegetal)

    def filtrePerception(self):
        super().filtrePerception()
        manger = []
        fuir = []
        symbiose = []

        for i in self.body.fustrum.perceptionList:
            i.dist = self.body.position.distance_to(i.position)
            if i.mort is True:
                manger.append(i)

        return manger, fuir, symbiose
