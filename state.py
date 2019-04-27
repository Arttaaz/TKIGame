import pygame, sys
from enum import Enum
from gerer_arbre import GererArbre

class GameState(Enum):
    MENU            = 0
    BEFORE_SIMU     = 1
    SIMU            = 2
    ARBRE           = 3

clock = pygame.time.Clock()
black = 0, 0, 0

# Current game state is always last element of self.state
class State:
    def __init__(self, screen, map):
        self.state  = [GameState.BEFORE_SIMU] # TODO: change to MENU when menu exists
        self.screen = screen
        self.map    = map


    # Add state to the stack when creating new state
    # pop state from the stackif leaving state
    def start(self):
        while 1:
            clock.tick(60)
            if self.state[len(self.state)-1] == GameState.MENU:
                self.state = [GameState.BEFORE_SIMU]


            self.event()
            self.update()
            self.draw()


    # check events only for current state
    def event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if self.state[len(self.state)-1] == GameState.BEFORE_SIMU:
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        map_pos_x, map_pos_y = (self.map.world_to_map_x(int(event.pos[0] - self.screen.get_width() / 2)),
                                       self.map.world_to_map_y(int(event.pos[1] - self.screen.get_height() / 2)))
                        if self.map.cases[map_pos_x][map_pos_y][1] is not None:
                            self.tree = GererArbre(self.screen, self.map.cases[map_pos_x][map_pos_y][1].arbre)
                            self.tree.boucle_principale()

                    elif event.button == 3:
                        self.state.append(GameState.SIMU)

    #draw all states onto screen in order first to current (except menu)
    def draw(self):
        self.screen.fill(black)

        for state in self.state:
            if state == GameState.BEFORE_SIMU or state == GameState.SIMU:
                self.map.draw(self.screen, self.screen.get_width() / 2, self.screen.get_height() / 2)

        pygame.display.flip()

    #update current state
    def update(self):
        if self.state[len(self.state)-1] == GameState.SIMU:
            self.map.update()
