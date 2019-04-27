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
    DEAD = 3
bullet_time = 0.3

class Unit(GameObject):
    def __init__(self, image, grid, xmap, ymap, id = 1, collide = True, team = 1):
        GameObject.__init__(self, image, grid, xmap, ymap, id, collide)
        self.state = State.SHOOT
        self.target = None
        self.xmap = xmap
        self.ymap = ymap
        self.team = team
        self.hp = 100
        self.bullet_progress = 0
        self.start_shooting_time = 0
        self.start_shooting = False
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

        if self.target is None:
            self.target = map.closest_unit(self)

        if self.state == State.SHOOT and self.target is not None:
            self.rotation = 0.9 * self.rotation + 0.1 * self.rotation_to_target()
            self.bullet_progress += 1 / 60 / (bullet_time)

            if self.bullet_progress > 1:
                self.bullet_progress = 0
                self.target.hp -= 10
                self.target = map.closest_unit(self)

        if self.hp < 0:
            self.state = State.DEAD
            self.rotation += 1
            
    def draw(self, screen, x, y):
        super().draw(screen, x, y)

        if self.state == State.SHOOT and self.target is not None:
            pos1 = pygame.Vector2(self.rect.centerx, self.rect.centery)
            pos2 = pygame.Vector2(self.target.rect.centerx, self.target.rect.centery)
            dir = (pos2 - pos1).normalize()
            begin = pos1 +  dir * 23
            end = pos2 - dir * 11

            if self.bullet_progress < 0.1:
                p1 = begin
            else:
                t = (self.bullet_progress - 0.1) / 0.9
                p1 = (1 - t) * begin + t * end
            if self.bullet_progress > 0.9:
                p2 = end
            else:
                t = self.bullet_progress / 0.9
                p2 = (1 - t) * begin + t * end
            
            
            pygame.draw.aaline(screen, (0, 0, 0), (p1.x, p1.y),
                                (p2.x, p2.y))



def neighbors(unit):
    x, y = unit.grid.coord_of(unit, 1)
    return [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]

def cost(n, goal):
    return 1

def dist(u0, u1):
    x0, y0 = u0.xmap, u0.ymap
    x1, y1 = u1.xmap, u1.ymap
    return ((x1 - x0)**2 + (y1 - y0)**2)**0.5
