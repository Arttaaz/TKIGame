"""
Ennemi.
"""
from enum import Enum

class State(Enum):
    IDLE = 1
    FOLLOW = 2
    
    
class Unit(pygame.sprite.Sprite):

    def __init__(self, pos, speed):
        pygame.sprite.Sprite.__init__(self)

        self.pos = pos
        self.speed = speed

    def follow(self, target):
        
        
    def update(self, collisions):
        self
