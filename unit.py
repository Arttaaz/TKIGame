"""
Ennemi.
"""
import pygame
from enum import Enum
import astar
from gameobject import GameObject

class State(Enum):
    IDLE = 1
    SHOOT = 2


class Unit(GameObject):
    def __init__(self, image, grid, id = 1, collide = True):
        GameObject.__init__(self, image, grid, id, collide)
        self.state = State.SHOOT
        self.target = None
    def follow(self, target):
        pass

    def update(self, collisions):
        self

    def move(self, destination):
        path = list(astar.find_path(self.grid.coord_of(self, 1), self.grid.coord(destination, 1), neighbors_fnct=neighbors,
         heuristic_cost_estimate_fnct=cost, distance_between_fnct=dist))
        x0, y0 = self.grid.coord_of(self, 1)
        x1, y1 = path[0]
        self.grid.cases[x0][y0].remove(self)
        self.grid.cases[x1][y1][1] = self


    def rotation_to_target(self):

        pos1 = pygame.Vector2(self.rect.centerx, self.rect.centery)
        pos2 = pygame.Vector2(self.target.rect.centerx, self.target.rect.centery)
        dir = pos2 - pos1
        y = pygame.Vector2(0, 1)
        return( 180 - y.angle_to(dir)) % 360

    def update(self, map):

        if map.units[0] != self:
            self.target = map.units[0]

        if self.state == State.SHOOT and self.target is not None:
            self.rotation = 0.9 * self.rotation + 0.1 * self.rotation_to_target()

    def draw(self, screen, x, y):
        super().draw(screen, x, y)

        #if self.state == State.SHOOT and self.target is not None:
            #pygame.draw.aalines(screen, (0, 0, 0), (self.rect.centerx, self.rect.centery)


def neighbors(unit):
    x, y = unit.grid.coord_of(unit, 1)
    return [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]

def cost(n, goal):
    return 1

def dist(u0, u1):
    x0, y0 = u0.grid.coord_of(u0, 1)
    x1, y1 = u1.grid.coord_of(u1, 1)
    return ((x1 - x0)**2 + (y1 - y0)**2)**0.5
