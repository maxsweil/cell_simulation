import pygame
import random
import copy
ALIVE = True
DEATH = False
DEATH_COLOR = (50, 50, 50)
OFFSET = 1

class Cell:
    def __init__(self, id):
        self.status = ALIVE
        self.changeId(id)
        
    def changeId(self, newId = None):
        if newId==None:
            self.id = random.randint(0, 4)
        else:
            self.id = newId

        self.color = [(255,0,0), (0,0,255), (255,255,0), (0,255,0), (255, 192, 203)][self.id]
        
    def isAlive(self):
        return self.status == ALIVE

    def __str__(self) -> str:
        return str(self.status) + "," + str(self.id)

    def copy(self, status):
        myCopy = Cell(self.id)
        myCopy.status = status
        return myCopy
    
    def isPredator(self, neighbor):
        return neighbor.id==(self.id + 1) % 5 or neighbor.id==(self.id + 2) % 5

    def isPrey(self, neighbor):
        return neighbor.id==(self.id + 3) % 5 or neighbor.id==(self.id + 4) % 5

    def turnPrey(self):
        myCopy = Cell( (self.id + random.randint(3, 4)) % 5 )
        myCopy.status = self.status
        return myCopy

    def turnPredator(self):
        myCopy = Cell( (self.id + random.randint(1, 2)) % 5 )
        myCopy.status = self.status
        return myCopy

class GameofLife:
    def __init__(self, surface, width=1920, height=1080, scale=10):
        self.surface = surface
        self.width = width
        self.height = height
        self.scale = scale
        self.columns = int(height / scale)
        self.rows = int(width / scale)
        # The _universe is a two-dimensional grid of cells_, each of which is in one of two possible states: alive or dead.
        self.grid = [[Cell((c+r)%5) for c in range(self.columns)] for r in range(self.rows)]
        
    def draw_grid(self):
        """ It draws the grid."""
        for row in range(self.rows):
            for col in range(self.columns):
                if self.grid[row][col].isAlive():
                    pygame.draw.rect(self.surface, self.grid[row][col].color, [row * self.scale, col * self.scale, self.scale - OFFSET, self.scale - OFFSET])
                else: # It is not really necessary, all cells on the grid are alive.
                    pygame.draw.rect(self.surface, DEATH_COLOR, [row * self.scale, col * self.scale, self.scale - OFFSET, self.scale - OFFSET])
    
    def update_grid(self):
        """ It updates the grid based on Rock Paper Scissors Lizard and Spock rules."""
        updated_grid = copy.deepcopy(self.grid)
        for row in range(self.rows):
            for col in range(self.columns):
                updated_grid[row][col] = self.update_cell(row, col)

        self.grid = updated_grid

    
    def cell_neighbors(self, x, y):
        """ It returns the number of the current or active cell's (self.grid[x, y]) neighbors that are predators and the number of its neighbors that are prey."""
        predators_neighbors = 0
        prey_neighbors = 0

        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0: # The cell does not count itself as a neighbour. I am not my neighbour!
                    continue
                elif (x+i)<0 or (x+i)>=self.rows or (y+j)<0 or (y+j)>=self.columns: # The neighbour cell needs to be on the grid.
                    continue
                elif self.grid[x + i][y + j].isAlive() and self.grid[x][y].isPredator(self.grid[x + i][y + j]): # If the neighbour cell is alive and it is one of the current cell predators, we increase the variable predators_neighbors by 1.
                    predators_neighbors += 1
                elif self.grid[x + i][y + j].isAlive() and self.grid[x][y].isPrey(self.grid[x + i][y + j]): # If the neighbour cell is alive and it is one of the current cell preys, we increase the variable prey_neighbors by 1.
                    prey_neighbors += 1
        
        return predators_neighbors, prey_neighbors

    def update_cell(self, x, y):
        """ It updates the cell based on Rock Paper Scissors Lizard and Spock rules."""
        predators_neighbors, pray_neighbors = self.cell_neighbors(x, y)
        current_state = self.grid[x][y].status
        threshold = 3 + random.randint(0, 2)
        # Rather than checking if the winning neighbor count (the number of the current cell neighbors that are predators) is greater than a specified threshold, we are going to check if it is greater than a threshold plus a small random amount (random.randint(0, 2)).
        
        if current_state==ALIVE and predators_neighbors >= threshold:
            return self.grid[x][y].turnPredator()
        # We can also check if the losing neighbor count is greater than a threshold plus a small random amount, and if this is the case, turn the current or active cell into prey. However, these are different ways of designing our simulation. It is up to you to evaluate and decide which is the best model or rules to be chosen. 
        # elif current_state==ALIVE and pray_neighbors >= threshold:
        #    return self.grid[x][y].turnPrey()
        else:
            return self.grid[x][y].copy(current_state)