import pygame
import sys
from pygame.locals import *
import random
import math
from collections import deque

pygame.init()

pygame.mixer.music.load('assets/game_start.wav') 
pygame.mixer.music.play(-1, 0.0)

eat_sound = pygame.mixer.Sound('assets/munch_1.wav') 
game_over_sound = pygame.mixer.Sound('assets/death_1.wav') 
ghost_collision_sound = pygame.mixer.Sound('assets/eat_ghost.wav') 

screen_width = 448
screen_height = 576
screen_game = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('PAC-MAN')

Black = (0, 0, 0)
Yellow = (255, 255, 0)
Blue = (0, 0, 255)
White = (255, 255, 255)
Red = (255, 0, 0)

pos = [224, 288]
speed = 4
radius = 10
direction = [0, 0]

pos_ghost = [224, 224]
speed_ghost = 2

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

mazedots = [[(col_idx * 16 + 8, row_idx * 16 + 8) for col_idx, col in enumerate(row) if col == '.'] for row_idx, row in enumerate(Maze)]

pacman_image = pygame.image.load('assets/ean.jpg')
ghost_image = pygame.image.load('assets/image.png') 

pacman_image = pygame.transform.scale(pacman_image, (34, 34))
ghost_image = pygame.transform.scale(ghost_image, (34, 34))


def maze_draw():
    for row_idx, row in enumerate(Maze):
        for col_idx, col in enumerate(row):
            if col == "X":
                x = col_idx * 16
                y = row_idx * 16

                if row_idx == 0 or Maze[row_idx - 1][col_idx] != "X":
                    pygame.draw.line(screen_game, Blue, (x, y), (x + 16, y), 2)
                if row_idx == len(Maze) - 1 or Maze[row_idx + 1][col_idx] != "X":
                    pygame.draw.line(screen_game, Blue, (x, y + 16), (x + 16, y + 16), 2)
                if col_idx == 0 or Maze[row_idx][col_idx - 1] != "X":
                    pygame.draw.line(screen_game, Blue, (x, y), (x, y + 16), 2)
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
    ghost_row, ghost_col = int(pos_ghost[1] / 16), int(pos_ghost[0] / 16)
    pacman_row, pacman_col = int(pos[1] / 16), int(pos[0] / 16)

    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    queue = deque([(ghost_row, ghost_col, [])])
    visited = set() 

    while queue:
        current_row, current_col, path = queue.popleft()

        if (current_row, current_col) == (pacman_row, pacman_col):
            if path:
                next_step = path[0]
                pos_ghost[0] += next_step[1] * speed_ghost 
                pos_ghost[1] += next_step[0] * speed_ghost 
            return

        visited.add((current_row, current_col))

        for dr, dc in directions:
            new_row, new_col = current_row + dr, current_col + dc
            if (
                0 <= new_row < len(Maze) and
                0 <= new_col < len(Maze[0]) and
                Maze[new_row][new_col] != "X" and
                (new_row, new_col) not in visited
            ):
                queue.append((new_row, new_col, path + [(dr, dc)]))


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
            game_over_sound.play()
            pygame.quit()
            sys.exit()

        if win():
            print("You Win!")
            pygame.quit()
            sys.exit()

        screen_game.fill(Black)
        maze_draw()
        dotsdraw()

        screen_game.blit(pacman_image, (pos[0] - 8, pos[1] - 8)) 
        screen_game.blit(ghost_image, (pos_ghost[0] - 8, pos_ghost[1] - 8)) 
        pygame.display.update()
        clock.tick(30)


if __name__ == '__main__':
    main()
