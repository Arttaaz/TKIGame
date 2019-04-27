"""
Ennemi.
"""
import pygame
from enum import Enum
from gameobject import GameObject

class State(Enum):
    IDLE = 1
    SHOOT = 2
    DEAD = 3
bullet_time = 0.3

class Unit(GameObject):

    def __init__(self, image, id = 1, collide = True):
        GameObject.__init__(self, image, id, collide)
        self.state = State.SHOOT
        self.target = None
        self.hp = 100
        self.bullet_progress = 0
        self.start_shooting_time = 0
        self.start_shooting = False
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
            self.bullet_progress += 1 / 60 / (bullet_time)

            if self.bullet_progress > 1:
                self.bullet_progress = 0
                self.target.hp -= 10
        if self.hp < 0:
            self.state = State.DEAD
            self.rotation += 1
            
    def draw(self, screen, x, y):
        super().draw(screen, x, y)

        if self.state == State.SHOOT and self.target is not None:
            pos1 = pygame.Vector2(self.rect.centerx, self.rect.centery)
            pos2 = pygame.Vector2(self.target.rect.centerx, self.target.rect.centery)
            dir = (pos2 - pos1).normalize()
            begin = pos1 +  dir * 23
            end = pos2 - dir * 11

            if self.bullet_progress < 0.1:
                p1 = begin
            else:
                t = (self.bullet_progress - 0.1) / 0.9
                p1 = (1 - t) * begin + t * end
            if self.bullet_progress > 0.9:
                p2 = end
            else:
                t = self.bullet_progress / 0.9
                p2 = (1 - t) * begin + t * end
            
            
            pygame.draw.aaline(screen, (0, 0, 0), (p1.x, p1.y),
                                (p2.x, p2.y))


