import sys
import pygame
from pygame.locals import *
from src import game
WIDTH = 1280
HEIGHT = 1024

class Game: # It represents the game itself
    def __init__(self):
        pygame.init()  # It initializes all imported pygame modules.
        pygame.display.set_caption("Conway's Game of Life") # It sets the current window tittle.
         # It sets the display mode and creates an instance of the pygame.Surface class.
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT)) 
        self.conway = game.GameofLife(self.screen, scale=13)
        self.clock = pygame.time.Clock()  # A pygame.time.Clock object helps us to make sure our program runs at a certain FPS.
        self.fps = 60 # This is our frame rate. It is expressed in frames per second or FPS. It is the frequency or rate at which consecutive images or frames are captured or displayed in the game.
        self.running = True # It indicates that the game is still running.

    def gameLoop(self):
        self.clock.tick(self.fps) # It keeps the game running at a constant FPS. 
        self.screen.fill((0, 0, 0)) # It fills the whole screen with black.
        self.checkEvents() # It checks all the events.
        self.conway.draw_grid() # It draws our grid or universe.
        self.conway.update_grid() # It updates our grid or universe.
        pygame.display.update() # It updates the full display surface to the screen.

    def checkEvents(self): # Pygame handles all its event messaging through an event queue. This method checks all these events.
        for event in pygame.event.get(): # It gets events from the queue.
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == KEYDOWN: # A key is physically pressed on.
                    if event.key == K_ESCAPE: # The ESC key was pressed.
                        self.running = False

if __name__ == '__main__':
    game = Game() # The main function is quite simple. We create an instance of our Game class.
    while game.running: # It loops while the game is still running.
        game.gameLoop() # We call the game's game_loop function.

    pygame.quit()
    sys.exit()