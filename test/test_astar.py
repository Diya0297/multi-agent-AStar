import time 
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from astar.astar import A_STAR
from astar.heuristics import manhatten_grid, euclidean

'''helpers'''
def make_empty_grid(rows, cols):
    ans = []
    for _ in range(rows):
        ans.append([0]*cols)
    return ans


def print_path_on_grid(grid,path,start,goal):
    vis = [row[:] for row in grid]
    for (r,c) in path:
        if (r,c) != start and (r,c) != goal:
            vis[r][c] = 2
    for row in vis:
        print(" ".join(["#" if c ==1 else "G" if c ==2 else "." for c in row]))

'''test 1 (no obstacles)'''
def test_no_obs():
    print("\n Test 1: no obstacles")
    grid = make_empty_grid(5,5)
    path, expansions = A_STAR((0,0), (4,4), grid, manhatten_grid)
    assert path is not None, "should find a path"
    assert path[0] == (0,0), "path should start at start"
    assert path[-1] == (4,4), "path should end at goal"
    print(f" Path: {path}")
    print(f" Nodes expanded: {expansions}")
    print(f" PASSED")

'''test 2 (obstacle wall with gap)'''
def test_obstacle_wall():
    print("\n Test 2: wall with gap")
    grid = make_empty_grid(5,5)
    for r in range(4):
        grid[r][2] = 1
    path, expansions = A_STAR((0,0),(0,4),grid,manhatten_grid)
    assert path is not None, "should find a path around wall"
    assert path[-1] == (0,4)
    print(f" Path: {path}")
    print_path_on_grid(grid,path,(0,0), (0,4))
    print(f" Nodes expanded: {expansions}")
    print(" PASSED")

'''test 3 (no path exists)'''
def test_no_path():
    print("\n Test 3: no path exists")
    grid = make_empty_grid(5,5)
    for r in range(5):
        grid[r][2] = 1
    path, expansions = A_STAR((0,0),(0,4),grid,manhatten_grid)
    assert path is None, "should return None when no path"
    print(f" Path: {path}")
    print(f" Nodes expanded: {expansions}")
    print(f" PASSED")

'''test 4 (start is the goal)'''
def test_start_is_goal():
    print("\n Test 4: start is the goal")
    grid = make_empty_grid(5,5)
    path, expansions = A_STAR((2,2),(2,2),grid,manhatten_grid)
    assert path is not None
    assert len(path) == 1 or path[-1] == (2,2)
    print(f" Path: {path}")
    print(" PASSED")

'''test 5 (comparing heuristics)'''
def test_compare_heuristics():
    print("\n Test 5: Manhattan vs Euclidean")
    #Set up stuff
    grid = make_empty_grid(20,20)
    obs = [(5,5),(5,6),(5,7), (5,8), (10,3), (10,4), (10, 5), (15,12), (15,13)]
    for (r,c) in obs:
        grid[r][c] = 1
    start, goal = (0,0), (19,19)

    #time each
    t0 = time.time()
    path_m, exp_m = A_STAR(start,goal,grid,manhatten_grid)
    t1 = time.time()
    path_e, exp_e = A_STAR(start,goal,grid,euclidean)
    t2 = time.time()

    print(f" Manhattan \n   path length: {len(path_m)}, node expanded: {exp_m}, time: {(t1-t0)*1000:.2f}ms")
    print(f" Eulidean  \n   path length: {len(path_e)}, node expanded: {exp_e}, time: {(t2-t1)*1000:.2f}ms")
    print(" PASSED")

'''test 6 (scalability)'''
def test_scalability():
    print("\n Test 6: scalability across grid sizes")
    sizes = [ 10,20, 50, 100]
    for size in sizes:
        grid = make_empty_grid(size,size)
        #adding obstical cluster in middle
        mid = size//2
        for i in range(-3,4):
            if 0 <= mid+i < size:
                grid[mid][mid+i] = 1

        start, goal = (0,0) , (size-1, size -1)
        t0 = time.time()
        path, expansions = A_STAR(start,goal, grid, manhatten_grid)
        t1 = time.time()
        print(f" {size}x{size} \n   path length: {len(path) if path else 'None'}, ")
        print(f"nodes expanded: {expansions}, time: {(t1-t0)*1000:.2f}ms")
    print(" PASSED")

'''run'''
if __name__ == "__main__":
    test_no_obs()
    test_obstacle_wall()
    test_no_path()
    test_start_is_goal()
    test_compare_heuristics()
    test_scalability()
    print("\n all tests passed")