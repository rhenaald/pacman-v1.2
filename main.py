import pygame
import sys
from pygame.locals import *
import random
import math
from collections import deque

pygame.init()

# Screen dimensions
screen_width = 448
screen_height = 576
screen_game = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('PAC-MAN')

# Colors
Black = (0, 0, 0)
Yellow = (255, 255, 0)
Blue = (0, 0, 255)
White = (255, 255, 255)
Red = (255, 0, 0)

# Pac-Man
pos = [224, 288]
speed = 4
radius = 10
direction = [0, 0]

# Ghost
pos_ghost = [224, 224]
speed_ghost = 2

# Drawing maze
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
    "X         X      X         X",
    "XXXXXX.XX X      X XX.XXXXXX",
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

mazedots = [[(col_idx * 16 + 8, row_idx * 16 + 8) for col_idx, col in enumerate(row) if col == '.'] for row_idx, row in enumerate(Maze)]


def maze_draw():
    for row_idx, row in enumerate(Maze):
        for col_idx, col in enumerate(row):
            if col == "X":
                x = col_idx * 16
                y = row_idx * 16

                # Atas
                if row_idx == 0 or Maze[row_idx - 1][col_idx] != "X":
                    pygame.draw.line(screen_game, Blue, (x, y), (x + 16, y), 2)
                # Bawah
                if row_idx == len(Maze) - 1 or Maze[row_idx + 1][col_idx] != "X":
                    pygame.draw.line(screen_game, Blue, (x, y + 16), (x + 16, y + 16), 2)
                # Kiri
                if col_idx == 0 or Maze[row_idx][col_idx - 1] != "X":
                    pygame.draw.line(screen_game, Blue, (x, y), (x, y + 16), 2)
                # Kanan
                if col_idx == len(row) - 1 or Maze[row_idx][col_idx + 1] != "X":
                    pygame.draw.line(screen_game, Blue, (x + 16, y), (x + 16, y + 16), 2)

def dotsdraw():
    for row in mazedots:
        for mazedot in row:
            pygame.draw.circle(screen_game, White, mazedot, 3)


def pacman_movement():
    nextpos = [pos[0] + direction[0] * speed, pos[1] + direction[1] * speed]
    row = int(nextpos[1] / 16)
    col = int(nextpos[0] / 16)
    if Maze[row][col] != "X":
        pos[0] = nextpos[0]
        pos[1] = nextpos[1]


def ghost_movement():
    global pos_ghost

    # Convert positions to grid coordinates
    ghost_row, ghost_col = int(pos_ghost[1] / 16), int(pos_ghost[0] / 16)
    pacman_row, pacman_col = int(pos[1] / 16), int(pos[0] / 16)

    # Directions for moving in the grid: right, left, down, up
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    # BFS queue: stores tuples of (current position, path to get there)
    queue = deque([(ghost_row, ghost_col, [])])
    visited = set()  # Keep track of visited positions

    while queue:
        current_row, current_col, path = queue.popleft()

        # If we've reached Pac-Man's position, return the first step in the path
        if (current_row, current_col) == (pacman_row, pacman_col):
            if path:  # Ensure there's a path to follow
                next_step = path[0]
                pos_ghost[0] += next_step[1] * speed_ghost  # Update x position
                pos_ghost[1] += next_step[0] * speed_ghost  # Update y position
            return

        # Mark current position as visited
        visited.add((current_row, current_col))

        # Explore neighbors
        for dr, dc in directions:
            new_row, new_col = current_row + dr, current_col + dc
            if (
                0 <= new_row < len(Maze) and
                0 <= new_col < len(Maze[0]) and
                Maze[new_row][new_col] != "X" and
                (new_row, new_col) not in visited
            ):
                # Add new position to the queue with updated path
                queue.append((new_row, new_col, path + [(dr, dc)]))

    # If no path is found (e.g., Pac-Man is inaccessible), do nothing



def check_collision():
    pacman_rect = pygame.Rect(pos[0] - radius, pos[1] - radius, radius * 2, radius * 2)
    ghost_rect = pygame.Rect(pos_ghost[0] - radius, pos_ghost[1] - radius, radius * 2, radius * 2)
    return pacman_rect.colliderect(ghost_rect)


def food_dots():
    global mazedots
    center = (pos[0], pos[1])
    for row in mazedots:
        row[:] = [mazedot for mazedot in row if (center[0] - mazedot[0]) ** 2 + (center[1] - mazedot[1]) ** 2 >= (radius + 3) ** 2]


def win():
    return all(not row for row in mazedots)


def main():
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_LEFT:
                    direction[0] = -1
                    direction[1] = 0
                elif event.key == K_RIGHT:
                    direction[0] = 1
                    direction[1] = 0
                elif event.key == K_UP:
                    direction[0] = 0
                    direction[1] = -1
                elif event.key == K_DOWN:
                    direction[0] = 0
                    direction[1] = 1

        pacman_movement()
        ghost_movement()
        food_dots()

        if check_collision():
            print("Game Over")
            pygame.quit()
            sys.exit()

        if win():
            print("You Win!")
            pygame.quit()
            sys.exit()

        screen_game.fill(Black)
        maze_draw()
        dotsdraw()
        pygame.draw.circle(screen_game, Yellow, (int(pos[0]), int(pos[1])), radius)
        pygame.draw.circle(screen_game, Red, (int(pos_ghost[0]), int(pos_ghost[1])), radius)
        pygame.display.update()
        clock.tick(30)


if __name__ == '__main__':
    main()
