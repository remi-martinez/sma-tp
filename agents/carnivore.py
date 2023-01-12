import random

from pygame import Vector2

from agents.agent import Agent
from agents.herbivore import Herbivore
from bodies.herbivorebody import HerbivoreBody
from fustrum import Fustrum
from items.vegetal import Vegetal


class Carnivore(Agent):
    def __init__(self, body):
        super().__init__(body)
        self.body.color = (102, 48, 0)

    def update(self):
        manger, fuir, symbiose = self.filtrePerception()

        target = Vector2(random.randint(-1, 1), random.randint(-1, 1))
        while target.length() == 0:
            target = Vector2(random.randint(-1, 1), random.randint(-1, 1))

        self.body.acceleration += target

        if len(manger) > 0:
            target = manger[0].position - self.body.position
            self.body.acceleration = self.body.acceleration + target

    def filtrePerception(self):
        manger = []
        fuir = []
        symbiose = []

        for i in self.body.fustrum.perceptionList:
            i.dist = self.body.position.distance_to(i.position)
            if isinstance(i, HerbivoreBody):
                manger.append(i)

        manger.sort(key=lambda x: x.dist, reverse=False)
        return manger, fuir, symbiose


