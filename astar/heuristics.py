def euclidean(state, goal):
    '''
    Count how many tiles (not including the blank) are in the WRONG index

    ARGS:
        state: current board -> list
        goal: goal board -> list

    RETURN:
        count: number of tiles in target index -> int
    '''
    n = len(state)
    i = 0
    count = 0
    while i < n:
        if state[i] != 0 and state[i] != goal[i]:
            count +=1
        i +=1
    
    return count

def manhatten(state, goal):
    '''
    For each tile calculate the Manhatten Distance (abs(x1-x2) + abs(y1-y2))

    ARGS:
        state: current board -> list
        goal: goal board -> list

    RETURN:
        total_dist: total number of steps all tiles need to move to reach goal position -> int
    '''
    total_dist = 0

    for i in range(len(state)):
        tile = state[i]

        #if the tile isnt 0, count the distance from goal tile
        if tile != 0:
            #set coords of state tile 
            state_x, state_y = i//3, i%3

            #get index on the goal board of the tile 
            goal_i = goal.index(tile)
            #set coords of goal tile 
            goal_x, goal_y = goal_i//3, goal_i%3

            #calc Manhatten Distance
            total_dist += abs(state_x-goal_x) + abs(state_y-goal_y)

    return total_dist

def weightedManhattan(state, goal):
    '''
    h3 = Manhattan Distance + 2 * (number of linear conflicts)
    Linear conflict happens when two tiles are in the same row/column,
    belong in that row/column in the goal, but appear in the wrong order.
    '''

    # compute the Manhattan distance
    manhattan = manhatten(state, goal)
    conflicts = 0

    '''Checks for any conflicts in each row'''
    for row in range(3):

        # Extract the 3 tiles in this row 
        # row=0 → tiles 0,1,2 
        # row=1 → tiles 3,4,5 
        # row=2 → tiles 6,7,8
        row_tiles = state[row*3:(row+1)*3]

        # Compare every pair of tiles in this row
        for i in range(3):
            for j in range(i+1, 3):

                
                tile1 = row_tiles[i]
                tile2 = row_tiles[j]

                # ignore if tiles are blank
                if tile1 != 0 and tile2 != 0:

                    # find the goal state for tile 1
                    goal_i1 = goal.index(tile1)

                    # find the goal state for tile 2
                    goal_i2 = goal.index(tile2)

                   # Check if BOTH tiles belong in THIS SAME ROW in the goal 
                   # goal_i1 // 3 gives the goal row of tile1 
                   # goal_i2 // 3 gives the goal row of tile2
                    if goal_i1 // 3 == row and goal_i2 // 3 == row:

                        # check if tile1 should be on the right of tile 2 but is on left which indicates conflict
                        if goal_i1 > goal_i2:
                            conflicts += 1

    '''Check for any coloum conflicts'''
    for col in range(3):
        col_tiles = [state[col], state[col+3], state[col+6]]

        for i in range(3):
            for j in range(i+1, 3):
                tile1 = col_tiles[i]
                tile2 = col_tiles[j]

                if tile1 != 0 and tile2 != 0:
                    goal_i1 = goal.index(tile1)
                    goal_i2 = goal.index(tile2)

                    # Check if both tiles belong in THIS SAME COLUMN in the goal 
                    # goal_i1 % 3 gives the goal column of tile1 
                    # goal_i2 % 3 gives the goal column of tile2
                    if goal_i1 % 3 == col and goal_i2 % 3 == col:
                      
                        if goal_i1 > goal_i2:
                            
                            conflicts += 1

    return manhattan + 2 * conflicts
