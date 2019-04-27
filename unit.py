"""
Ennemi.
"""
import pygame
from enum import Enum
<<<<<<< HEAD
import astar

class State(Enum):
    IDLE = 1
    FOLLOW = 2


class Unit(pygame.sprite.Sprite):

    def __init__(self, pos, speed):
        pygame.sprite.Sprite.__init__(self)

        self.pos = pos
        self.speed = speed
=======
from gameobject import GameObject

class State(Enum):
    IDLE = 1
    SHOOT = 2
    
    
class Unit(GameObject):
>>>>>>> 75cba5b88cfdd91a9b7950bd2765c8943e2e0109

    def __init__(self, image, id = 1, collide = True):
        GameObject.__init__(self, image, id, collide)
        self.state = State.SHOOT
        self.target = None
    def follow(self, target):
<<<<<<< HEAD


    def update(self, collisions):
        self

    def move(self, destination):
        path = list(astar.find_path(self, destination, neighbors_fnct=neighbors,
         heuristic_cost_estimate_fnct=cost, distance_between_fnct=dist))
        self.grid.coord_of(path[0])


def neighbors(unit):
    x, y = unit.grid.coord_of(unit, 1)
    return [unit.grid.cases[x+1, y], unit.grid.cases[x-1, y], unit.grid.cases[x, y+1], unit.grid.cases[x, y-1]]

def cost(n, goal):
    return 1

def dist(u0, u1):
    x0, y0 = u0.grid.coord_of(u0, 1)
    x1, y1 = u1.grid.coord_of(u1, 1)
    return ((x1 - x0)**2 + (y1 - y0)**2)**0.5
=======
        pass

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
    
>>>>>>> 75cba5b88cfdd91a9b7950bd2765c8943e2e0109
