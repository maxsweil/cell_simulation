import pygame
import random
N_OBJS = 11
SEED = 3
random.seed(SEED)

# N_OBJ >= 2, SEED = 3 for collision testing

class sim_game():
    def __init__(self, surface, width=1920, height=1080, scale=10):
        self.surface = surface
        self.width = width
        self.height = height
        self.scale = scale
        self.objs = [foo(self.width, self.height) for i in range(N_OBJS)]

    def draw_objs(self):
        for obj in self.objs:
            obj.render(self.surface)
    
    def update_objs(self):
        # Updating x position
        for obj in self.objs:
            new_loc = [obj.rect.x+obj.x_velo, obj.rect.y]
            obj.update_loc(*new_loc, save_frame=1)
        
        # Checking for collisions after x update and flagging
        x_colls = [obj.check_collisions({tuple(o.rect):o.x_velo for o in self.objs if o != obj}) for obj in self.objs]

        # Updating y position
        for obj in self.objs:
            new_loc = [obj.rect.x, obj.rect.y+obj.y_velo]
            obj.update_loc(*new_loc, save_frame=1)
        
        # Checking for collisions after y update and flagging
        y_colls = [obj.check_collisions({tuple(o.rect):o.y_velo for o in self.objs if o != obj}) for obj in self.objs]

        # Resolving collisions
        for obj, x_coll, y_coll in zip(self.objs, x_colls, y_colls):
            obj.resolve_collisions(x_coll, y_coll)


        

class foo():
    def __init__(self, screen_width, screen_height):
        self.color = (85, 200, 215)
        self.size = 30
        
        self.x_min = 0
        self.y_min = 0
        self.x_max = screen_width - self.size
        self.y_max = screen_height - self.size

        self.x_velo = random.randint(-5, 5)
        self.y_velo = random.randint(-5, 5)

        #self.x_velo = -1
        #self.y_velo = 1
        #self.rect = pygame.Rect(5, 5, self.size, self.size)

        self.rect = pygame.Rect(random.randint(0, self.x_max), random.randint(0, self.y_max), self.size, self.size)
        self.last_rect = self.rect.copy()

    def update_loc(self, new_x, new_y, save_frame):
        if save_frame:
            self.last_rect = self.rect.copy()
        self.rect.update(max(min(new_x, self.x_max), self.x_min),
                         max(min(new_y, self.y_max), self.y_min),
                         self.size,
                         self.size)

    def bounce(self, x, y):
        if x:
            self.x_velo *= -1
        if y:
            self.y_velo *= -1

    def check_collisions(self, oth_rects):
        coll = self.rect.collidedict(oth_rects)
        if coll:
            return coll[1]
        else:
            return False

    def resolve_collisions(self, x_coll, y_coll):

        # Resolving collisions with other rects
        if x_coll:
            self.rect.x = self.last_rect.x
            if x_coll*self.x_velo<=0:
                self.bounce(1,0)
        elif y_coll:
            self.rect.y = self.last_rect.y
            if y_coll*self.y_velo<=0:
                self.bounce(0,1)

        # Resolving collisions with boundaries
        if (self.rect.x >= self.x_max) or (self.rect.x <= self.x_min):
            self.rect.x = self.last_rect.x
            self.bounce(1,0)
        if (self.rect.y >= self.y_max) or (self.rect.y <= self.y_min):
            self.rect.y = self.last_rect.y
            self.bounce(0,1)
        self.last_rect = self.rect
            
        '''if (self.rect.top >= col_hitbox.bottom or self.rect.bottom <= col_hitbox.top) and (self.rect.right < col_hitbox.left or self.rect.left > col_hitbox.right):
            self.bounce(0,1)
        if (self.rect.right >= col_hitbox.left or self.rect.left <= col_hitbox.right):# and (self.rect.top < col_hitbox.bottom or self.rect.bottom > col_hitbox.top):
            self.bounce(1,0)'''


    def render(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        
    
