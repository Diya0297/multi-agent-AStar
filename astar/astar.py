from astar import node 
import heapq


def A_STAR(inital_state, goal_state, h_function):
    '''
    Use Priority Queue to implement search logic 

    ARGS:
        inital_state: current board -> list
        goal_state: goal board -> list
        h_function: one of the h(n) functions
    
    RETURN:
        path, expansion_count: sequence of actions to reach goal, total number of nodes the alg looked at -> tuple 
    '''
    #initalize starting node
    start_node = node.Node(state =inital_state, g=0, h=h_function(inital_state, goal_state))

    #create frontier list to hold tuples of each nodes (f,Node)
    frontier = [(start_node.f,start_node)]
    #frontier_status to keep track of neighbour status
    frontier_states = {inital_state: start_node.g}

    #set to hold explored nodes
    explored = set()

    #while frontier is not empty:
    while frontier:

        #Pop node n with the lowest f
        _, current_node = heapq.heappop(frontier)
        state = current_node.state

        #if n = goal, return reconstructed path to the current node, len(explored)
        if state == goal_state:
            return get_path(current_node), len(explored)

        #make sure not to explore the same node twice
        if state in explored:
            continue
        #add node to explored 
        explored.add(state)

        if state in frontier_states:
            del frontier_states[state]
            
        #check neighbours for every move from the current position and calc cost 
        for action, neighbour_state in get_neighbours(state):
            #Update g by 1 for every neighbour
            new_g = current_node.g + 1

            #if neighbour is not in frontier update explored
            if neighbour_state not in explored and neighbour_state not in frontier_states:
                h_value = h_function(neighbour_state, goal_state)
                neighbour_node = node.Node(neighbour_state, current_node, action, new_g, h_value)

                #insert to frontier, and update frontier states
                heapq.heappush(frontier, (neighbour_node.f, neighbour_node))
                frontier_states[neighbour_state] = new_g



            #else if neighbour is in frontier 
            elif neighbour_state in frontier_states:

                #if current path is better than previous one in frontier, update
                if new_g < frontier_states[neighbour_state]:
                    h_value = h_function(neighbour_state, goal_state)
                    neighbour_node = node.Node(neighbour_state, current_node, action, new_g, h_value)
                    #insert to frontier, and update frontier states
                    heapq.heappush(frontier, (neighbour_node.f, neighbour_node))
                    frontier_states[neighbour_node] = new_g
                     

    return None, len(explored)

def get_neighbours(state):
    '''
    Helper function that returns list of (actions, neightbour_states) tuples
    
    :param state: current board
    '''
    #initalize neighbours, index, row, column, moves
    neighbours = []
    i = state.index(0)
    row, column = i//3, i %3
    moves = {"Up": (row-1,column), "Down": (row+1, column), "Left": (row, column-1), "Right": (row, column+1)}

    #loop through the possible combinations, and add them to neighbours
    for actions, (new_r, new_c) in moves.items():

        #if 0 <= new r < 3 AND 0 <= new c < 3
        if 0 <= new_r < 3 and 0 <= new_c < 3:
            new_i = new_r * 3 + new_c

            #swap index and new index
            temp = list(state)
            temp[i], temp[new_i] = temp[new_i], temp[i]

            #add actions and temp to neighbours 
            neighbours.append((actions,tuple(temp)))
            
    return neighbours

def get_path(node):
    '''
    Helper function returns the reconstructed path to given node
    
    :param node: current node
    '''
    path = []

    while node.parent:
        path.append(node.actions)
        node = node.parent

    return path[::-1]