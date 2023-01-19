import random

from pygame import Vector2

from agents.agent import Agent


class SuperPredateur(Agent):
    def __init__(self, body):
        super().__init__(body)
        self.body.color = (235, 0, 0)

    def update(self):
        super().update()
        manger = self.filtrePerception()

        target = Vector2(random.randint(-1, 1), random.randint(-1, 1))
        while target.length() == 0:
            target = Vector2(random.randint(-1, 1), random.randint(-1, 1))

        if len(manger) > 0:
            target = manger[0].position - self.body.position

        self.body.acceleration = self.body.acceleration + target

    def filtrePerception(self):
        manger = []

        for i in self.body.fustrum.perceptionList:
            i.dist = self.body.position.distance_to(i.position)
            if i.mort is False:
                if i.type == 'Carnivore':
                    manger.append(i)

        manger.sort(key=lambda x: x.dist, reverse=False)
        return manger
