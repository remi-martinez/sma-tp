import random

from pygame import Vector2

from bodies.body import Body
from bodies.carnivorebody import CarnivoreBody
from bodies.decomposeurbody import DecomposeurBody


class SuperPredateurBody(Body):
    def __init__(self):
        super().__init__()

    def update(self):
        super().update()


