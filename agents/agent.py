import random

from pygame import Vector2


class Agent(object):
    def __init__(self, body):
        self.uuid = random.randint(100000, 999999999)
        self.body = body
        self.perceptionList = []

    def update(self):
        manger, fuir, symbiose = self.filtrePerception()

        manger.sort(key=lambda x: x.dist, reverse=False)
        fuir.sort(key=lambda x: x.dist, reverse=False)
        symbiose.sort(key=lambda x: x.dist, reverse=False)

        target = Vector2(random.randint(-1, 1), random.randint(-1, 1))
        while target.length() == 0:
            target = Vector2(random.randint(-1, 1), random.randint(-1, 1))

        # Fuite = priorité MIN
        if len(symbiose) > 0:
            target = symbiose[0].position - self.body.position

        # Fuite = priorité MOYENNE
        if len(manger) > 0:
            target = manger[0].position - self.body.position

        # Fuite = priorité MAX
        if len(fuir) > 0:
            target = self.body.position - fuir[0].position

        self.body.acceleration = self.body.acceleration + target

    def filtrePerception(self):
        # Le filtre de perception sera 'override' par les classes enfants Carnivore, Decomposeur, etc
        return [], [], []

    def show(self):
        self.body.show()
