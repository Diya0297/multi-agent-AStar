import pygame
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from drone_simulation.drone_simulation import Drone, Grid, collision_avoidance

GRID_SIZE = 20
CELL_SIZE = 50
WIDTH = GRID_SIZE * CELL_SIZE
HEIGHT = GRID_SIZE * CELL_SIZE

BACKGROUND = (25, 25, 30)
GRID_DOT = (60, 60, 70)
OBSTACLE_COLOR = (220, 50, 50)
GOAL_COLOR = (50, 220, 50)

DRONE_COLORS = [(50, 150, 255), (255, 200, 50)]
DRONE_RADIUS = 12
GLOW_RADIUS = 25

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Disaster Drone Simulation")
clock = pygame.time.Clock()

# ================== GRID ==================
grid = Grid(GRID_SIZE, GRID_SIZE)  # use Grid from drone_simulation

# ================== GOAL ==================
goal = (15, 15)

# ================== DRONES ==================
drones = [
    Drone(1, (0, 0), goal, grid),
    Drone(2, (0, 3), goal, grid)
]

# ================== DRAW ==================
def draw_grid():
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            px = x * CELL_SIZE + CELL_SIZE // 2
            py = y * CELL_SIZE + CELL_SIZE // 2

            if grid.is_obstacle((x, y)):
                pygame.draw.circle(screen, OBSTACLE_COLOR, (px, py), 6)
            else:
                pygame.draw.circle(screen, GRID_DOT, (px, py), 3)

def draw_goal():
    gx, gy = goal
    px = gx * CELL_SIZE + CELL_SIZE // 2
    py = gy * CELL_SIZE + CELL_SIZE // 2
    pygame.draw.circle(screen, GOAL_COLOR, (px, py), DRONE_RADIUS)

def draw_drones():
    for drone, color in zip(drones, DRONE_COLORS):
        # GREEN PATH (planned path)
        for step in drone.path:
            px = step[0] * CELL_SIZE + CELL_SIZE // 2
            py = step[1] * CELL_SIZE + CELL_SIZE // 2
            pygame.draw.circle(screen, (50, 220, 50), (px, py), 6)

        # CURRENT POSITION
        x, y = drone.position
        px = x * CELL_SIZE + CELL_SIZE // 2
        py = y * CELL_SIZE + CELL_SIZE // 2

        # GLOW EFFECT
        for i in range(GLOW_RADIUS, DRONE_RADIUS, -3):
            alpha = int(60 * (i - DRONE_RADIUS) / (GLOW_RADIUS - DRONE_RADIUS))
            surf = pygame.Surface((i * 2, i * 2), pygame.SRCALPHA)
            pygame.draw.circle(surf, (*color, alpha), (i, i), i)
            screen.blit(surf, (px - i, py - i))

        pygame.draw.circle(screen, color, (px, py), DRONE_RADIUS)

# ================== SIMULATION ==================
move_delay = 300
last_move_time = 0

def update_simulation():
    global last_move_time
    current_time = pygame.time.get_ticks()

    if current_time - last_move_time > move_delay:
        # 1. Decide moves
        moves = {}
        for drone in drones:
            moves[drone.id] = drone.next_position()

        # 2. Collision avoidance
        moves = collision_avoidance(moves)

        # 3. Execute moves
        for drone in drones:
            move = moves[drone.id]
            if move is None:
                continue

            if grid.is_obstacle(move):
                drone.detect_obstacle(move, [])
                drone.replan_as_required(move)
            else:
                drone.shift()

        last_move_time = current_time

# ================== CLICK ==================
def handle_click(pos):
    x = pos[0] // CELL_SIZE
    y = pos[1] // CELL_SIZE

    if 0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE:
        grid.add_obstacle((x, y))
        for drone in drones:
            drone.plan_for_path()

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
    clock.tick(5)

pygame.quit()
sys.exit()