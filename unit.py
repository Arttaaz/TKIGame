"""
Ennemi.
"""
import pygame
from enum import Enum
import astar
from gameobject import GameObject
from creer_arbre import *
from target import Target
class InnerState(Enum):
    IDLE = "Idle"
    SHOOT = "Attaquer"
    DEAD = "DEAD"

bullet_time = 0.3

class Unit(GameObject):
    def __init__(self, image, grid, xmap, ymap, id = 1, collide = True, team = 1):
        GameObject.__init__(self, image, grid, xmap, ymap, id, collide)
        self.state = InnerState.SHOOT
        self.target = None
        self.xmap = xmap
        self.ymap = ymap
        self.team = id
        self.hp = 100
        self.bullet_progress = 0
        self.start_shooting_time = 0
        self.start_shooting = False
        self.arbre = creer_unite_attaque(self)
    def follow(self, target):
        pass


    def move(self, param):
        if not self.can_shoot():
            path = astar.find_path(self.grid.coord_of(self, 1), self.grid.coord_of(self.target, 1), neighbors_fnct=neighbors_map(self.grid, self.target), heuristic_cost_estimate_fnct=cost, distance_between_fnct=dist)
            if path is not None:
                path = list(path)
                x0, y0 = self.grid.coord_of(self, 1)
                x1, y1 = path[1]
                self.grid.cases[x0][y0][1] = None
                self.grid.cases[x1][y1][1] = self
                self.xmap = x1
                self.ymap = y1

    def set_inner_state(self, state):
        print("set state" + str(state))
        self.state = state
    def set_tree_state(self, state):
        print("set state" + str(state))
        print("set state" + str(self.arbre.etat_courant))
        self.arbre.set_state(state)
    def select_target(self, target):
        if target == Target.NEAREST_ENEMY:
            self.target = self.grid.closest_unit(self, False)
    def shoot(self, param):
        self.set_inner_state(shoot)
    def est_a_portee(self, param):
        return  "Oui" if self.target is not None and dist((self.target.xmap, self.target.ymap)) <= 5 else "Non"
    def rotation_to_target(self):

        pos1 = pygame.Vector2(self.rect.centerx, self.rect.centery)
        pos2 = pygame.Vector2(self.target.rect.centerx, self.target.rect.centery)
        dir = pos2 - pos1
        y = pygame.Vector2(0, 1)
        return( 180 - y.angle_to(dir)) % 360
    def is_dead(self, param):
        if self.target.state == InnerState.DEAD:
            return "Oui"
        else:
            return "Non"


    def can_shoot(self):

        if self.target is not None and dist((self.xmap, self.ymap), (self.target.xmap, self.target.ymap)) <= 3: # TODO: change 3 to range
            return True  # TODO: line_of_sight function
        return False


    def update(self, map):

        self.bullet_progress += 1 / 60 / (bullet_time)

        if self.target is None:
            self.target = map.closest_unit(self)

        if self.state == InnerState.SHOOT and self.target is not None:
            if self.can_shoot():
                self.rotation = 0.9 * self.rotation + 0.1 * self.rotation_to_target()
                self.bullet_progress += 1 / 60 / (bullet_time)

                if self.bullet_progress > 1:
                    self.target.hp -= 10
                    self.target = map.closest_unit(self)
            else:
                self.move()
        if self.bullet_progress > 1:
            self.bullet_progress = 0
            self.arbre.eval()
        
        if self.hp < 0:
            self.state = InnerState.DEAD
            self.rotation += 1

    def draw(self, screen, x, y):
        super().draw(screen, x, y)

        if self.state == InnerState.SHOOT and self.target is not None:
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


def neighbors_map(map, goal):
    def neighbors(unit):
        x, y = unit
        l = []
        if x < (map.width-1) and (map.cases[x+1][y][1] is None or map.cases[x+1][y][1] == goal or not map.cases[x+1][y][1].collide):
            l.append((x+1, y))
        if x > 0 and (map.cases[x-1][y][1] is None or map.cases[x-1][y][1] == goal or not map.cases[x-1][y][1].collide):
            l.append((x-1, y))
        if y < (map.height-1) and (map.cases[x][y+1][1] is None or map.cases[x][y+1][1] == goal or not map.cases[x][y+1][1].collide):
            l.append((x, y+1))
        if y > 0 and (map.cases[x][y-1][1] is None or map.cases[x][y-1][1] == goal or not map.cases[x][y-1][1].collide):
            l.append((x, y-1))
        return l

    return neighbors


def cost(n, goal):
    return 1

def dist(u0, u1):
    x0, y0 = u0
    x1, y1 = u1
    return ((x1 - x0)**2 + (y1 - y0)**2)**0.5
