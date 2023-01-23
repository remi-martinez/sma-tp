from agents.agent import Agent
from agents.superpredateur import SuperPredateur
from bodies.carnivorebody import CarnivoreBody
from items.vegetal import Vegetal


class Herbivore(Agent):
    def __init__(self, body):
        super().__init__(body)
        self.body.color = (25, 94, 31)

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
                if isinstance(i, Vegetal):
                    manger.append(i)
                if isinstance(i, CarnivoreBody):
                    fuir.append(i)
                if isinstance(i, SuperPredateur):
                    symbiose.append(i)

        return manger, fuir, symbiose
