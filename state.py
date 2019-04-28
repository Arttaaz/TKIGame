import pygame, sys
from enum import Enum
from gerer_arbre import GererArbre
from unit import UNIT_LAYER, Unit
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
        self.arbre_surface = pygame.Surface((screen.get_width(), screen.get_height()))  # the size of your rect
        self.map    = map
        self.modifs_arbres = {}
        self.select_pos = None
        self.clicking = False

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
            if self.state[len(self.state)-1] == GameState.ARBRE:
                if self.tree.handle_event(event):
                    self.modifs_arbres[self.selected] = self.tree.get_modifs()
                    self.state.pop()
            if self.state[len(self.state)-1] == GameState.BEFORE_SIMU:
                if event.type == pygame.MOUSEMOTION:
                    map_pos_x, map_pos_y = (self.map.world_to_map_x(int(event.pos[0] - self.screen.get_width() / 2)),
                                            self.map.world_to_map_y(int(event.pos[1] - self.screen.get_height() / 2)))
                    object = self.map.cases[map_pos_x][map_pos_y][UNIT_LAYER]
                    if isinstance(object, Unit):
                        self.select_pos = (self.map.map_to_world_x(map_pos_x), self.map.map_to_world_y(map_pos_y))
                    else:
                        self.select_pos = None
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.clicking = True
                if event.type == pygame.MOUSEBUTTONUP:
                    self.clicking = False
                    if event.button == 1:
                        map_pos_x, map_pos_y = (self.map.world_to_map_x(int(event.pos[0] - self.screen.get_width() / 2)),
                                       self.map.world_to_map_y(int(event.pos[1] - self.screen.get_height() / 2)))
                        object = self.map.cases[map_pos_x][map_pos_y][UNIT_LAYER]
                        if isinstance(object, Unit):
                            if object not in self.modifs_arbres:
                                self.tree = GererArbre(self.screen, object.arbre)
                            else:
                                self.tree = GererArbre(self.screen, object.arbre, self.modifs_arbres[object])
                            self.selected = object
                            self.state.append(GameState.ARBRE)

                    elif event.button == 3:
                        for unit in self.modifs_arbres:
                            for modif in self.modifs_arbres[unit]:
                                modif.effectuer_modification()
                        self.state.append(GameState.SIMU)

    #draw all states onto screen in order first to current (except menu)
    def draw(self):
        self.screen.fill((255, 255, 255))

        for state in self.state:
           if state == GameState.BEFORE_SIMU or state == GameState.SIMU:
                self.map.draw(self.screen, self.screen.get_width() / 2, self.screen.get_height() / 2)
        if state == GameState.ARBRE:
            self.tree.render()

        if state == GameState.BEFORE_SIMU:
            if self.select_pos is not None:
                rect = pygame.Rect(0, 0, self.map.cell_size, self.map.cell_size)
                rect.centerx, rect.centery = self.screen.get_width() / 2 + self.select_pos[0], self.screen.get_height() / 2 + self.select_pos[1]

                if self.clicking:
                    s = pygame.Surface((self.map.cell_size, self.map.cell_size))  # the size of your rect
                    s.set_alpha(128) # alpha level
                    s.fill((0,0,0), rect = pygame.Rect(0, 0, self.map.cell_size, self.map.cell_size))           # this fills the entire surface
                    self.screen.blit(s, (rect.left, rect.top))

                pygame.draw.rect(self.screen, pygame.Color(255, 0, 0, 50), rect, 2)
        pygame.display.flip()

    #update current state
    def update(self):
        if self.state[len(self.state)-1] == GameState.SIMU:
            self.map.update()

        if self.state[len(self.state)-1] == GameState.ARBRE:
            self.tree.update()
