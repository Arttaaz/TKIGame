import sys, pygame
from map import Map
from enum import Enum
from state import State, GameState

pygame.init()

size = width, height = 800, 800
black = 0, 0, 0

clock = pygame.time.Clock()
screen = pygame.display.set_mode(size)
path = "assets/map.map"
map = Map(64, path=path, depth=1)

while 1:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYUP:
            print(event.key)

    map.update()
    screen.fill(black)
    map.draw(screen, screen.get_width() / 2, screen.get_height() / 2)
    pygame.display.flip()
