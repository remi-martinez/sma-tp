from agents.agent import Agent


class SuperPredateur(Agent):
    def __init__(self, body):
        super().__init__(body)
        self.body.color = (235, 0, 0)

