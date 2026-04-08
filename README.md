# multi-agent-AStar
Disaster Drone Simulation (using A* pathfinding)
    A multi-agent simulation of rescue drones navigating a collapsed building using A* alg. 

Running the Simulation
    1. install pygame 
    2. run the project main using; python visual/visual.py
    3. pygame window will open and drones will start immediately
    4. click anywhere on the grid to spawn debris in that cell (causing drones to replan)

Changing the Map
    Open visual/visual.py and change the LAYOUT variable near the top
    
Map File Format
    Maps are .txt files & format is as follows:
    20 20 //rows cols
    3     // number of drones
    1 1   // drone 1 start
    18 1  // drone 2 start
    10 18 // drone 3 start
    10 10 // rendezvous point
    00100100010001... // grid rows top to bottom (0 = open, 1 = obstacle)
    11100111110001...
    ...

    IMPORTANT: the parser in visual.py automatically converts to (row, col) for internal grid.

Changing Heuristic
    In drone_simulation/drone_simulation.py, find plan_for_path and swap the heuristic in line 45 (where it calls A_STAR(_,_,_, heuristic))

IF DRONES ARE STUCK
    1. check that the rendezvous point in map file is not on an obstacle cell
    2. check that drones start positions are not on an obstacle cell
    3. increase max_steps on simulation function in drone_simulation/drone_simulation.py (this is for if map is large)
    
