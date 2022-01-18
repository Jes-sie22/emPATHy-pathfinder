import pygame
from queue import PriorityQueue
from nodeClass import Node

# function to draw shortest path
def reconstruct_path(previous, current, draw):
    while current in previous:
        current = previous[current]
        current.make_path()
        draw()

# function for dijkstra's pathfinding algorithm 
def dijkstraAlgo(draw,grid,start,end):
    open_set = PriorityQueue() # for unvisited
    open_set.put((0,start))# append set
    previous_node = {}
    # initialize costs for all nodes in cost dict
    cost = {spot: float("inf") for row in grid for spot in row}
    cost[start] = 0 # cost of start node = 0

    open_set_hash = {start}
    
    while not open_set.empty(): # repeat the following steps until unvisited list is empty
        # quit function 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        # get node with minnimum cost  from open_set or unvisted
        current = open_set.get()[1] 
        if current == end:
            reconstruct_path(previous_node,end,draw)
            end.make_end()
            return True

        # neighbors of current node
        for neighbor in current.neighbors: 
            temp_cost = cost[current] + 1

            if temp_cost < cost[neighbor]:
                cost[neighbor] = temp_cost
                previous_node[neighbor] = current # update previous node of neighbor

                if neighbor not in open_set_hash:
                    open_set.put((cost[neighbor], neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open() 
        draw()
        # remove current node from unvisited list?? and make red 
        if current != start:
            current.make_closed() # red
    return False