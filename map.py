# -*- coding: utf-8 -*-
"""
Objet permettant de gérer
une carte du jeu.
"""


from gameobject import GameObject
from unit import Unit, dist, InnerState
import pygame
import random


class Map:
    def __init__(self, cell_size, width=0, height=0, depth=0, path=None):
        """
        Il est possible d'initialisé la map avec
        un fichier, en donnant le chemin
        du fichier en paramètre.
        """
        self.cell_size = cell_size
        self.surf = None # Objet pygame : surface de la map
        if path is not None:
            self.read_file(path)
        else:
            self.cases = [[[None for k in depth] for j in range(height)] for i in range(width)]
            self.width = width
            self.height = height
            self.depth = depth
            self.units = []

    def update(self):
        """
        Update tout les composants de la map,
        layer par layer. Cela ne les dessines pas, mais
        ça actualise leur représentation en interne,
        pour le prochain draw.
        """
        for k in range(self.depth):
            for i in range(self.width):
                for j in range(self.height):
                    if self.cases[i][j][k] is not None:
                        self.cases[i][j][k].update() # C'est pour cette raison qu'il faut que gameobject ai une fonction update

    def draw(self, screen, x, y):
        """
        Dessine la map ainsi que tous les composants.
        Les dessins sont fait sur la surface de la map,
        puis la surface est redessinée sur le screen
        """
        if self.surf is None:
            self.surf = pygame.Surface((screen.get_width(), screen.get_height()))
        self.surf.fill((0, 0, 0))

        x -= self.cell_size * (self.width - 1) / 2
        y -= self.cell_size * (self.height - 1) / 2
        for k in range(self.depth): # Dessine les composants du plus petit layer au plus grand
            for i in range(self.width):
                for j in range(self.height):
                    if self.cases[i][j][k] is not None:
                        self.cases[i][j][k].draw(self.surf, x + i * self.cell_size, y + j * self.cell_size)

        screen.blit(self.surf, (0, 0)) # affiche la nouvelle belle surface sur l'écran !

    def resize(self, width=None, height=None, depth=None):
        """
        Resize la map.
        Les anciens objets sont coupés,
        on ne garde que ceux qui sont dans déjà dans
        la bonne taille de la nouvelle map.
        """
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
                    new_cases[i][j][k] = self.cases[i][j][k] # recopie les anciennes cases, si possible

        self.cases = new_cases
        self.width = width
        self.height = height
        self.depth = depth

    def random_unit(self, omit, my_team=False):
        """
        Selectionne une unité au hasard sur la carte.
        Si on set my_team à True, l'unité doit être de la même team que l'unité omit,
        Les unités mortes sont ignorées.
        L'unité 'omit' est ignorée.
        """
        l = [_ for _ in self.units if (_.team is omit.team) == my_team and _.state is not InnerState.DEAD  and _ is not omit]
        if len(l) == 0:
            return None

        return random.choice(l)

    def closest_unit(self, unit, my_team=False):
        """
        Retourne l'unité la plus proche de l'unité donnée.
        Si my_team est set à True, l'unité sélectionnée fait partie de la team de l'unit initiale.
        """
        l = [_ for _ in self.units if (_.team is unit.team) == my_team
             and _.state != InnerState.DEAD and _ is not unit]

        if len(l) == 0:
            return None

        return min(l, key=lambda u : dist((u.xmap, u.ymap), (unit.xmap, unit.ymap))) # la distance est calculée en distance euclidienne !

    def farthest_unit(self, unit, my_team=False):
        """
        Retourne l'unité la plus éloignée de l'unité donnée.
        Si my_team est set à True, l'unité sélectionnée fait partie de la team de l'unit initiale.
        """
        l = [_ for _ in self.units if (_.team is unit.team) == my_team
             and _.state != InnerState.DEAD  and _ is not unit]

        if len(l) == 0:
            return None

        return max(l, key = lambda u : dist((u.xmap, u.ymap), (unit.xmap, unit.ymap)))

    def low_hp_unit(self, unit, my_team=False):
        """
        Sélectionne l'unité la plus endommagée.
        my_team a toujours le même rôle.
        """
        l = [_ for _ in self.units if (_.team is unit.team) == my_team and _.state is not InnerState.DEAD  and _ is not unit]
        if len(l) == 0:
            return None

        return min(l, key=lambda u : u.hp)

    def high_hp_unit(self, unit, my_role):
        """
        Sélectionne l'unité avec le plus de vie.
        my_team a toujours le même rôle.
        """
        l = [_ for _ in self.units if (_.team is unit.team) == my_team and _.state is not InnerState.DEAD and _ is not unit]
        if len(l) == 0:
            return None

        return max(l, key=lambda u : u.hp)


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
        """
        Retourne l'id de l'objet qui
        est aux coordonnées données.
        """
        objet = self.cases[x][y][z]
        if objet is None:
            return 0
        else:
            return objet.id

    def behaviour(self, x, y, z):
        """
        Retourne le comportement
        de l'unité ciblée par les coordonnées,
        si unité il y a. Sinon retourne 0.
        """
        objet = self.cases[x][y][z]
        if objet is None or not isinstance(objet, Unit):
            return 0
        else:
            return objet.behaviour

    def collide(self, x, y):
        """
        Retourne la propriété de collision
        des objets situés à la case pointée par x et y.
        Si un des objets a une propriété de collision,
        retourne True.
        """
        for case in self.cases[x][y]:
            if case.collide:
                return True

        return False

    def generate_object(self, desc, x, y):
        """
        Retourne un GameObject qui dépends de
        la description que l'on donne. Il est placé directement
        aux coordonnées x, y demandées.
        """
        words = desc.split(";")
        identifiant = int(words[0])
        behaviour = 0
        if len(words) > 1:
            behaviour = int(words[1])
        if identifiant == 0:
            game_object = None
        elif identifiant == 1:
            game_object = GameObject(pygame.image.load('assets/Herbe' + str(random.randint(0, 1)+1) + '.png'), self,  x, y, identifiant, False)
        elif identifiant in range(2, 4) or identifiant in range(10, 12):
            game_object = Unit(pygame.image.load('assets/' + str(identifiant) + '.png'), self, x, y, identifiant, behaviour)
            self.units.append(game_object)
        elif identifiant in range(4, 10):
            game_object = GameObject(pygame.image.load('assets/' + str(identifiant) + '.png'), self,  x, y, identifiant, True)
        else:
            game_object = GameObject(pygame.image.load('assets/' + str(identifiant) + '.png'), self,  x, y, identifiant, False)
        return game_object

    def read_cases(self, content):
        """
        Créé tous les GameObject et les places sur le tableau de case.
        Remplie aussi le tableau des unités.
        Content est une ligne d'un fichier décrivant la map.
        """
        objects = (self.generate_object(c, 0, 0) for line in content for c in line.split())
        self.cases = [[[None for k in range(self.depth)] for j in range(self.height)] for i in range(self.width)]
        self.units = []
        for k in range(self.depth):
            for j in range(self.height):
                for i in range(self.width):
                    objet = next(objects)
                    if objet is not None:
                        objet.xmap = i
                        objet.ymap = j

                    if isinstance(objet, Unit):
                        self.units.append(objet)

                    self.cases[i][j][k] = objet

    def remove(self, x, y, z):
        """
        Retire une unité du terrain.
        """
        if self.cases[x][y][z] in self.units:
            self.units.remove(self.cases[x][y][z])

    def write_file(self, path):
        """
        Ecrit dans un fichier la représentation de cette map.
        """
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
        """
        Lit dans un fichier la map,
        elle est donc reconstituée dans l'instance de cet objet.
        """
        f = open(path, 'r')
        lines = iter(f.readlines())

        self.width = int(next(lines))
        self.height = int(next(lines))
        self.depth = int(next(lines))
        self.read_cases(lines)

        if len(self.cases) != self.width or len(self.cases[0]) != self.height:
            print("Erreur dans les dimensions de la map chargée")
        f.close()
