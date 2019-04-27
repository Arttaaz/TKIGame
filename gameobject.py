import pygame
class GameObject:

    def __init__(self, image, grid, id = 0,  collide=False):
        self.image = image
        self.grid = grid
        self.collide = collide
        self.rotation = 0
        self.rect = image.get_rect()
        self.id = id
    def update(self, map):
        pass

    def draw(self, screen, x, y):
        image = pygame.transform.rotate(self.image, self.rotation)
        self.rect = image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        screen.blit(image, self.rect)

    def __str__(self):
        return str(self.id)
