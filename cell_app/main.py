import sys
import pygame
from pygame.locals import *
from src import game
WIDTH = 1280
HEIGHT = 720

class run_game:
    def __init__(self):

        # Initializing game window
        pygame.init()
        pygame.display.set_caption("Cell Sim")
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))

        # Creating surface for window and filling with black
        self.surface = pygame.Surface(self.window.get_size())
        self.surface = self.surface.convert()
        self.surface.fill((0, 0, 0))

        # Initializing game with surface
        self.game = game.sim_game(self.surface, WIDTH, HEIGHT)

        # Initializing game clock, runspeed, and running/pause states
        self.clock = pygame.time.Clock()
        self.fps = 30
        self.RUNNING = True
        self.PAUSE = False

    def game_loop(self):
        """
        Method for running game
        """

        # Run game as designated fps
        self.clock.tick(self.fps)

        # Update all objects
        self.game.update_objs()

        # Reset surface with background color
        self.surface.fill((0, 0, 0))

        # Draw all objects on surface and blit surface onto window
        self.game.draw_objs()
        self.window.blit(self.surface, (0,0))

        # Update display
        pygame.display.flip()

        # Check for any pause or quit events
        self.check_events()
        

    def check_events(self):
        """
        Method for checking pause or quit events
        """

        # Check for pause or quit events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.RUNNING = False
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.RUNNING = False
                if event.key == K_SPACE:
                    self.PAUSE = not self.PAUSE

        # If paused, stop running, allow single frame advancement with right arrow key
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

    # Running game loop
    game_instance = run_game()
    while game_instance.RUNNING:
        game_instance.game_loop()
    pygame.quit()
    sys.exit()