import core
from bodies.body import Body
# from agents.carnivore import Carnivore


class CarnivoreBody(Body):
    def __init__(self):
        super().__init__()
        self.type = 'Carnivore'
        self.fatigue_max = 80

    def update(self):
        super().update()

    def reproduction(self):
        cloned_body = super().reproduction()
        # core.memory('agents').append(Carnivore(cloned_body))
