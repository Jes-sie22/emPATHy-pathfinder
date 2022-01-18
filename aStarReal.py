import pygame
from queue import PriorityQueue
from djikstras import reconstruct_path

# A* algo - heuristic function in f(n)=h(n)+g(n) - manhattan distance
def h(p1,p2): # p1/p2 = (row,col) eg. p1 = (1,9) , x1= 1, y1=9
    x1,y1 = p1
    x2,y2 = p2 
    return abs(x1-x2) + abs(y1-y2) # abs turns negative to positive -> math symbol: ||


# A* pathfinding algorithm
def aStarAlgo(draw,grid,start,end):
    # initializing variables -> improvement use dict??
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