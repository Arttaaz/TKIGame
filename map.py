# -*- coding: utf-8 -*-
"""
A map.
"""
from gameobject import GameObject
from unit import Unit
import pygame
class Map:

    def __init__(self, cell_size, width = 0, height = 0, depth = 0, path = None):
        self.cell_size = cell_size
        if path is not None:
            self.width, self.height, self.depth, self.cases, self.units = read_file(path)
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
                        self.cases[i][j][k].update(self)
    def draw(self, screen, x, y):
        x -= self.cell_size * (self.width - 1) / 2
        y -= self.cell_size * (self.height - 1) / 2
        for k in range(self.depth):
            for i in range(self.width):
                for j in range(self.height):
                    if self.cases[i][j][k] is not None:
                        self.cases[i][j][k].draw(screen, x + i * self.cell_size, y + j * self.cell_size)
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

    """
    Transformer une coordonnee world en coordonnee map
    """
    def world_to_map_x(self, x):
        return int((x + self.cell_size * self.width / 2)) // self.cell_size
    def world_to_map_y(self, y):
        return int((y + self.cell_size * self.height / 2)) // self.cell_size

    """
    Transforme une coordonnée map en coordonnée world
    """
    def map_to_world_x(self, x):
        return x * self.cell_size + self.cell_size / 2 - self.cell_size * (self.width - 1) / 2
    def map_to_world_y(self, x):
        return y * self.cell_size + self.cell_size / 2 - self.cell_size * (self.height - 1) / 2


    def id(self, x, y, z):
        object = self.cases[x][y][z]
        if object is None:
            return 0
        else:
            return object.id
    def collide(self, x, y):
        for case in self.cases[x][y]:
            if case.collide:
                return True

        return False


    def coord_of(self, gameObject, depth):
        for x in range(0, self.width):
            for y in range(0, self.height):
                if case[x][y][depth] == gameObject:
                    return (x, y)
        return None


def generate_object(id):
    if id == 0:
        game_object = None
    elif id == 2:
        game_object = Unit(pygame.image.load('assets/' + str(id) + '.png'), id)
    else:
        game_object = GameObject(pygame.image.load('assets/' + str(id) + '.png'), id, False)

    return game_object
def read_cases(content, width, height, depth):
    objects = (generate_object(int(c)) for line in content for c in line.split())
    cases = [[[None for k in range(depth)] for j in range(height)] for i in range(width)]
    units = []
    for k in range(depth):
        for j in range(height):
            for i in range(width):
                object = next(objects)
                if isinstance(object, Unit):
                    units.append(object)
                cases[i][j][k] = object
    return cases, units

def write_file(path, map):
    f = open(path, 'w')
    f.write(str(map.width))
    f.write('\n')
    f.write(str(map.height))
    f.write('\n')
    f.write(str(map.depth))
    f.write('\n')
    for k in range(map.depth):
        for j in range(map.height):
            f.write(' '.join([str(map.id(i, j, k)) for i in range(map.width)]))
            f.write('\n')
        f.write('\n')
def read_file(path):
    f = open(path, 'r')
    lines = iter(f.readlines())

    width = int(next(lines))
    height = int(next(lines))
    depth = int(next(lines))
    cases, units = read_cases(lines, width, height, depth)

    if len(cases) != width or len(cases[0]) != height:
        print("Erreur dans les dimensions de la map chargée")
    f.close()

    return width, height, depth, cases, units
