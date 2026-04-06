# grid.py

class Grid:
    def __init__(self, width, height, obstacle_map):
        self.width = width
        self.height = height
        self.map = obstacle_map  # 2D list of 0/1
        self.listeners = []      # drones that want notifications

    def get_dimensions(self):
        return self.width, self.height

    def is_obstacle(self, x, y):
        return self.map[y][x] == 1

    def get_neighbors(self, x, y):
        neighbors = []
        directions = [(1,0), (-1,0), (0,1), (0,-1)]

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.width and 0 <= ny < self.height:
                if not self.is_obstacle(nx, ny):
                    neighbors.append((nx, ny))

        return neighbors

    def add_listener(self, drone):
        self.listeners.append(drone)

    def add_obstacle(self, x, y):
        if self.map[y][x] == 1:
            return  # already an obstacle

        self.map[y][x] = 1

        # notify all drones
        for drone in self.listeners:
            if hasattr(drone, "on_new_obstacle"):
                drone.on_new_obstacle(x, y)
