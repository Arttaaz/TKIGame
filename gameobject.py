import pygame
class GameObject:

    def __init__(self, image, grid, xmap, ymap, id = 0,  collide=False):
        self.image = image
        self.image_to_draw = image
        self.grid = grid
        self.xmap = xmap
        self.ymap = ymap
        self.collide = collide
        self.rotation = 0
        self.rect = image.get_rect()
        self.id = id
        self.last_rotation = 0
    def update(self, map):
        pass

    def draw(self, screen, x, y):
        if self.last_rotation != self.rotation:
            self.last_rotation = self.rotation
            self.image_to_draw = pygame.transform.rotate(self.image, self.rotation)
        self.rect = self.image_to_draw.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        screen.blit(self.image_to_draw, self.rect)

    def __str__(self):
        return str(self.id)
