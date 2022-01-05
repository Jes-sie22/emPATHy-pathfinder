from types import GeneratorType
import colorspy as colors
import pygame
import math
from queue import PriorityQueue
from pygame import mouse

from pygame.constants import K_SPACE, WINDOWHITTEST

pygame.init()# initializing pygame

# creating a window, adding caption
WIDTH = 800
WINDOW = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption('A* Path Finding Algorithm')

# class for the cubes of the grid
class Node:
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

    # method to get rows and colums
    def get_pos(self):
        return self.row, self.col

    # IS METHODS - methods to identify the state of a block && update state of a block // returns : T or F
    # method which identifies blocks we are not looking at anymore == RED blocks
    def is_closed(self):
        return self.color == colors.red

    # block is open for algorithm to look at
    def is_open(self):
        return self.color == colors.green
    
    # block is a barrier
    def is_barrier(self):
        return self.color == colors.black

    # start block
    def is_start(self):
        return self.color == colors.orange

    # end block
    def is_end(self):
        return self.color == colors.turquoise
    
    # reset
    def reset(self):
        self.color = colors.white

    # MAKE METHODS - transform block color
    def make_closed(self):
        self.color = colors.red
    
    # open
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

    # drawing the block
    def draw(self, window):
        pygame.draw.rect(window,self.color,(self.x,self.y,self.width,self.width))

    def update_neighbors(self, grid):
        # initializing neighbors list
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


# heuristic function in f(n)=h(n)+g(n) - manhattan distance
def h(p1,p2): # p1/p2 = (row,col) eg. p1 = (1,9) , x1= 1, y1=9
    x1,y1 = p1
    x2,y2 = p2 
    return abs(x1-x2) + abs(y1-y2) # abs turns negative to positive -> math symbol: ||

def reconstruct_path(previous, current, draw):
    while current in previous:
        current = previous[current]
        current.make_path()
        draw()

def algorithm(draw,grid,start,end):
    # initializing variables 
    count = 0 
    open_set = PriorityQueue() # get smallest element out first
    open_set.put((0, count,start))# append set
    previous = {}
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0
    f_score = {spot: float("inf") for row in grid for spot in row}
    f_score[start] = h(start.get_pos(),end.get_pos())

    open_set_hash = {start} # for prioritizing blocks in queue 

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current  = open_set.get()[2] # get node from open set
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(previous,end,draw)
            end.make_end()
            return True
        
        # neighbors of the current node
        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1  # unweighted edges 

            if temp_g_score < g_score[neighbor]:
                previous[neighbor] = current # update previous
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())

                if neighbor not in open_set_hash:
                    count +=1
                    open_set.put((f_score[neighbor],count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        draw()

        # close of / remove from unvisited list current node
        if current != start :
            current.make_closed()
    
    return False


    

# function making the grid w 2d lists
def make_grid(rows, width):
    grid = []
    gap = width // rows # gap = insides of square 

    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Node(i,j,gap,rows)
            grid[i].append(spot)

    return grid

# drawing grid LINES
def draw_grid(window,rows,width):
    gap = width //rows
    # drawing horizontal lines 
    for i in range(rows):
        pygame.draw.line(window, colors.gray,(0, i * gap),(width, i * gap))
        # drawing vertical lines
        for j in range(rows):
            pygame.draw.line(window,colors.gray, (j*gap,0),(j*gap, width))

# function to call drawing functions to DRAW FRESH CANVAS 
def draw(window,grid,rows,width):
    # filling the screen with 1 color
    window.fill(colors.white)
    
    # calling function to draw indivdual blocks
    for row in grid:
        for spot in row:
            spot.draw(window)  # calling method on individual blocks to draw # loop thoorugh rows and grid to draw all the spots

    # calling function to draw gridlines 
    draw_grid(window,rows,width)
    pygame.display.update()

# function to take mouse position and return which block on grid its on 
def get_clicked_position(mouse_pos,rows,width):
    gap = width//rows
    y,x = mouse_pos

    row = y // gap
    col = x // gap

    return row,col

# MAIN function
def main(window,width):
    ROWS = 50
    grid = make_grid(ROWS,width)

    # initializing start and end position
    start = None
    end = None

    # running the main loop or not
    run = True
    # started the algorithm or not
    started = False

    while run:
        # calling draw function 
        draw(window,grid,ROWS,width)

        for event in pygame.event.get():
            # user clicks quit
            if event.type == pygame.QUIT:
                run = False

            # mouse actions
            if pygame.mouse.get_pressed()[0]: # index 0 is LEFT CLICK
                pos = pygame.mouse.get_pos()
                row,col = get_clicked_position(pos, ROWS,width) # call function to get the actual block clicked on
                spot = grid[row][col]

                # assigning start block-> update start variable,change block color
                if not start and spot != end: # make sure start/end does not overlap
                    start = spot
                    start.make_start()
                # assigning end block-> update end variable with coordinates, change block color
                elif not end and spot != start:
                    end = spot
                    end.make_end()

                # clicking any other spot than start/end
                elif spot != end and spot != start:
                    spot.make_barrier()

            elif pygame.mouse.get_pressed()[2]: # index 2 is RIGHT CLICK
                # getting block row n column
                pos = pygame.mouse.get_pos()
                row,col = get_clicked_position(pos,ROWS,width)
                spot = grid[row][col]
                spot.reset()

                # reseting start/end blocks 
                if spot == start:
                    start = None 
                if spot == end:
                    end = None


            if event.type == pygame.KEYDOWN: # KEYDOWN = did user press a key on keyboard
                if event.key == pygame.K_SPACE and start and end: # start pathfinding algorithm when start and end blocks available
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)


                    algorithm(lambda: draw(window,grid,ROWS,width), grid, start, end) # lambda is an anonymous function - > to pass draw function as an argument to another function 
                
                if event.key == pygame.K_c: # clear the screen
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)

    pygame.quit()

main(WINDOW,WIDTH)
        
# position: row,column
# width: draw itself 
# neightbouring nodes