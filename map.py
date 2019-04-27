# -*- coding: utf-8 -*-
"""
A map.
"""
from gameobject import GameObject
import pygame
class Map:

    def __init__(self, cell_size, width = 0, height = 0, path = None):
        self.cell_size = cell_size
        if path is not None:
            self.width, self.height, self.cases = read_file(path)
        else:
            self.cases = [[None for i in range(width)] for j in range(height)]
            self.width = width
            self.height = height
    def update(self):
        for i in range(self.width):
            for j in range(self.height):
                if self.cases[i][j] is not None:
                    self.cases[i][j].update()
    def draw(self, screen):
        for i in range(self.width):
            for j in range(self.height):
                if self.cases[i][j] is not None:
                    self.cases[i][j].draw(screen, i * self.cell_size, j * self.cell_size)
    """
    Transformer une coordonnee world en coordonnee map
    """
    def world_to_map(self, x):
        return x // self.cell_size
    """
    Transforme une coordonnée map en coordonnée world
    """
    def map_to_world(self, x):
        return x * self.cell_size + self.cell_size / 2

    def id(self, x, y):
        object = self.cases[x][y]
        if object is None:
            return 0
        else:
            return object.id

    def coord_of(self, gameObject, layer):
        for x in range(0, self.width):
            for y in range(0, self.height):
                if case[layer][x][y] = gameObject:
                    return (x, y)
        return None


def generate_object(id):
    if id == 0:
        game_object = None
    else:
        game_object = GameObject(pygame.image.load('assets/' + str(id) + '.png'), id, False)
    return game_object

def read_cases(content, width, height):
    objects = (generate_object(int(c)) for line in content for c in line.split())
    cases = [[None for j in range(height)] for i in range(width)]
    for j in range(height):
        for i in range(width):
                cases[i][j] = next(objects)
    return cases

def write_file(path, map):
    f = open(path, 'w')
    f.write(str(map.width))
    f.write('\n')
    f.write(str(map.height))
    f.write('\n')
    for j in range(map.height):
        f.write(' '.join([str(map.id(i, j)) for i in range(map.width)]))
        f.write('\n')
def read_file(path):
    f = open(path, 'r')
    lines = iter(f.readlines())

    width = int(next(lines))
    height = int(next(lines))
    cases = read_cases(lines, width, height)

    if len(cases) != width or len(cases[0]) != height:
        print("Erreur dans les dimensions de la map chargée")
    f.close()

    return width, height, cases
