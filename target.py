"""
Enumération permettant de décrire
une cible d'une unité.
"""
from enum import Enum

class Target(Enum):
    NEAREST_ENEMY = "ENNEMI PROCHE"
    NEAREST_ALLY = "ALLIE PROCHE"
    FARTHEST_ENEMY = "ENNEMI LOIN"
    FARTHEST_ALLY = "ALLIE LOIN"
    THREAT = "MENACE" # La cible 'menace' est une cible qui nous attaque
    MAX_LIFE_ENEMY = "ENNEMI FORT"
    MIN_LIFE_ENEMY = "ENNEMI FAIBLE"
    MAX_LIFE_ALLY = "ALLIE FORT"
    MIN_LIFE_ALLY = "ALLIE FAIBLE"
    RANDOM_ENEMY = "ENNEMI ALEAT"
    RANDOM_ALLY = "ALLIE ALEAT"

    def __str__(self):
        return self.value
