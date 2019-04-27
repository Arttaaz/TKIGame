import pygame, sys

class GameState(Enum):
    MENU            = 0
    BEFORE_SIMU     = 1
    SIMU            = 2


# Current game state is always last element of self.state
class State:
    def __init__(self, screen, map):
        self.state = [GameState.BEFORE_SIMU] # TODO: change to MENU when menu exists
        self.screen = screen
        self.map = map


    # Add state to the stack when creating new state
    # pop state from the stackif leaving state
    def start(self):
        while 1:
            if self.state[len(self.state)-1] == GameState.MENU:
                self.state = [GameState.BEFORE_SIMU]

            elif self.state[len(self.state)-1] == GameState.BEFORE_SIMU:
                self.update()
                self.draw()

            elif self.state[len(self.state)-1] == GameState.SIMU:
                pass
            else:
                sys.exit()


    # check events only for current state
    def event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()


    #draw all states onto screen in order first to current (except menu)
    def draw(self):
        self.screen.fill(black)

        for state in self.state:
            if state == GameState.BEFORE_SIMU:
                self.map.draw(self.screen, self.screen.get_width() / 2, self.screen.get_height() / 2)

        pygame.display.flip()

    #update current state
    def update(self):
        if self.state[len(self.state)-1] == GameState.BEFORE_SIMU:
            self.map.update()
