import pygame
import sys
import random
from pygame.locals import *
from collections import deque

# Inisialisasi Pygame
pygame.init()

# Dimensi layar
WIDTH, HEIGHT = 448, 576
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('PAC-MAN')

# Warna
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Maze
Maze = [
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "X............XX............X",
    "X.XXXX.XXXXX.XX.XXXXX.XXXX.X",
    "X.XXXX.XXXXX.XX.XXXXX.XXXX.X",
    "X.XXXX.XXXXX.XX.XXXXX.XXXX.X",
    "X..........................X",
    "X.XXXX.XX.XXXXXXXX.XX.XXXX.X",
    "X.XXXX.XX.XXXXXXXX.XX.XXXX.X",
    "X......XX....XX....XX......X",
    "XXXXXX.XXXXX XX XXXXX.XXXXXX",
    "XXXXXX.XXXXX XX XXXXX.XXXXXX",
    "XXXXXX.XX          XX.XXXXXX",
    "XXXXXX.XX XXX  XXX XX.XXXXXX",
    "XXXXXX.XX X      X XX.XXXXXX",
    "          X      X          ",
    "XXXXXX.XX X  X   X XX.XXXXXX",
    "XXXXXX.XX XXXXXXXX XX.XXXXXX",
    "XXXXXX.XX          XX.XXXXXX",
    "XXXXXX.XX XXXXXXXX XX.XXXXXX",
    "XXXXXX.XX XXXXXXXX XX.XXXXXX",
    "X............XX............X",
    "X.XXXX.XXXXX.XX.XXXXX.XXXX.X",
    "X.XXXX.XXXXX.XX.XXXXX.XXXX.X",
    "X...XX................XX...X",
    "XXX.XX.XX.XXXXXXXX.XX.XX.XXX",
    "XXX.XX.XX.XXXXXXXX.XX.XX.XXX",
    "X......XX....XX....XX......X",
    "X.XXXXXXXXXX.XX.XXXXXXXXXX.X",
    "X.XXXXXXXXXX.XX.XXXXXXXXXX.X",
    "X..........................X",
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXX",
]

# Posisi awal Pac-Man
pacman_pos = [224, 288]
pacman_speed = 4
pacman_dir = [0, 0]
radius = 10

# Hantu
ghosts = [{"x": 224, "y": 224, "dx": 2, "dy": 0, "scared": False} for _ in range(3)]
ghost_speed = 2
scared_timer = 0

# Dot dan Power-up
mazedots = [[(col_idx * 16 + 8, row_idx * 16 + 8) for col_idx, col in enumerate(row) if col == '.'] for row_idx, row in enumerate(Maze)]
power_ups = [{"x": random.randint(0, WIDTH), "y": random.randint(0, HEIGHT)} for _ in range(5)]

# Game Status
score = 0
lives = 3

# Gambar
pacman_image = pygame.transform.scale(pygame.image.load('assets/ean.jpg'), (34, 34))
ghost_image = pygame.transform.scale(pygame.image.load('assets/image.png'), (34, 34))

def draw_maze():
    for row_idx, row in enumerate(Maze):
        for col_idx, col in enumerate(row):
            if col == "X":
                x = col_idx * 16
                y = row_idx * 16
                pygame.draw.rect(screen, BLUE, (x, y, 16, 16))

def draw_dots():
    for row in mazedots:
        for dot in row:
            pygame.draw.circle(screen, WHITE, dot, 3)
    for power_up in power_ups:
        pygame.draw.circle(screen, GREEN, (power_up["x"], power_up["y"]), 5)

def pacman_move():
    next_pos = [pacman_pos[0] + pacman_dir[0] * pacman_speed, pacman_pos[1] + pacman_dir[1] * pacman_speed]
    row = int(next_pos[1] / 16)
    col = int(next_pos[0] / 16)
    if Maze[row][col] != "X":
        pacman_pos[0], pacman_pos[1] = next_pos

def ghost_move():
    global scared_timer
    for ghost in ghosts:
        if scared_timer > 0:
            ghost["scared"] = True
        else:
            ghost["scared"] = False

        next_pos = [ghost["x"] + ghost["dx"], ghost["y"] + ghost["dy"]]
        row = int(next_pos[1] / 16)
        col = int(next_pos[0] / 16)

        if Maze[row][col] == "X":
            ghost["dx"] = -ghost["dx"]
            ghost["dy"] = -ghost["dy"]
        ghost["x"] += ghost["dx"]
        ghost["y"] += ghost["dy"]

def eat_dot():
    global score
    center = (pacman_pos[0], pacman_pos[1])
    for row in mazedots:
        row[:] = [dot for dot in row if (center[0] - dot[0]) ** 2 + (center[1] - dot[1]) ** 2 >= radius ** 2]
        if len(row) < len(mazedots[0]):
            score += 10

def eat_power_up():
    global scared_timer
    for power_up in power_ups[:]:
        if abs(pacman_pos[0] - power_up["x"]) < 10 and abs(pacman_pos[1] - power_up["y"]) < 10:
            power_ups.remove(power_up)
            scared_timer = 300

def check_collision():
    for ghost in ghosts:
        if abs(pacman_pos[0] - ghost["x"]) < 20 and abs(pacman_pos[1] - ghost["y"]) < 20:
            if ghost["scared"]:
                ghosts.remove(ghost)
            else:
                return True
    return False

def main():
    global scared_timer, lives

    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_LEFT:
                    pacman_dir[0], pacman_dir[1] = -1, 0
                elif event.key == K_RIGHT:
                    pacman_dir[0], pacman_dir[1] = 1, 0
                elif event.key == K_UP:
                    pacman_dir[0], pacman_dir[1] = 0, -1
                elif event.key == K_DOWN:
                    pacman_dir[0], pacman_dir[1] = 0, 1

        pacman_move()
        ghost_move()
        eat_dot()
        eat_power_up()

        if scared_timer > 0:
            scared_timer -= 1

        if check_collision():
            lives -= 1
            if lives <= 0:
                print("Game Over!")
                pygame.quit()
                sys.exit()

        screen.fill(BLACK)
        draw_maze()
        draw_dots()
        screen.blit(pacman_image, (pacman_pos[0] - 8, pacman_pos[1] - 8))
        for ghost in ghosts:
            color = WHITE if ghost["scared"] else RED
            pygame.draw.circle(screen, color, (ghost["x"], ghost["y"]), 16)
        pygame.display.update()
        clock.tick(30)

if __name__ == '__main__':
    main()
