"""
Ennemi.
"""
import pygame
from enum import Enum
from gameobject import GameObject

class State(Enum):
    IDLE = 1
    SHOOT = 2
    
    
class Unit(GameObject):

    def __init__(self, image, id = 1, collide = True):
        GameObject.__init__(self, image, id, collide)
        self.state = State.SHOOT
        self.target = None
    def follow(self, target):
        pass

    def rotation_to_target(self):
        
        pos1 = pygame.Vector2(self.rect.centerx, self.rect.centery)
        pos2 = pygame.Vector2(self.target.rect.centerx, self.target.rect.centery)
        dir = pos2 - pos1
        y = pygame.Vector2(0, 1)
        return( 180 - y.angle_to(dir)) % 360

    def update(self, map):
        
        if map.units[0] != self:
            self.target = map.units[0]

        if self.state == State.SHOOT and self.target is not None:
            self.rotation = 0.9 * self.rotation + 0.1 * self.rotation_to_target()

    def draw(self, screen, x, y):
        super().draw(screen, x, y)

        #if self.state == State.SHOOT and self.target is not None:
            #pygame.draw.aalines(screen, (0, 0, 0), (self.rect.centerx, self.rect.centery)
    
