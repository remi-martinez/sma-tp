import json
import threading
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

COLLISION_RADIUS = 10
VALEUR_NUTRITIVE = 30
SAVED_TIME = time.time()


def setup():
    print("Setup START---------")
    core.fps = 30

    core.WINDOW_SIZE = [600, 600]

    core.memory("agents", [])
    core.memory("items", [])
    core.memory("hearts", [])
    core.memory("timer", time.time())

    load("scenario.json")

    for i in range(0, core.memory('scenario')['SuperPredateur']['nb']):
        core.memory('agents').append(SuperPredateur(SuperPredateurBody()))

    for i in range(0, core.memory('scenario')['Carnivore']['nb']):
        core.memory('agents').append(Carnivore(CarnivoreBody()))

    for i in range(0, core.memory('scenario')['Herbivore']['nb']):
        core.memory('agents').append(Herbivore(HerbivoreBody()))

    for i in range(0, core.memory('scenario')['Decomposeur']['nb']):
        core.memory('agents').append(Decomposeur(DecomposeurBody()))

    for i in range(0, core.memory('scenario')['Vegetal']['nb']):
        core.memory('items').append(Vegetal())

    # Démarrage d'un thread parallèle pour le graphique
    threading.Thread(target=afficher_graph, args=()).start()

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
                        # Un décomposeur se nourrit du cadavre
                        # puis un végétal pousse à la place une fois le processus terminé
                        if b.body.mort is True:
                            if b.body.decomposition < 100:
                                b.body.decomposer()
                            else:
                                a.body.faim_valeur -= VALEUR_NUTRITIVE
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
    print("Scenario '" + path + "' loaded")


def afficher_graph():
    pass


def pourcentage_population():
    counts = {}
    for agent in core.memory('agents'):
        if agent.body.mort is False:
            if agent.body.type not in counts:
                counts[agent.body.type] = 0
            counts[agent.body.type] += 1

    # Afficher le pourcentage de chaque type d'agent
    total = len([a for a in core.memory('agents') if a.body.mort is False])
    for agent_type, count in counts.items():
        pourcentage = count / total * 100
        print(f"{agent_type}: {pourcentage:.2f}%")


def meilleur_individu():
    meilleure_genetique = 0
    meilleur_individu = None
    for agent in core.memory('agents'):
        if agent.body.mort is False:
            if agent.body.moyenne_genetique() > meilleure_genetique:
                meilleure_genetique = agent.body.moyenne_genetique()
                meilleur_individu = agent

    if meilleur_individu is None:
        return "Aucun"

    return f"{meilleur_individu.body.type} ({meilleur_individu.uuid})"


def run():
    core.cleanScreen()

    # Appuyer sur 'R' pour relancer la simulation
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

    if time.time() - core.memory('timer') >= 1:
        print("==== POPULATION ====")
        pourcentage_population()

        print("MEILLEUR INDIVIDU : " + meilleur_individu())

        core.memory('timer', time.time())


core.main(setup, run)
