"""
Objet permettant d'implémenter une unité
dans le jeu. Contient toutes les fonctions
pour que l'unité puisse intéragir grâce à son arbre
de comportement.
"""

import pygame
from enum import Enum
import astar
from gameobject import GameObject
from creer_arbre import *
from target import Target


BULLET_TIME = 0.3
TICK_TIME = 0.4
UNIT_LAYER = 2
DEAD_LAYER = 1
DOMMAGES_ATTAQUE = 34
SOIN_ATTAQUE = 34


class InnerState(Enum):
    IDLE = "Idle"
    SHOOT = "Attaquer"
    FAILED = "Impossible..."
    HEAL = "Soin"
    WALK = "Marche"
    DEAD = "DEAD"


class Unit(GameObject):
    def __init__(self, image, grid, xmap, ymap, id_unit=1, behaviour=1, collide=True, team=1):
        GameObject.__init__(self, image, grid, xmap, ymap, id_unit, collide)

        self.state = InnerState.IDLE
        self.xmap, self.ymap = xmap, ymap
        self.xori, self.yori = xmap, ymap
        self.behaviour = behaviour
        self.image_dead = pygame.image.load('assets/grave.png')

        self.team = id_unit % 2
        self.hp = 100 * (self.team + 1) # l'équipe 1 a deux fois plus de hp que l'équipe 2
        self.hpmax = 100 * (self.team + 1)
        self.target = None

        self.bullet_progress = 0
        self.tick_progress = 0
        self.start_shooting_time = 0
        self.start_shooting = False

        self.lastUnit = None
        self.lastLastUnit = None
        self.is_attacked = False

        self.arbre = creer_unite(self, self.behaviour)

    def move(self, param):
        """
        Fonction 'Marcher vers' pour l'arbre.
        Utilise l'algo astar pour le path finding.
        """
        if self.target is not None:
            path = astar.find_path((self.xmap, self.ymap), (self.target.xmap, self.target.ymap), neighbors_fnct=neighbors_map(self.grid, self.target), heuristic_cost_estimate_fnct=cost, distance_between_fnct=dist)
            if path is not None:
                path = list(path)
                x, y = path[1]
                self.state = InnerState.WALK
                self.xori = self.xmap
                self.yori = self.ymap
                self.xmap = x
                self.ymap = y
                self.grid.cases[self.xori][self.yori][UNIT_LAYER] = None
                self.grid.cases[self.xmap][self.ymap][UNIT_LAYER] = self

    def set_inner_state(self, state):
        """
        Permet nottament de modifier l'état de l'unité
        comme étant 'THREAT', c'est à dire que l'unité
        est en train de se faire attaqué.
        """
        self.state = state

    def set_tree_state(self, state):
        """
        Fonction 'Changer état' pour l'arbre.
        """
        self.arbre.set_state(state)

    def select_target(self, target):
        """
        Fonction 'Selectionner cible' pour l'arbre.
        """
        if target == Target.NEAREST_ENEMY:
            self.target = self.grid.closest_unit(self, False)
        elif target == Target.NEAREST_ALLY:
            self.target = self.grid.closest_unit(self, True)
        elif target == Target.FARTHEST_ENEMY:
            self.target = self.grid.farthest_unit(self, False)
        elif target == Target.FARTHEST_ALLY:
            self.target = self.grid.closest_unit(self, True)
        elif target == Target.THREAT:
            self.target = self.lastLastUnit # représente la dernière unité à avoir attaqué cette unité
            if self.target is None:
                self.target = self.grid.closest_unit(self, False)
        elif target == Target.MAX_LIFE_ENEMY:
            self.target = self.grid.high_hp_unit(self, False)
        elif target == Target.MIN_LIFE_ENEMY:
            self.target = self.grid.low_hp_unit(self, False)
        elif target == Target.MAX_LIFE_ALLY:
            self.target = self.grid.high_hp_unit(self, True)
        elif target == Target.MIN_LIFE_ALLY:
            self.target = self.grid.low_hp_unit(self, True)
        elif target == Target.RANDOM_ENEMY:
            self.target = self.grid.high_hp_unit(self, False)
        elif target == Target.RANDOM_ALLY:
            self.target = self.grid.low_hp_unit(self, True)

    def shoot(self, param):
        """
        Fonction 'Attaquer' pour l'arbre.
        """
        if self.can_shoot():
            self.set_inner_state(InnerState.SHOOT)
            self.target.hp -= DOMMAGES_ATTAQUE
            self.target.is_attacked = True
            self.target.lastUnit = self
        else:
            self.set_inner_state(InnerState.FAILED)

    def heal(self, param):
        """
        Fonction 'Soin' pour l'arbre.
        """
        if self.target is not None and self.can_shoot():
            self.set_inner_state(InnerState.HEAL)
            self.target.hp += SOINS_ATTAQUE
        else:
            self.set_inner_state(InnerState.FAILED)

    def subit_attaque(self):
        """
        Fonction 'Menacé ?' pour l'arbre.
        """
        return "Oui" if self.is_attacked else "Non"

    def est_a_portee(self, param):
        """
        Fonction 'A portée' pour l'arbre.
        """
        if self.target is None:
            return "NO TARGET"
        return  "Oui" if ((dist((self.target.xmap, self.target.ymap), (self.xmap, self.ymap)) <= 3) and self.has_line_of_sight()) else "Non"

    def rotation_to_target(self):
        """
        Permet de faire pointer l'unité vers sa cible courante.
        """
        pos1 = pygame.Vector2(self.rect.centerx, self.rect.centery)
        pos2 = pygame.Vector2(self.target.rect.centerx, self.target.rect.centery)
        direction = pos2 - pos1
        y = pygame.Vector2(0, 1)
        return (180 - y.angle_to(direction)) % 360

    def am_i_dead(self, param):
        """
        On meurt lorsqu'on a plus de hp (no shit).
        """
        return self.hp <= 0

    def is_dead(self, param):
        """
        Fonction 'Est mort ?' pour l'arbre.
        """
        if self.target is None or self.target.am_i_dead(param):
            return "Oui"
        else:
            return "Non"

    def can_shoot(self):
        """
        On peut tirer que si on a bien une target, et qu'on a la ligne de vue
        sur celle ci.
        """
        if self.target is not None and self.has_line_of_sight():
                return True
        return False

    def has_line_of_sight(self):
        """
        Utilise un vecteur dirigé de l'unité à l'unité ciblée. Ce vecteur
        pointe toutes les cases sur lesquelles il passe en faisant la ligne
        droite d'une unité à l'autre.
        Si un obstacle est rencontré, on retourne False, sinon on retourne True.
        """
        vec = pygame.Vector2(self.target.xmap - self.xmap, self.target.ymap - self.ymap)
        longueur_chemin = vec.length()
        if longueur_chemin <= 0.2: # les deux unités sont déjà presque sur la même case, pas besoin de checker
            return True # sans ça, le normalize peut lancer une exception de division par 0


        vec = vec.normalize()/4 # vecteur petit, que l'on va faire grandir jusqu'à dépasser la longueur du chemin
        vec_n = vec.normalize()/4 # vecteur que l'on ajoute au vecteur initial pour le faire grandir
        while vec.length() < longueur_chemin:
            case = self.grid.cases[self.xmap + round(vec.x)][self.ymap + round(vec.y)][UNIT_LAYER]
            if case is not None:
                if case.collide and ((case != self.target) and (case != self)):
                    return False
            vec += vec_n

        return True

    def tick(self):
        """
        Actualise le comportement de l'unité.
        Réinitialise certaines variables qui ont
        une durée de vie que d'un tick.
        """
        self.tick_progress = 0
        if self.state == InnerState.WALK or self.state == InnerState.IDLE:
            self.xori = self.xmap
            self.yori = self.ymap
        self.arbre.eval()
        self.lastLastUnit = self.lastUnit
        self.lastUnit = None

        self.is_attacked = False

    def update(self):
        """
        Actualise l'unité en fonction de l'état dans lequel elle est.
        """
        if self.state != InnerState.DEAD:
            self.tick_progress += 1 / 60 / (TICK_TIME) # avance la valeur du tick, permet de savoir quand il faut actualiser le comportement
        if self.state != InnerState.DEAD and self.tick_progress > 1: # on actualise le comportement !
            self.tick()

        if self.hp <= 0 and self.state != InnerState.DEAD:
            self.image = self.image_dead
            self.state = InnerState.DEAD
            self.collide = False # une unité morte ne bloque pas le passage ni la ligne de vue
            self.grid.cases[self.xmap][self.ymap][UNIT_LAYER] = None
            self.grid.cases[self.xmap][self.ymap][DEAD_LAYER] = self

        if self.state == InnerState.DEAD:
            self.rotation = 0
        elif self.target is not None:
            self.rotation = 0.9 * self.rotation + 0.1 * self.rotation_to_target()

    def draw(self, screen, x, y):
        """
        Dessine l'unité en prenant en compte l'état dans
        lequel elle est.
        Dessine aussi les particules qu'elle emets.
        """
        if self.state == InnerState.WALK or self.state == InnerState.DEAD:
            x += (self.xori - self.xmap) * self.grid.cell_size * (1 - self.tick_progress) # tick_progress représente un pourcentage d'avancement
            y += (self.yori - self.ymap) * self.grid.cell_size * (1 - self.tick_progress)
        super().draw(screen, x, y) 

        if self.state != InnerState.DEAD: # dessine la barre de vie
            screen.fill((255, 0, 0), rect=pygame.Rect(self.rect.centerx - 32 + 15, self.rect.centery - 32 + 50, 34 , 5))
            screen.fill((0, 255, 0), rect=pygame.Rect(self.rect.centerx - 32 + 15, self.rect.centery - 32 + 50, int(34 * self.hp/self.hpmax), 5))

        if self.state in [InnerState.SHOOT, InnerState.HEAL] and self.target is not None and self.can_shoot():
            pos1 = pygame.Vector2(self.rect.centerx, self.rect.centery)
            pos2 = pygame.Vector2(self.target.rect.centerx, self.target.rect.centery)
            if pos1 != pos2: # pour ne pas normaliser un vecteur nul
                return

            direction = (pos2 - pos1).normalize()

            begin = pos1 +  direction * 23
            end = pos2 - direction * 11

            if self.state == InnerState.SHOOT: # dessine le tir d'attaque
                self.bullet_progress = (self.tick_progress * 4) % 2
                self.bullet_progress = 1 if self.bullet_progress > 1 else self.bullet_progress
                draw_progress_line(screen, begin, end, self.bullet_progress, 0.1, 0.9, (0, 0, 0))
            else: # dessine le tir de soin
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

def neighbors_map(carte, goal):
    """
    Retourne une fonction
    qui calcule les voisoins autour d'un
    point. Cette fonction retourne les points
    voisins ayant pour valeur la valeur goal
    donnée.
    """
    def neighbors(unit):
        l = []
        x, y = unit

        if x < (carte.width-1) and (carte.cases[x+1][y][UNIT_LAYER] is None or carte.cases[x+1][y][UNIT_LAYER] == goal or not carte.cases[x+1][y][UNIT_LAYER].collide):
            l.append((x+1, y))
        if x > 0 and (carte.cases[x-1][y][UNIT_LAYER] is None or carte.cases[x-1][y][UNIT_LAYER] == goal or not carte.cases[x-1][y][UNIT_LAYER].collide):
            l.append((x-1, y))
        if y < (carte.height-1) and (carte.cases[x][y+1][UNIT_LAYER] is None or carte.cases[x][y+1][UNIT_LAYER] == goal or not carte.cases[x][y+1][UNIT_LAYER].collide):
            l.append((x, y+1))
        if y > 0 and (carte.cases[x][y-1][UNIT_LAYER] is None or carte.cases[x][y-1][UNIT_LAYER] == goal or not carte.cases[x][y-1][UNIT_LAYER].collide):
            l.append((x, y-1))
        return l

    return neighbors


### Fonctions pour le pathfinding du astar
def cost(n, goal):
    """
    Fonction de coût basique.
    """
    return 1

def dist(u0, u1):
    """
    Distance euclidienne.
    """
    x0, y0 = u0
    x1, y1 = u1
    return ((x1 - x0)**2 + (y1 - y0)**2)**0.5
