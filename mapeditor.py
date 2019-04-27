import sys, pygame
from unit import Unit
from map import Map
pygame.init()

size = width, height = 800, 800
black = 0, 0, 0

screen = pygame.display.set_mode(size)


clock = pygame.time.Clock()
path = "assets/map.map"
map = Map(64, path = path)
layer = 0
while 1:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYUP:
            print(event.key)
            if event.key == pygame.K_s:
                print(event.key)
                map.write_file(path)
            if event.key == pygame.K_l:
                map = Map(30, path = path)
            if event.key == pygame.K_RIGHT:
                print(layer)
                layer += 1
                if layer >= map.depth:
                    map.resize(depth = layer + 1)
            if event.key == pygame.K_LEFT:
                layer -= 1
        if event.type == pygame.MOUSEBUTTONDOWN:
            map_pos_x, map_pos_y = (map.world_to_map_x(int(event.pos[0] - screen.get_width() / 2)),
                           map.world_to_map_y(int(event.pos[1] - screen.get_height() / 2)))
            id = map.id(int(map_pos_x), int(map_pos_y), layer)
            if event.button == 3:
                if id > 0:
                    id -= 1
            elif event.button == 1:
                id += 1
                
            map.cases[map_pos_x][map_pos_y][layer] = map.generate_object(id)



    map.update()
    screen.fill(black)

    map.draw(screen, screen.get_width() / 2, screen.get_height() / 2)
    pygame.display.flip()
    
