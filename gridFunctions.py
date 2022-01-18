import colorspy as colors
import pygame 
from nodeClass import Node

# making the grid w 2d lists
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
    
    # # calling method on individual blocks to draw 
    for row in grid:
        for spot in row:
            spot.draw(window) 

    # calling function to draw gridlines 
    draw_grid(window,rows,width)
    pygame.display.update()