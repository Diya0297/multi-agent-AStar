import pygame
import sys

# ================== CONFIG ==================
GRID_SIZE = 20
CELL_SIZE = 50
WIDTH = GRID_SIZE * CELL_SIZE
HEIGHT = GRID_SIZE * CELL_SIZE

BACKGROUND = (25, 25, 30)
GRID_DOT = (60, 60, 70)
OBSTACLE_COLOR = (220, 50, 50)
GOAL_COLOR = (50, 220, 50)

DRONE_COLORS = [(50, 150, 255), (255, 200, 50)]
DRONE_RADIUS = 15
GLOW_RADIUS = 25

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Disaster Drone Simulation")
clock = pygame.time.Clock()

# ================== 🔴 GRID (REPLACE LATER WITH SHARON) ==================
grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

def is_obstacle(x, y):
    return grid[x][y] == 1

def add_obstacle(x, y):
    grid[x][y] = 1

# ================== GOAL ==================
goal = (15,15)

# ================== 🔴 PATHFINDING (REPLACE WITH ELLA) ==================
def get_path(start, goal):
    """Fake path — move right then down, avoids obstacles minimally"""
    path = []
    x, y = start
    while (x, y) != goal:
        if x < goal[0] and not is_obstacle(x+1, y):
            x += 1
        elif y < goal[1] and not is_obstacle(x, y+1):
            y += 1
        else:
            break
        path.append((x, y))
    return path

# ================== 🔴 DRONES (REPLACE WITH AASTHA) ==================
drones = [
    {"id": 1, "pos": [0, 0], "path": [], "color": DRONE_COLORS[0], "step": 0},
    {"id": 2, "pos": [0, 3], "path": [], "color": DRONE_COLORS[1], "step": 0}
]

def initialize_paths():
    for drone in drones:
        drone["path"] = get_path(tuple(drone["pos"]), goal)
        drone["step"] = 0

initialize_paths()

# ================== DRAW ==================
def draw_grid():
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            px = x * CELL_SIZE + CELL_SIZE // 2
            py = y * CELL_SIZE + CELL_SIZE // 2
            color = OBSTACLE_COLOR if is_obstacle(x, y) else GRID_DOT
            pygame.draw.circle(screen, color, (px, py), 5)

def draw_goal():
    gx, gy = goal
    px = gx * CELL_SIZE + CELL_SIZE // 2
    py = gy * CELL_SIZE + CELL_SIZE // 2
    pygame.draw.circle(screen, GOAL_COLOR, (px, py), DRONE_RADIUS)

def draw_drones():
    for drone in drones:
        x, y = drone["pos"]
        px = x * CELL_SIZE + CELL_SIZE // 2
        py = y * CELL_SIZE + CELL_SIZE // 2

        # draw trail (green path already traveled)
        for i in range(drone["step"]):
            tx, ty = drone["path"][i]
            tpx = tx * CELL_SIZE + CELL_SIZE // 2
            tpy = ty * CELL_SIZE + CELL_SIZE // 2
            pygame.draw.circle(screen, (50, 220, 50), (tpx, tpy), 8)

        # glow effect
        for i in range(GLOW_RADIUS, DRONE_RADIUS, -3):
            alpha = int(50 * (i - DRONE_RADIUS) / (GLOW_RADIUS - DRONE_RADIUS))
            glow_surf = pygame.Surface((i*2, i*2), pygame.SRCALPHA)
            pygame.draw.circle(glow_surf, (*drone["color"], alpha), (i, i), i)
            screen.blit(glow_surf, (px - i, py - i))

        # main drone
        pygame.draw.circle(screen, drone["color"], (px, py), DRONE_RADIUS)

# ================== SIMULATION ==================
move_delay = 300
last_move_time = 0

def update_simulation():
    global last_move_time
    current_time = pygame.time.get_ticks()
    if current_time - last_move_time > move_delay:
        for drone in drones:
            if drone["step"] < len(drone["path"]):
                drone["pos"] = list(drone["path"][drone["step"]])
                drone["step"] += 1
            else:
                drone["path"] = get_path(tuple(drone["pos"]), goal)
                drone["step"] = 0
        last_move_time = current_time

# ================== CLICK ==================
def handle_click(pos):
    x = pos[0] // CELL_SIZE
    y = pos[1] // CELL_SIZE
    if 0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE:
        add_obstacle(x, y)

        # REPLAN PATHS LATER WITH REAL A* + COMMUNICATION
        for drone in drones:
            drone["path"] = get_path(tuple(drone["pos"]), goal)
            drone["step"] = 0

# ================== MAIN LOOP ==================
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
    clock.tick(2)

pygame.quit()
sys.exit()