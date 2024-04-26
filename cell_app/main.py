import sys
import pygame
from pygame.locals import *
from src import game
WIDTH = 1280
HEIGHT = 720

class run_game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Cell Sim")
        
        # It sets the display mode and creates an instance of the pygame.Surface class.
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        self.surface = pygame.Surface(self.window.get_size())
        self.surface = self.surface.convert()
        self.surface.fill((0, 0, 0))
        self.game = game.sim_game(self.surface, WIDTH, HEIGHT, scale=20)

        self.clock = pygame.time.Clock()
        self.fps = 30
        self.RUNNING = True
        self.PAUSE = False

    def game_loop(self):
        self.clock.tick(self.fps) # It keeps the game running at a constant FPS.
        self.game.update_objs() # It updates our grid or universe.
        self.surface.fill((0, 0, 0)) # Reset surface with background color
        self.game.draw_objs() # It draws our grid or universe.
        self.window.blit(self.surface, (0,0)) # Draw surface onto window
        pygame.display.flip() # It updates the full display surface to the window.
        self.check_events() # It checks all the events.
        

    def check_events(self): # Pygame handles all its event messaging through an event queue. This method checks all these events.
        # If not paused, run as usual
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.RUNNING = False
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.RUNNING = False
                if event.key == K_SPACE:
                    self.PAUSE = not self.PAUSE

        # If paused, freeze running, allow single frame movement with right arrow key
        # Quitting or escape key will break out of pausing to end the game
        while self.PAUSE:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.RUNNING = False
                    return
                if event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        self.PAUSE = not self.PAUSE
                    if event.key == K_ESCAPE:
                        self.RUNNING = False
                        return
                    if event.key == K_RIGHT:
                        return

if __name__ == '__main__':
    game_instance = run_game()
    while game_instance.RUNNING:
        game_instance.game_loop()

    pygame.quit()
    sys.exit()