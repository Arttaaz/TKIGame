"""
Objet représenté sur la carte.
C'est un objet parent, dont d'autres
objets peuvent hériter pour ajouter
des fonctionnalités (dont l'objet 'Unit')
"""


import pygame


class GameObject:
    def __init__(self, image, grid, xmap, ymap, id_obj=0, collide=False):
        self.image = image # image représentant l'objet sur la map
        self.image_to_draw = image # image_to_draw subit des modifications de l'image avant d'être dessinée
        self.grid = grid
        self.xmap = xmap
        self.ymap = ymap
        self.collide = collide # est-ce que l'objet est de type bloquant ?
        self.rotation = 0 # tourne l'image dans le bon sens
        self.rect = image.get_rect()
        self.id = id_obj
        self.last_rotation = 0 # permet d'éviter de tourner deux fois l'image alors qu'on en a pas besoin

    def update(self):
        """
        Fonction qu'on par défaut tout les objets.
        On la créé là pour ne pas créer d'erreurs
        lorsqu'on appel sans réfléchir cette méthode (car
        certains objets n'ont pas besoin de update).
        """
        pass

    def draw(self, screen, x, y):
        """
        Dessine l'objet sur la carte,
        effectue une rotation de l'image avant,
        si nécéssaire.
        """
        if self.last_rotation != self.rotation:
            self.last_rotation = self.rotation
            self.image_to_draw = pygame.transform.rotate(self.image, self.rotation)
        self.rect = self.image_to_draw.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        screen.blit(self.image_to_draw, self.rect)

    def __str__(self):
        return str(self.id)
