# parser.py

from grid.grid import Grid

def load_input_file(path):
    with open(path, "r") as f:
        lines = [line.strip() for line in f if line.strip() and not line.startswith("//")]

    # 1. Grid dimensions
    height, width = map(int, lines[0].split())

    # 2. Number of robots
    num_robots = int(lines[1])

    # 3. Robot positions
    robots = []
    index = 2
    for _ in range(num_robots):
        x, y = map(int, lines[index].split())
        robots.append((x, y))
        index += 1

    # 4. Rendezvous point
    rx, ry = map(int, lines[index].split())
    index += 1

    # 5. Obstacle map
    obstacle_map = []
    for i in range(height):
        row = [int(c) for c in lines[index + i]]
        obstacle_map.append(row)

    grid = Grid(width, height, obstacle_map)

    return grid, robots, (rx, ry)
