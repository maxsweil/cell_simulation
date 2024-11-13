import pygame
import random
from itertools import chain
import uuid
import numpy as np

N_OBJS = 30
SEED = 3

# TESTING SPECIFIC OBJECTS #
#OBJS = {(1114, 133):(-2, 4), (970, 640):(0, 4),}

random.seed(SEED)

# N_OBJ >= 2, SEED = 3 for collision testing

class sim_game():
    def __init__(self, surface, width=1920, height=1080):

        # Initializing game surface
        self.surface = surface
        self.width = width
        self.height = height

        # Initializing some physics
        self.coll_coef = 0.96

        # TESTING SPECIFIC OBJECTS #
        #self.objs = [foo(self.width, self.height, pos, velo) for pos,velo in OBJS.items()]

        # Initializing game objects
        self.objs = [foo(self.width, self.height, 1, 1) for i in range(N_OBJS)]

    def draw_objs(self):
        """
        Method for drawing game objects
        """
        for obj in self.objs:
            obj.render(self.surface)
    
    def update_objs(self):
        """
        Method to update object between frames
        """
        # Updating x position
        for obj in self.objs:
            new_loc = [obj.rect.x+obj.x_velo, obj.rect.y]
            obj.update_loc(*new_loc, save_frame=1)
        
        # Checking for collisions after x update and flagging
        x_colls = [obj.check_collisions({tuple(o.rect):o for o in self.objs if o != obj}) for obj in self.objs]

        # Updating y position
        for obj in self.objs:
            new_loc = [obj.rect.x, obj.rect.y+obj.y_velo]
            obj.update_loc(*new_loc, save_frame=1)
        
        # Checking for collisions after y update and flagging
        y_colls = [obj.check_collisions({tuple(o.rect):o for o in self.objs if o != obj}) for obj in self.objs]

        # Creating dictionary to store all collisions
        colls = {}
        
        # Iterating over all x and y collisions
        for origin, rects in chain((('x', coll) for coll in chain.from_iterable(x_colls)),
                                (('y', coll) for coll in chain.from_iterable(y_colls))):
            unique_coll = tuple(sorted(rects, key=lambda x: x.id))
            # If unique collision is not in collision dict, add it
            if unique_coll not in colls.keys():
                colls[unique_coll] = origin

        # Resolving collisions
        for coll, origin in colls.items():
            self.resolve_collisions(coll, origin)


    def resolve_collisions(self, coll, direction):
        """
        Method for resolving collision in x and/or y direction
        """
        if direction=='x':
            coll[0].rect.x, coll[1].rect.x = coll[0].last_rect.x, coll[1].last_rect.x # Revert y-position to last frame's y-position
            velos = (coll[0].x_velo, coll[1].x_velo)
            if np.prod(velos)<0:
                coll[0].bounce(1,0)
                coll[1].bounce(1,0)
            coll[0].x_velo, coll[1].x_velo = round(self.coll_coef*velos[1], 2), round(self.coll_coef*velos[0], 2)
        elif direction=='y':
            coll[0].rect.y, coll[1].rect.y = coll[0].last_rect.y, coll[1].last_rect.y # Revert y-position to last frame's y-position
            velos = (coll[0].y_velo, coll[1].y_velo)
            if np.prod(velos)<0:
                coll[0].bounce(0,1)
                coll[1].bounce(0,1)
            coll[0].y_velo, coll[1].y_velo = round(self.coll_coef*velos[1], 2), round(self.coll_coef*velos[0], 2)


class foo():
    def __init__(self, screen_width, screen_height, pos, velo):
        # Initializing object id
        self.id = uuid.uuid4()

        # Initializing color and size
        self.color = (85, 200, 215)
        self.size = 30
        
        # Setting screen bounds
        self.x_min = 0
        self.y_min = 0
        self.x_max = screen_width - self.size
        self.y_max = screen_height - self.size

        # TESTING SPECIFIC OBJECTS #
        """self.x_velo = velo[0]
        self.y_velo = velo[1]
        self.rect = pygame.Rect(*pos, self.size, self.size)"""

        # Initializing veocity and object as pygame rectangle
        self.x_velo = random.randint(-5, 5)
        self.y_velo = random.randint(-5, 5)
        self.rect = pygame.Rect(random.randint(0, self.x_max), random.randint(0, self.y_max), self.size, self.size)
        self.last_rect = self.rect.copy()

    def update_loc(self, new_x, new_y, save_frame):
        """
        Method for updating the location of object
        """
        if save_frame:
            self.last_rect = self.rect.copy()
        self.rect.update(max(min(new_x, self.x_max), self.x_min),
                         max(min(new_y, self.y_max), self.y_min),
                         self.size,
                         self.size)
        
        if (self.rect.x >= self.x_max) or (self.rect.x <= self.x_min):
            self.rect.x = self.last_rect.x
            self.bounce(1,0)
        if (self.rect.y >= self.y_max) or (self.rect.y <= self.y_min):
            self.rect.y = self.last_rect.y
            self.bounce(0,1)

    def bounce(self, x, y):
        """
        Method for reversing the x and/or y direction of object
        """
        if x:
            self.x_velo *= -1
        if y:
            self.y_velo *= -1

    def check_collisions(self, oth_rects):
        """
        Method for checking if object is colliding with a list of other objects
        """
        coll = self.rect.collidedictall(oth_rects)
        #return coll
        if coll:
            return [(self, c[1]) for c in coll] # Return list of tuples, containing self and objects that rectangle collided with
        else:
            return []

    def render(self, surface):
        """
        Method to render object on surface
        """
        pygame.draw.rect(surface, self.color, self.rect)
        
    
