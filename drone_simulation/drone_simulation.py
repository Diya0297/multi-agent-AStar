import copy
from astar import A_STAR, manhatten

class Grid:
    def __init__(self, size):
        self.size = size
        self.obstacles = set()

    def add_obstacle(self, position):
        self.obstacles.add(tuple(position))

    def is_obstacle(self, position):
        return tuple(position) in self.obstacles


#building a class drone which will store the position, path and its own known map
class Drone:
    def __init__(self, drone_id, start_position, destination, grid):
        self.id = drone_id  #each drone will have a unique id
        self.position = start_position #current position of the drone
        self.destination = destination #destination 
        self.grid = grid #map

        self.path=[] #this will be the path from current position to destination position
        self.obstacles_known = set() #obstacles that the drone knows about
        self.known_grid = copy.deepcopy(grid) #this is drone's personal version of the map
        self.plan_for_path()

    def plan_for_path(self): #this calls A* to compute a path from current to destination
        #fake grid representation for A*
        self.path, _ = A_STAR(tuple(self.position), tuple(self.destination), manhatten)

    def next_position(self):
        if not self.path:
            return self.position #no shift if no path exists
        return self.path[0] #returns next step in the path without shifting yet
    
    def shift(self):
        if self.path:
            self.position = self.path.pop(0) #shifts the drone one step forward and also remove that step

    def detect_obstacle(self, position, message_queue):
        if position not in self.obstacles_known:
            message_queue.append({
                "type": "obstacle",
                "position": position,
                "sender": self.id
            })

    def process_messages(self, message_queue):
        for message in message_queue:
            if message["type"] == "obstacle":
                position = message["position"]
                if position not in self.obstacles_known:
                    self.obstacles_known.add(position)
                    self.known_grid.add_obstacle(position)
                    self.replan_as_required(position)

    def replan_as_required(self, obstacle_position):
        if obstacle_position in self.path:
            self.plan_for_path()


#this is a basic collision avoidance function using cell reservation
#if two drones want the same cell, one waits a tick so only one drone per cell
def collision_avoidance(moves):
    seen={}
    final_moves ={}
    for drone_id, position in moves.items():
        if position not in seen: #no collision so drone gets the cell
            seen[position] = drone_id
            final_moves[drone_id] = position
        else:
            final_moves[drone_id] = None #in this case collision occurs, so the drone waits
    return final_moves



#building a simulaiton loop (all drones move one step per tick simultaneously)
def simulation(drones, max_steps=50):
    message_queue = [] #shared message queue to communicate
    for step in range(max_steps):
        #there will be 3 steps as follows:
        #1: decide moves
        moves={}
        for drone in drones:
            moves[drone.id] = drone.next_position()

        #2: resolve collisions (this method is defined below)
        moves = collision_avoidance(moves)

        #3: shift/move drones
        for drone in drones:
            if moves[drone.id] is not None: #prevents collision
                drone.position = moves[drone.id]
                if drone.path:
                    drone.path.pop(0) #shifts the drone one step forward and also remove that step
        
        #4: process messages
        for drone in drones:
            drone.process_messages(message_queue)
        message_queue.clear() #now we will clear all messages after all drones have read them

def update_simulation(drones, message_queue):
    #1 - decide moves
    moves = {drone.id: drone.next_position() for drone in drones}

    #2 - resolve collisions
    moves = collision_avoidance(moves)

    #3 - move drones
    for drone in drones:
        if moves[drone.id] is not None:
            drone.position = moves[drone.id]
            if drone.path:
                drone.path.pop(0)
    
    #4 - process messages
    for drone in drones:
        drone.process_messages(message_queue)

    message_queue.clear()



    