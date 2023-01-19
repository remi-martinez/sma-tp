import core
from agents.superpredateur import SuperPredateur
from bodies.body import Body


class SuperPredateurBody(Body):
    def __init__(self):
        self.type = 'SuperPredateur'
        super().__init__()

    def update(self):
        super().update()

    def reproduction(self):
        cloned_body = super().reproduction()
        core.memory('agents').append(SuperPredateur(cloned_body))
