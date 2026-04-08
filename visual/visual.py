import pygame
import sys
import os

# IMPORT TEAM CODE
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from drone_simulation.drone_simulation import Drone, Grid, collision_avoidance

# CONFIG
CELL_SIZE = 25

BACKGROUND = (25, 25, 30)
GRID_DOT = (60, 60, 70)
OBSTACLE_COLOR = (220, 50, 50)
GOAL_COLOR = (50, 220, 50)

DRONE_COLORS = [(50, 150, 255), (255, 200, 50), (200, 100, 255), (255, 100, 100)]
DRONE_RADIUS = 6
GLOW_RADIUS = 12
LAYOUT = "medium_collapse.txt"

# FILE PATH
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(BASE_DIR, LAYOUT)


# PARSER 
def parse_input(file_path):
    with open(file_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    rows, cols = map(int, lines[0].split())
    n = int(lines[1])

    # Convert (x,y) to (row,col)
    def convert(x, y):
        return (rows - 1 - y, x)

    # Drone positions
    drone_positions = []
    for i in range(n):
        x, y = map(int, lines[2 + i].split())
        drone_positions.append(convert(x, y))

    # Goal
    gx, gy = map(int, lines[2 + n].split())
    goal = convert(gx, gy)

    # Grid using teammate class
    grid = Grid(rows, cols)

    grid_lines = lines[3 + n:]
    for r, line in enumerate(grid_lines):
        for c, val in enumerate(line):
            if val == "1":
                grid.add_obstacle((r, c))

    return grid, drone_positions, goal, rows, cols

#  LOAD
grid, drone_starts, goal, ROWS, COLS = parse_input(file_path)

WIDTH = COLS * CELL_SIZE
HEIGHT = ROWS * CELL_SIZE

# INIT PYGAME 
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("A* Drone Simulation")
clock = pygame.time.Clock()

# DRONES 
drones = [
    Drone(i + 1, start, goal, grid)
    for i, start in enumerate(drone_starts)
]

# DRAW 
def draw_grid():
    for r in range(ROWS):
        for c in range(COLS):
            px = c * CELL_SIZE + CELL_SIZE // 2
            py = r * CELL_SIZE + CELL_SIZE // 2

            if grid.is_obstacle((r, c)):
                pygame.draw.circle(screen, OBSTACLE_COLOR, (px, py), 5)
            else:
                pygame.draw.circle(screen, GRID_DOT, (px, py), 2)

def draw_goal():
    r, c = goal
    px = c * CELL_SIZE + CELL_SIZE // 2
    py = r * CELL_SIZE + CELL_SIZE // 2
    pygame.draw.circle(screen, GOAL_COLOR, (px, py), DRONE_RADIUS)

def draw_drones():
    for drone, color in zip(drones, DRONE_COLORS):

        # Draw path
        for step in drone.path:
            px = step[1] * CELL_SIZE + CELL_SIZE // 2
            py = step[0] * CELL_SIZE + CELL_SIZE // 2
            pygame.draw.circle(screen, (50, 220, 50), (px, py), 4)

        # Current position
        r, c = drone.position
        px = c * CELL_SIZE + CELL_SIZE // 2
        py = r * CELL_SIZE + CELL_SIZE // 2

        # Glow
        for i in range(GLOW_RADIUS, DRONE_RADIUS, -2):
            alpha = int(60 * (i - DRONE_RADIUS) / (GLOW_RADIUS - DRONE_RADIUS))
            surf = pygame.Surface((i * 2, i * 2), pygame.SRCALPHA)
            pygame.draw.circle(surf, (*color, alpha), (i, i), i)
            screen.blit(surf, (px - i, py - i))

        pygame.draw.circle(screen, color, (px, py), DRONE_RADIUS)


# SIMULATION
move_delay = 250
last_move_time = 0
message_queue = []

def update_simulation():
    global last_move_time
    current_time = pygame.time.get_ticks()

    if current_time - last_move_time > move_delay:
        active_drones = [d for d in drones if d.position != d.destination]

        if not active_drones:
            return
        
        # 1. Decide moves
        moves = {drone.id: drone.next_position() for drone in active_drones}

        # 2. Collision avoidance
        moves = collision_avoidance(moves, active_drones)

        # 3. Execute moves
        for drone in active_drones:
            move = moves[drone.id]

            if move is None:
                continue

            if grid.is_obstacle(move):
                drone.detect_obstacle(move, message_queue)
                drone.replan_as_required(move)
            else:
                drone.shift()

        # 4. Share knowledge
        for drone in active_drones:
            drone.process_messages(message_queue)

        message_queue.clear()
        last_move_time = current_time

# CLICK 
def handle_click(pos):
    c = pos[0] // CELL_SIZE
    r = pos[1] // CELL_SIZE

    if 0 <= r < ROWS and 0 <= c < COLS:
        grid.add_obstacle((r, c))

        for drone in drones:
            drone.plan_for_path()

# MAIN LOOP 
running = True
while running:
    screen.fill(BACKGROUND)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            handle_click(pygame.mouse.get_pos())

    update_simulation()
    draw_grid()
    draw_goal()
    draw_drones()

    pygame.display.flip()
    clock.tick(10)

pygame.quit()
sys.exit()