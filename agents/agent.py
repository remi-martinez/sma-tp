import random

from pygame import Vector2


class Agent(object):
    def __init__(self, body):
        self.uuid = random.randint(100000, 999999999)
        self.body = body
        self.perceptionList = []

    def update(self):
        # TODO
        self.filtrePerception()

    def filtrePerception(self):
        # TODO
        pass

    def show(self):
        self.body.show()
