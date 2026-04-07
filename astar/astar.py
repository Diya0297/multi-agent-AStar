from astar.node import Node
from astar.heuristics import manhatten_grid
import heapq


def A_STAR(start, goal, grid, h_function = manhatten_grid):
    '''
    Use Priority Queue to implement search logic 

    ARGS:
        start: start position -> list
        goal: goal position -> list
        grid: 2D list, 0 = open 1 = blocked -> List[List[int]] 
        h_function: heuristic function -> callable from astar.heuristics file
    
    RETURN:
        path, expansion_count -> tuple 
    '''
    #initalize starting node
    start_node = Node(state =start, g=0, h=h_function(start, goal))

    #create frontier list to hold tuples of each nodes (f,Node)
    frontier = [(start_node.f,start_node)]
    #frontier_status to keep track of neighbour status
    frontier_states = {start: 0}

    #set to hold explored nodes
    explored = set()

    #while frontier is not empty:
    while frontier:

        #Pop node n with the lowest f
        _, current_node = heapq.heappop(frontier)
        state = current_node.state

        #if n = goal, return reconstructed path to the current node, len(explored)
        if state == goal:
            return get_path(current_node), len(explored)

        #make sure not to explore the same node twice
        if state in explored:
            continue
        #add node to explored 
        explored.add(state)

        if state in frontier_states:
            del frontier_states[state]
            
        #check neighbours for every move from the current position and calc cost 
        for action, neighbour_state in get_neighbours(state, grid):
            #Update g by 1 for every neighbour
            new_g = current_node.g + 1

            #if neighbour is not in frontier update explored
            if neighbour_state not in explored and neighbour_state not in frontier_states:
                h_value = h_function(neighbour_state, goal)
                neighbour_node = Node(neighbour_state, current_node, action, new_g, h_value)

                #insert to frontier, and update frontier states
                heapq.heappush(frontier, (neighbour_node.f, neighbour_node))
                frontier_states[neighbour_state] = new_g



            #else if neighbour is in frontier 
            elif neighbour_state in frontier_states:

                #if current path is better than previous one in frontier, update
                if new_g < frontier_states[neighbour_state]:
                    h_value = h_function(neighbour_state, goal)
                    neighbour_node = Node(neighbour_state, current_node, action, new_g, h_value)
                    #insert to frontier, and update frontier states
                    heapq.heappush(frontier, (neighbour_node.f, neighbour_node))
                    frontier_states[neighbour_state] = new_g
                     

    return None, len(explored)

def get_neighbours(currPos, grid):
    '''
    Helper function that returns list of (actions, neightbour_states) tuples
    
    :param state: current board
    '''
    #initalize neighbours, index, row, column, moves
    rows, columns = len(grid), len(grid[0])
    row, col = currPos
    neighbours = []

    #loop through the possible combinations, and add them to neighbours
    for dr, dc, action in [(-1,0, "up"), (1,0, "down"), (0,-1, "left"), (0,1, "right")]:

        new_r, new_c = row + dr, col + dc

        if 0 <= new_r < rows and 0 <= new_c < columns:
            if grid[new_r][new_c] == 0:
                neighbours.append((action,(new_r, new_c)))
            
    return neighbours

def get_path(node):
    '''
    Helper function returns the reconstructed path to given node
    
    :param node: current node
    '''
    path = []

    while node.parent:
        path.append(node.state)
        node = node.parent

    path.append(node.state)

    return path[::-1]
