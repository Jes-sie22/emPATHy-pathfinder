import imp
import pygame
import colorspy as colors
from queue import PriorityQueue
from nodeClass import Node # node objects to change color
from gridFunctions import * # drawing grid on window functions
from djikstras import *
from aStarReal import *

# pygame setup
pygame.init()

WIDTH = 800
WINDOW = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption('em-PATH-y pathfinding algrorithm visualizer')

# function to take mouse position and return which block on grid its on 
def get_clicked_position(mouse_pos,rows,width):
    gap = width//rows
    y,x = mouse_pos

    row = y // gap
    col = x // gap

    return row,col

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
                pygame.quit()

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
                
                # get A* running
                if event.key == pygame.K_a and start and end: # start pathfinding algorithm when start and end blocks available
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)
                    
                    
                    aStarAlgo(lambda: draw(window,grid,ROWS,width), grid, start, end) 
                    # lambda is an anonymous function - > to pass draw function as an argument to another function 
                
                # get dijkstras running
                if event.key == pygame.K_d and start and end:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)
                            
                    dijkstraAlgo(lambda: draw(window,grid,ROWS,width),grid,start,end)


                if event.key == pygame.K_c: # clear the screen
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)

    

main(WINDOW,WIDTH)


