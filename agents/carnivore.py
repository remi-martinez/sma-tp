from agents.agent import Agent


class Carnivore(Agent):
    def __init__(self, body):
        super().__init__(body)
        self.body.color = (102, 48, 0)

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
                if i.type == 'Herbivore':
                    manger.append(i)
                if i.type == 'SuperPredateur':
                    fuir.append(i)

        return manger, fuir, symbiose
