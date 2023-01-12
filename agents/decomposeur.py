from agents.agent import Agent


class Decomposeur(Agent):
    def __init__(self, body):
        super().__init__(body)
        self.body.color = (194, 168, 19)

