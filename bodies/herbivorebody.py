import core
from agents.herbivore import Herbivore
from bodies.body import Body


class HerbivoreBody(Body):
    def __init__(self):
        super().__init__()
        self.type = 'Herbivore'
        self.fatigue_max = 60

    def update(self):
        super().update()

    def reproduction(self):
        cloned_body = super().reproduction()
        core.memory('agents').append(Herbivore(cloned_body))
