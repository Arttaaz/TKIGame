"""
Ennemi.
"""
from enum import Enum
import astar

class State(Enum):
    IDLE = 1
    FOLLOW = 2


class Unit(pygame.sprite.Sprite):

    def __init__(self, pos, speed):
        pygame.sprite.Sprite.__init__(self)

        self.pos = pos
        self.speed = speed

    def follow(self, target):


    def update(self, collisions):
        self

    def move(self, destination):
        path = list(astar.find_path(self, destination, neighbors_fnct=neighbors,
         heuristic_cost_estimate_fnct=cost, distance_between_fnct=dist))
        self.grid.coord_of(path[0])


def neighbors(unit):
    x, y = unit.grid.coord_of(unit)
    return [unit.grid.cases[x+1, y], unit.grid.cases[x-1, y], unit.grid.cases[x, y+1], unit.grid.cases[x, y-1]]

def cost(n, goal):
    return 1

def dist(u0, u1):
    x0, y0 = u0.grid.coord_of(u0)
    x1, y1 = u1.grid.coord_of(u1)
    return ((x1 - x0)**2 + (y1 - y0)**2)**0.5
