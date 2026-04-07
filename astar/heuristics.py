def euclidean(currPos, grid):
    '''
    Straight distance between two positions on a grid

    ARGS:
        currPos: current board -> list
        grid: goal board -> list

    RETURN:
        total_distance -> int
    '''
    return ((currPos[0]- grid[0])**2 + (currPos[1]- grid[1])**2 )** 0.5

def manhatten_grid(currPos, grid):
    '''
    Manhatten distance between two positions on a grid

    ARGS:
        currPos: current position -> tuple
        goal: goal position -> tuple

    RETURN:
        total_distance -> int
    '''

    return abs(currPos[0] - grid[0]) + abs(currPos[1] - grid[1])

