from bodies.body import Body


class CarnivoreBody(Body):
    def __init__(self):
        super().__init__()
        self.fatigue_max = 80

    def update(self):
        super().update()
