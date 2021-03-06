import sys, pygame
from unit import Unit
from map import Map
import dimensions
pygame.init()

size = width, height = dimensions.LONGUEUR_FENETRE, dimensions.HAUTEUR_FENETRE
black = 0, 0, 0

screen = pygame.display.set_mode(size)


clock = pygame.time.Clock()

path = "assets/tuto2.map"
map = Map(64, path = path)
layer = 0
while 1:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            print(event.key)
            if event.key == pygame.K_s:
                print(event.key)
                map.write_file(path)
            if event.key == pygame.K_l:
                map = Map(64, path = path)
            if event.key == pygame.K_RIGHT:
                print(layer)
                layer += 1
                if layer >= map.depth:
                    map.resize(depth = layer + 1)
            if event.key == pygame.K_LEFT:
                layer -= 1
                if layer < 0:
                    layer = 0
        if event.type == pygame.MOUSEBUTTONDOWN:
            map_pos_x, map_pos_y = (map.world_to_map_x(int(event.pos[0] - screen.get_width() / 2)),
                           map.world_to_map_y(int(event.pos[1] - screen.get_height() / 2)))
            id = map.id(int(map_pos_x), int(map_pos_y), layer)
            if event.button == 3:
                if id > 0:
                    id -= 1
            elif event.button == 1:
                id += 1

            map.remove(map_pos_x, map_pos_y, layer)
            map.cases[map_pos_x][map_pos_y][layer] = map.generate_object(str(id) + ";1", map_pos_x, map_pos_y)



    screen.fill(black)

    map.draw(screen, screen.get_width() / 2, screen.get_height() / 2)
    pygame.display.flip()
