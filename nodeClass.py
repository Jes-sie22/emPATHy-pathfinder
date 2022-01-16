import colorspy as colors
import pygame
# Class for the individual blocks/nodes in the grid
class Node:
    # Attributes 
    def __init__(self,row,col,width,total_rows):
        self.row = row
        self.col = col
        # coordinates by pixels
        self.x = row * width 
        self.y = col * width 
        self.color = colors.white
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    # method to get position in rows# and col#
    def get_pos(self):
        return self.row, self.col

    # IS METHODS - methods to identify the state of a block// returns : T or F
    # blocks is not open for algorithm to run
    def is_closed(self):
        return self.color == colors.red

    # block is open for algorithm to look at
    def is_open(self):
        return self.color == colors.green
    
    # block is a barrier
    def is_barrier(self):
        return self.color == colors.black

    # block is start block
    def is_start(self):
        return self.color == colors.orange

    # block is end block
    def is_end(self):
        return self.color == colors.turquoise

    
    # MAKE METHODS - to update state of a block (color coded)
    # making a block red to show closed for algorithm
    def make_closed(self):
        self.color = colors.red

    # making a block green to show open for algorithm
    def make_open(self):
        self.color = colors.green

    def make_barrier(self):
        self.color = colors.black

    def make_start(self):
        self.color = colors.orange
    
    def make_end(self):
        self.color = colors.turquoise
    
    def make_path(self):
        self.color = colors.purple

    # reset
    def reset(self):
        self.color = colors.white

    # drawing the block
    def draw(self, window):
        pygame.draw.rect(window,self.color,(self.x,self.y,self.width,self.width))

    def update_neighbors(self, grid):
        # initializing neighbors-of-a-block list
        self.neighbors = []
        # check whether up,down,left,right blocks of nth block are barriers
        if self.row < self.total_rows-1 and not grid[self.row+1][self.col].is_barrier(): # check if can move DOWN 
            self.neighbors.append(grid[self.row+1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): # check if can move UP 
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows-1 and not grid[self.row][self.col+1].is_barrier(): # check if can move RIGHT 
            self.neighbors.append(grid[self.row][self.col+1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): # check if can move LEFT 
            self.neighbors.append(grid[self.row][self.col - 1])

    # less than  - compare 2 blocks ?
    def __lt__(self, other):
        return False