import sys, pygame

pygame.init()

size = width, height = 800, 800
black = 0, 0, 0

screen = pygame.display.set_mode(size)

while 1:
    for event in pygame.event.get():
        if event == pygame.QUIT:
            sys.exit()

    screen.fill(black)
    pygame.display.flip()
