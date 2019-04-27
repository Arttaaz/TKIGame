import sys, pygame
from map import Map

pygame.init()

size = width, height = 800, 800
black = 0, 0, 0

clock = pygame.time.Clock()
screen = pygame.display.set_mode(size)
path = "assets/map.map"
map = Map(64, path=path, depth=1)

object = map.cases[4][4][1]

while 1:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYUP:
            print(event.key)
            if event.key == pygame.K_RIGHT:
                object.team = 2

    map.update()
    screen.fill(black)
    map.draw(screen, screen.get_width() / 2, screen.get_height() / 2)
    pygame.display.flip()
