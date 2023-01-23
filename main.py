import json

import matplotlib.pyplot as plt
import numpy as np
from pygame import time as pygtime

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
DEBUT_SIMU = 0


def setup():
    print("Setup START---------")
    core.fps = 30

    core.WINDOW_SIZE = [600, 600]

    core.memory("agents", [])
    core.memory("items", [])
    core.memory("hearts", [])
    core.memory("timer", pygtime.get_ticks())

    # Chargement du scénario
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
    # threading.Thread(target=afficher_graph, args=()).start()

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
    global DEBUT_SIMU
    DEBUT_SIMU = pygtime.get_ticks()
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


def afficher_graph():
    while True:
        # Effacer les axes
        plt.cla()

        # Valeurs
        donnees = {"SuperPredateur": 0,
                   "Carnivore": 0,
                   "Herbivore": 0,
                   "Decomposeur": 0,
                   "Cadavre": 0,
                   "Vegetal": 0}
        y_pos = np.arange(len(donnees.keys()))

        for a in core.memory("agents"):
            if a.body.mort is True:
                donnees["Cadavre"] += 1
            else:
                donnees[a.body.type] += 1

        for i in core.memory("items"):
            donnees[i.type] += 1

        colors = [(235, 0, 0), (102, 48, 0), (25, 94, 31), (194, 168, 19), (138, 138, 138), (0, 255, 0)]
        colors = [[c / 255 for c in color] for color in colors]  # pour avoir des valeurs rgb entre 0 et 1
        plt.barh(y_pos, donnees.values(), align='center', color=colors)

        plt.yticks(y_pos, labels=donnees.keys())
        plt.gca().invert_yaxis()  # labels read top-to-bottom
        plt.xlabel("Nombre d'individus")
        plt.title("Population en temps réel")

        # Formatter les labels de l'axe des ordonnées
        for i, v in enumerate(donnees.values()):
            plt.text(v + 0.2, i - 0.1, str(v), color='black')
        start, end = plt.gca().get_xlim()
        plt.gca().xaxis.set_ticks(np.arange(end, start + 1, 1))

        plt.ion()
        plt.draw()
        plt.pause(0.1)


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

    return f"{meilleur_individu.body.type} (uuid {meilleur_individu.uuid})"


def temps_simu():
    return (pygtime.get_ticks() - DEBUT_SIMU) / 1000


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

    # Print toutes les 1000ms pour ne pas spammer
    if pygtime.get_ticks() - core.memory("timer") >= 1000:
        print(f"==== POPULATION ==== ({temps_simu():.0f}s)")
        pourcentage_population()
        core.memory("timer", pygtime.get_ticks())

        print("MEILLEUR INDIVIDU : " + meilleur_individu())


core.main(setup, run)
