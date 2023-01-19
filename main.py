import json
import time

import core
from agents.carnivore import Carnivore
from agents.decomposeur import Decomposeur
from agents.herbivore import Herbivore
from agents.superpredateur import SuperPredateur
from bodies.carnivorebody import CarnivoreBody
from bodies.decomposeurbody import DecomposeurBody
from bodies.herbivorebody import HerbivoreBody
from bodies.superpredateurbody import SuperPredateurBody
from items.vegetal import Vegetal

COLLISION_RADIUS = 20
VALEUR_NUTRITIVE = 30


def setup():
    print("Setup START---------")
    core.fps = 30

    core.WINDOW_SIZE = [500, 500]

    core.memory("agents", [])
    core.memory("items", [])
    core.memory("hearts", [])
    core.memory("timer", time.time())

    # load("scenario.json")

    for i in range(0, 1):
        core.memory('agents').append(SuperPredateur(SuperPredateurBody()))

    # for i in range(0, 3):
    #     core.memory('agents').append(Decomposeur(DecomposeurBody()))
    #
    # for i in range(0, 5):
    #     core.memory('agents').append(Herbivore(HerbivoreBody()))
    #
    for i in range(0, 1):
        core.memory('agents').append(Carnivore(CarnivoreBody()))
    #
    # for i in range(0, 10):
    #     core.memory('items').append(Vegetal())

    print("Setup END-----------")


def computePerception(a):
    a.body.fustrum.perceptionList = []
    for b in core.memory('agents'):
        if a.uuid != b.uuid:
            if a.body.fustrum.inside(b.body):
                a.body.fustrum.perceptionList.append(b.body)
    for item in core.memory("items"):
        if a.body.fustrum.inside(item):
            a.body.fustrum.perceptionList.append(item)


def computeDecision(a):
    a.update()


def applyDecision(a):
    a.body.update()


def reset():
    setup()


def update_environment():
    for a in core.memory('agents'):
        for b in core.memory('agents'):
            if (a.body.position.distance_to(b.body.position) - a.body.taille_body) <= COLLISION_RADIUS:
                if isinstance(a, Decomposeur):
                    if not (isinstance(b, Decomposeur)):
                        if b.body.mort is True:
                            if b.body.decomposition < 100:
                                b.body.decomposer()
                            else:
                                nouveau_vegetal = Vegetal()
                                nouveau_vegetal.position = b.body.position
                                core.memory('items').append(nouveau_vegetal)
                                core.memory('agents').remove(b)
                if isinstance(a, Carnivore):
                    if isinstance(b, Herbivore):
                        a.body.faim_valeur -= VALEUR_NUTRITIVE
                        b.body.kill()
                    if isinstance(b, SuperPredateur):
                        a.body.faim_valeur -= VALEUR_NUTRITIVE
                        a.body.kill()
        for item in core.memory('items'):
            if (a.body.position.distance_to(item.position) - a.body.taille_body) <= COLLISION_RADIUS:
                if isinstance(a, Herbivore):
                    core.memory('items').remove(item)


def load(path):
    f = open(path)
    data = json.load(f)
    core.memory("scenario", data)


def run():
    core.cleanScreen()

    if core.getKeyPressList("r"):
        reset()

    for item in core.memory("items"):
        item.show()

    for agent in core.memory("agents"):
        agent.show()

    for agent in core.memory("agents"):
        computePerception(agent)

    for agent in core.memory("agents"):
        computeDecision(agent)

    for agent in core.memory("agents"):
        applyDecision(agent)

    for heart in core.memory("hearts"):
        heart.show()

    update_environment()


core.main(setup, run)
