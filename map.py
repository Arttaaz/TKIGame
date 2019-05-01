# -*- coding: utf-8 -*-
"""
A map.
"""

from gameobject import GameObject
from unit import Unit, dist, InnerState
import pygame
import random

class Map:
    def __init__(self, cell_size, width = 0, height = 0, depth = 0, path = None):
        self.cell_size = cell_size
        self.surf = None
        if path is not None:
            self.read_file(path)
        else:
            self.cases = [[[None for k in depth] for j in range(height)] for i in range(width)]
            self.width = width
            self.height = height
            self.depth = depth
            self.units = []

    def update(self):
        for k in range(self.depth):
            for i in range(self.width):
                for j in range(self.height):
                    if self.cases[i][j][k] is not None:
                        print(type(self.cases[i][j][k]))
                        self.cases[i][j][k].update()

    def draw(self, screen, x, y):
        if self.surf is None:
            self.surf = pygame.Surface((screen.get_width(), screen.get_height()))
        self.surf.fill((0, 0, 0))
        x -= self.cell_size * (self.width - 1) / 2
        y -= self.cell_size * (self.height - 1) / 2
        for k in range(self.depth):
            for i in range(self.width):
                for j in range(self.height):
                    if self.cases[i][j][k] is not None:
                        self.cases[i][j][k].draw(self.surf, x + i * self.cell_size, y + j * self.cell_size)

        screen.blit(self.surf, (0, 0))
    def resize(self, width = None, height = None, depth = None):
        if width is None:
            width = self.width
        if height is None:
            height = self.height
        if depth is None:
            depth = self.depth

        new_cases = [[[None for k in range(depth)] for j in range(height)] for i in range(width)]
        for k in range(self.depth):
            for i in range(self.width):
                for j in range(self.height):
                    new_cases[i][j][k] = self.cases[i][j][k]
        self.cases = new_cases
        self.width = width
        self.height = height
        self.depth = depth
    def random_unit(self, omit, my_team = False):
        l = [_ for _ in self.units if (_.team is omit.team) == my_team and _.state is not InnerState.DEAD  and _ is not unit]
        if len(l) == 0:
            return None

        return random.choice(l)

    def closest_unit(self, unit, my_team = False):
        l = [_ for _ in self.units if (_.team is unit.team) == my_team
             and _.state != InnerState.DEAD and _ is not unit]

        if len(l) == 0:
            return None

        return min(l, key = lambda u : dist((u.xmap, u.ymap), (unit.xmap, unit.ymap)))
    def farthest_unit(self, unit, my_team = False):
        l = [_ for _ in self.units if (_.team is unit.team) == my_team
             and _.state != InnerState.DEAD  and _ is not unit]

        if len(l) == 0:
            return None

        return max(l, key = lambda u : dist((u.xmap, u.ymap), (unit.xmap, unit.ymap)))
    
    def low_hp_unit(self, unit):
        l = [_ for _ in self.units if (_.team is unit.team) == my_team and _.state is not InnerState.DEAD  and _ is not unit]
        if len(l) == 0:
            return None

        return min(l, key = lambda u : u.hp)
    def high_hp_unit(self, unit):
        l = [_ for _ in self.units if (_.team is unit.team) == my_team and _.state is not InnerState.DEAD and _ is not unit]
        if len(l) == 0:
            return None

        return max(l, key = lambda u : u.hp)


    """
    Transformer une coordonnee world en coordonnee map
    """
    def world_to_map_x(self, x):
        return max(min(int((x + self.cell_size * self.width / 2)) // self.cell_size, self.width - 1), 0)
    def world_to_map_y(self, y):
        return max(min(int((y + self.cell_size * self.height / 2)) // self.cell_size, self.height - 1), 0)

    """
    Transforme une coordonnée map en coordonnée world
    """
    def map_to_world_x(self, x):
        return x * self.cell_size - self.cell_size * (self.width - 1) / 2
    def map_to_world_y(self, y):
        return y * self.cell_size - self.cell_size * (self.height - 1) / 2


    def id(self, x, y, z):
        object = self.cases[x][y][z]
        if object is None:
            return 0
        else:
            return object.id

    def behaviour(self, x, y, z):
        object = self.cases[x][y][z]
        if object is None or not isinstance(object, Unit):
            return 0
        else:
            return object.behaviour

    def collide(self, x, y):
        for case in self.cases[x][y]:
            if case.collide:
                return True

        return False


    def generate_object(self, desc, x, y):
        words = desc.split(";")
        id = int(words[0])
        behaviour = 0
        if len(words) > 1:
            behaviour = int(words[1])
        if id == 0:
            game_object = None
        elif id == 1:
            game_object = GameObject(pygame.image.load('assets/Herbe' + str(random.randint(0, 1)+1) + '.png'), self,  x, y, id, False)
        elif id in range(2, 4) or id in range(10, 12):
            game_object = Unit(pygame.image.load('assets/' + str(id) + '.png'), self, x, y, id, behaviour)
            self.units.append(game_object)
        elif id in range(4, 10):
            game_object = GameObject(pygame.image.load('assets/' + str(id) + '.png'), self,  x, y, id, True)
        else:
            game_object = GameObject(pygame.image.load('assets/' + str(id) + '.png'), self,  x, y, id, False)

        return game_object
    def read_cases(self, content):
        objects = (self.generate_object(c, 0, 0) for line in content for c in line.split())
        self.cases = [[[None for k in range(self.depth)] for j in range(self.height)] for i in range(self.width)]
        self.units = []
        for k in range(self.depth):
            for j in range(self.height):
                for i in range(self.width):
                    object = next(objects)
                    if object is not None:
                        object.xmap = i
                        object.ymap = j
                    self.cases[i][j][k] = object
    def remove(self, x, y, z):
        if self.cases[x][y][z] in self.units:
            self.units.remove(self.cases[x][y][z])
    def write_file(self, path):
        f = open(path, 'w')
        f.write(str(self.width))
        f.write('\n')
        f.write(str(self.height))
        f.write('\n')
        f.write(str(self.depth))
        f.write('\n')
        for k in range(self.depth):
            for j in range(self.height):
                f.write(' '.join([str(self.id(i, j, k)) + ";" + str(self.behaviour(i,j,k)) for i in range(self.width)]))
                f.write('\n')
            f.write('\n')
    def read_file(self, path):
        f = open(path, 'r')
        lines = iter(f.readlines())

        self.width = int(next(lines))
        self.height = int(next(lines))
        self.depth = int(next(lines))
        self.read_cases(lines)

        if len(self.cases) != self.width or len(self.cases[0]) != self.height:
            print("Erreur dans les dimensions de la map chargée")
        f.close()
