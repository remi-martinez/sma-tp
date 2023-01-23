import core

import random


def parametre_aleatoire(agent_type, parametre):
    return random.randint(core.memory('scenario')[agent_type]['parametres'][parametre][0],
                          core.memory('scenario')[agent_type]['parametres'][parametre][1]) or None
