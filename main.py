import sys, pygame
from map import Map

pygame.init()

size = width, height = 800, 800
black = 0, 0, 0

clock = pygame.time.Clock()
screen = pygame.display.set_mode(size)
path = "assets/map.map"
map = Map(64, path=path, depth=1)

map.cases[4][2][1] = map.generate_object(2, 4, 2)
map.cases[6][5][1] = map.generate_object(2, 6, 5)

while 1:
    clock.tick(60)
    for event in pygame.event.get():
        if event == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYUP:
            print(event.key)
            if event.key == pygame.K_RIGHT:
                map.cases[4][2][1].move(map.cases[6][5][1])
    map.update()
    screen.fill(black)
    map.draw(screen, screen.get_width() / 2, screen.get_height() / 2)
    pygame.display.flip()
