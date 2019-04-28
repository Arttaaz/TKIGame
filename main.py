import sys, pygame
from map import Map
from enum import Enum
from state import State, GameState
import dimensions

pygame.init()

size = width, height = dimensions.LONGUEUR_FENETRE, dimensions.HAUTEUR_FENETRE
screen = pygame.display.set_mode(size, pygame.DOUBLEBUF, 32)
pygame.display.set_caption("LASER CRABS")
path = "assets/map.map"

State(screen).start()
