from bodies.body import Body


class HerbivoreBody(Body):
    def __init__(self):
        super().__init__()
        self.fatigue_max = 60

    def update(self):
        super().update()
