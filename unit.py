
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
    FAILED = "Impossible..."
    HEAL = "Soin"
    WALK = "Marche"
    DEAD = "DEAD"

bullet_time = 0.3
tick_time = 1
UNIT_LAYER = 2
DEAD_LAYER = 1
class Unit(GameObject):
    def __init__(self, image, grid, xmap, ymap, id = 1, collide = True, team = 1):
        GameObject.__init__(self, image, grid, xmap, ymap, id, collide)
        self.state = InnerState.IDLE
        self.target = None
        self.xmap = xmap
        self.ymap = ymap
        self.xdest = xmap
        self.ydest = ymap
        self.team = id
        self.hp = 100
        self.hpmax = 100
        self.bullet_progress = 0
        self.tick_progress = 0
        self.start_shooting_time = 0
        self.start_shooting = False
        self.arbre = creer_unite_attaque(self)
    def follow(self, target):
        pass


    def move(self, param):
        if self.target is not None:
            path = astar.find_path((self.xmap, self.ymap), (self.target.xmap, self.target.ymap), neighbors_fnct=neighbors_map(self.grid, self.target), heuristic_cost_estimate_fnct=cost, distance_between_fnct=dist)
            if path is not None:
                path = list(path)
                x, y = path[1]
                self.state = InnerState.WALK
                self.xdest = x
                self.ydest = y

    def set_inner_state(self, state):
        self.state = state
    def set_tree_state(self, state):
        self.arbre.set_state(state)
    def select_target(self, target):
        if target == Target.NEAREST_ENEMY:
            self.target = self.grid.closest_unit(self, True)
            self.state = InnerState.IDLE
    def shoot(self, param):
        if self.target is not None and self.can_shoot():
            self.set_inner_state(InnerState.SHOOT)
            self.target.hp -= 34
        else:
            self.set_inner_state(InnerState.FAILED)
    def heal(self, param):
        if self.target is not None and self.can_shoot():
            self.set_inner_state(InnerState.HEAL)
            self.target.hp += 10
        else:
            self.set_inner_state(InnerState.FAILED)
    
    def est_a_portee(self, param):
        if self.target is  None:
            return "NO TARGET"
        return  "Oui" if dist((self.target.xmap, self.target.ymap), (self.xmap, self.ymap)) <= 3 else "Non"
    def rotation_to_target(self):

        pos1 = pygame.Vector2(self.rect.centerx, self.rect.centery)
        pos2 = pygame.Vector2(self.target.rect.centerx, self.target.rect.centery)
        dir = pos2 - pos1
        y = pygame.Vector2(0, 1)
        return( 180 - y.angle_to(dir)) % 360
    def am_i_dead(self, param):
        return self.hp <= 0
    def is_dead(self, param):
        if self.target is None or self.target.am_i_dead(param):
            return "Oui"
        else:
            return "Non"


    def can_shoot(self):
        if self.target is not None: # TODO: change 3 to range
            return True  # TODO: line_of_sight function
        return False

    def tick(self): 
        if self.state == InnerState.WALK:
            self.grid.cases[self.xmap][self.ymap][UNIT_LAYER] = None
            self.grid.cases[self.xdest][self.ydest][UNIT_LAYER] = self
            self.xmap = self.xdest
            self.ymap = self.ydest
        self.tick_progress = 0

        self.arbre.eval()


    def update(self, map):
        if self.state != InnerState.DEAD:
            self.tick_progress += 1 / 60 / (tick_time)
        if self.state != InnerState.DEAD and self.tick_progress > 1:
            self.tick()
            
        if self.hp <= 0 and self.state != InnerState.DEAD:

            self.state = InnerState.DEAD
            self.grid.cases[self.xmap][self.ymap][UNIT_LAYER] = None
            self.grid.cases[self.xmap][self.ymap][DEAD_LAYER] = self
            
        if self.state == InnerState.DEAD:
            self.rotation += 1
        elif self.target is not None:
            
            self.rotation = 0.9 * self.rotation + 0.1 * self.rotation_to_target()
        

    def draw(self, screen, x, y):
        if self.state == InnerState.WALK or self.state == InnerState.DEAD:
            x += (self.xdest - self.xmap) * self.grid.cell_size * self.tick_progress
            y += (self.ydest - self.ymap) * self.grid.cell_size * self.tick_progress
        super().draw(screen, x, y)
        screen.fill((255, 0, 0), rect=pygame.Rect(self.rect.centerx - 32 + 15, self.rect.centery - 32 + 50, 34 , 5))
        screen.fill((0, 255, 0), rect=pygame.Rect(self.rect.centerx - 32 + 15, self.rect.centery - 32 + 50, int(34 * self.hp/self.hpmax), 5))
        if self.state in [InnerState.SHOOT, InnerState.HEAL] and self.target is not None and self.can_shoot():
            pos1 = pygame.Vector2(self.rect.centerx, self.rect.centery)
            pos2 = pygame.Vector2(self.target.rect.centerx, self.target.rect.centery)
            if pos1 != pos2:
                dir = (pos2 - pos1).normalize()
                
                begin = pos1 +  dir * 23
                end = pos2 - dir * 11
                
                if self.state == InnerState.SHOOT:
                    self.bullet_progress = (self.tick_progress * 4) % 2 
                    self.bullet_progress = 1 if self.bullet_progress > 1 else self.bullet_progress
                    draw_progress_line(screen, begin, end, self.bullet_progress, 0.1, 0.9, (0, 0, 0))
                if self.state == InnerState.HEAL:
                    self.soin_progress = (self.tick_progress * 2) % 2
                    draw_progress_line(screen, begin, end, self.soin_progress, 0.4, 0.6, (0, 255, 0))
def draw_progress_line(screen,begin, end, progress, deb_time, end_time, color):
    if progress < deb_time:
        p1 = begin
    else:
        t = (progress - deb_time) / (1 - deb_time)
        p1 = (1 - t) * begin + t * end
    if progress > end_time:
        p2 = end
    else:
        t = progress / end_time
        p2 = (1 - t) * begin + t * end
                
        pygame.draw.aaline(screen, color, (p1.x, p1.y),
                               (p2.x, p2.y))
            
def neighbors_map(map, goal):
    def neighbors(unit):

        l = []
        
        x, y = unit
        
        if x < (map.width-1) and (map.cases[x+1][y][UNIT_LAYER] is None or map.cases[x+1][y][UNIT_LAYER] == goal or not map.cases[x+1][y][UNIT_LAYER].collide):
            l.append((x+1, y))
        if x > 0 and (map.cases[x-1][y][UNIT_LAYER] is None or map.cases[x-1][y][UNIT_LAYER] == goal or not map.cases[x-1][y][UNIT_LAYER].collide):
            l.append((x-1, y))
        if y < (map.height-1) and (map.cases[x][y+1][UNIT_LAYER] is None or map.cases[x][y+1][UNIT_LAYER] == goal or not map.cases[x][y+1][UNIT_LAYER].collide):
            l.append((x, y+1))
        if y > 0 and (map.cases[x][y-1][UNIT_LAYER] is None or map.cases[x][y-1][UNIT_LAYER] == goal or not map.cases[x][y-1][UNIT_LAYER].collide):
            l.append((x, y-1))
        return l

    return neighbors


def cost(n, goal):
    return 1

def dist(u0, u1):
    x0, y0 = u0
    x1, y1 = u1
    return ((x1 - x0)**2 + (y1 - y0)**2)**0.5
