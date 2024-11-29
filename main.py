import pygame
import sys
from pygame.locals import *
import random
import math
from collections import deque

pygame.init()
pygame.mixer.init()

screen_width = 448
screen_height = 608
screen_game = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('PAC-MAN')

Black = (0, 0, 0)
Yellow = (255, 255, 0)
Blue = (0, 0, 255)
White = (255, 255, 255)
Red = (255, 0, 0)

game_started = False

pygame.mixer.music.load("assets/game_start.wav")  
pygame.mixer.music.play(-1)

eat_sound = pygame.mixer.Sound("assets/munch_1.wav")

pacman_image = pygame.image.load("assets/pacman.png")  

ghost_images = [
    pygame.image.load("assets/ghost_red.png"),  
    pygame.image.load("assets/ghost_yellow.png"),  
    pygame.image.load("assets/ghost_pink.png"),  
    pygame.image.load("assets/ghost_green.png")  ]

blue_ghost_images = [
    pygame.image.load("assets/ghost_blue.png"),  
    pygame.image.load("assets/ghost_blue.png"),  
    pygame.image.load("assets/ghost_blue.png"),  
    pygame.image.load("assets/ghost_blue.png")   
]

pacman_image = pygame.transform.scale(pacman_image, (24, 24))  
ghost_images = [pygame.transform.scale(ghost, (24, 24)) for ghost in ghost_images]  
blue_ghost_images = [pygame.transform.scale(ghost, (24, 24)) for ghost in blue_ghost_images]  


pos = [224, 288]
speed = 4
radius = 10
direction = [0, 0]

ghosts = [
    {"pos": [224, 224], "speed": 2},
    {"pos": [224, 352], "speed": 2},
    {"pos": [352, 224], "speed": 2},
    {"pos": [352, 352], "speed": 2}
]

score = 0
lives = 3
power_up_active = False
power_up_timer = 0
power_up_duration = 100

Maze = [
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "X............XX............X",
    "X.XXXX.XXXXX.XX.XXXXX.XXXX.X",
    "XPXXXX.XXXXX.XX.XXXXX.XXXXPX", 
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
    "X.P....XX....XX....XX....P.X", 
    "X.XXXXXXXXXX.XX.XXXXXXXXXX.X",
    "X.XXXXXXXXXX.XX.XXXXXXXXXX.X",
    "X..........................X",  
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXX",
]

mazedots = [[(col_idx * 16 + 8, row_idx * 16 + 8) for col_idx, col in enumerate(row) if col == '.'] for row_idx, row in enumerate(Maze)]

def draw_pacman():
    screen_game.blit(pacman_image, (pos[0] - 10, pos[1] - 10))  

def draw_ghosts():
    for i, ghost in enumerate(ghosts):
        if power_up_active:  
            screen_game.blit(blue_ghost_images[i], (ghost["pos"][0] - 10, ghost["pos"][1] - 10))
        else:  
            screen_game.blit(ghost_images[i], (ghost["pos"][0] - 10, ghost["pos"][1] - 10))

def reset_ghosts():
    global ghosts
    ghosts = [
        {"pos": [224, 224], "speed": 2},
        {"pos": [224, 352], "speed": 2},
        {"pos": [352, 224], "speed": 2},
        {"pos": [352, 352], "speed": 2}
    ]

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
    global power_up_active, power_up_timer
    nextpos = [pos[0] + direction[0] * speed, pos[1] + direction[1] * speed]
    row = int(nextpos[1] / 16)
    col = int(nextpos[0] / 16)
    if Maze[row][col] != "X":
        pos[0] = nextpos[0]
        pos[1] = nextpos[1]
        if Maze[row][col] == 'P':
            Maze[row] = Maze[row][:col] + '.' + Maze[row][col + 1:]
            power_up_active = True
            power_up_timer = power_up_duration

def ghost_movement():
    for ghost in ghosts:
        pos_ghost = ghost["pos"]
        ghost_row, ghost_col = int(pos_ghost[1] / 16), int(pos_ghost[0] / 16)
        pacman_row, pacman_col = int(pos[1] / 16), int(pos[0] / 16)
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        queue = deque([(ghost_row, ghost_col, [])])
        visited = set()
        
        if power_up_active:
            max_distance = -1
            best_direction = None
            for dr, dc in directions:
                new_row, new_col = ghost_row + dr, ghost_col + dc
                if (
                    0 <= new_row < len(Maze)
                    and 0 <= new_col < len(Maze[0])
                    and Maze[new_row][new_col] != "X"
                ):
                    distance = math.sqrt((new_row - pacman_row) ** 2 + (new_col - pacman_col) ** 2)
                    if distance > max_distance:
                        max_distance = distance
                        best_direction = (dr, dc)
            if best_direction:
                pos_ghost[0] += best_direction[1] * ghost["speed"]
                pos_ghost[1] += best_direction[0] * ghost["speed"]
        else:
            while queue:
                current_row, current_col, path = queue.popleft()
                if (current_row, current_col) == (pacman_row, pacman_col):
                    if path:
                        next_step = path[0]
                        pos_ghost[0] += next_step[1] * ghost["speed"]
                        pos_ghost[1] += next_step[0] * ghost["speed"]
                    break
                visited.add((current_row, current_col))
                for dr, dc in directions:
                    new_row, new_col = current_row + dr, current_col + dc
                    if (
                        0 <= new_row < len(Maze)
                        and 0 <= new_col < len(Maze[0])
                        and Maze[new_row][new_col] != "X"
                        and (new_row, new_col) not in visited
                    ):
                        queue.append((new_row, new_col, path + [(dr, dc)]))

def check_collision():
    global lives, pos, score, power_up_active
    pacman_rect = pygame.Rect(pos[0] - radius, pos[1] - radius, radius * 2, radius * 2)

    for ghost in ghosts:
        ghost_rect = pygame.Rect(ghost["pos"][0] - radius, ghost["pos"][1] - radius, radius * 2, radius * 2)

        if pacman_rect.colliderect(ghost_rect):
            if power_up_active:
                score += 50  
                ghost["pos"] = [224, 224]  
            else:
                lives -= 1
                pos[:] = [224, 288]  
                reset_ghosts()  
                break


def food_dots():
    center = (pos[0], pos[1])
    food_eaten = False  # Flag untuk cek jika ada makanan yang dimakan
    for row in mazedots:
        initial_length = len(row)
        row[:] = [mazedot for mazedot in row if not ((center[0] - mazedot[0]) ** 2 + (center[1] - mazedot[1]) ** 2 < (radius + 3) ** 2)]
        if len(row) < initial_length:  # Cek jika makanan berkurang
            food_eaten = True
    if food_eaten:
        eat_sound.play()  # Mainkan efek suara saat makanan dimakan

def win():
    return all(not row for row in mazedots)  
def draw_score_and_lives():
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, White)
    lives_text = font.render(f"Lives: {lives}", True, White)
    screen_game.blit(score_text, (10, screen_height - 30))
    screen_game.blit(lives_text, (screen_width - 100, screen_height - 30))

def powerup_draw():
    for row_idx, row in enumerate(Maze):
        for col_idx, col in enumerate(row):
            if col == 'P':  
                x = col_idx * 16 + 8
                y = row_idx * 16 + 8
                pygame.draw.circle(screen_game, Red, (x, y), 6)

def spawn_power_up():
    global power_up_pos
    empty_cells = [] 
    for row_idx, row in enumerate(Maze):
        for col_idx, col in enumerate(row):
            if col == 'P':  
                empty_cells.append((row_idx, col_idx))
    if empty_cells:
        power_up_pos = random.choice(empty_cells)
        Maze[power_up_pos[0]] = Maze[power_up_pos[0]][:power_up_pos[1]] + 'P' + Maze[power_up_pos[0]][power_up_pos[1] + 1:]

def show_message(message, color):
    screen_game.fill(Black)
    font = pygame.font.Font(None, 74)
    text = font.render(message, True, color)
    text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2))
    screen_game.blit(text, text_rect)
    pygame.display.update()
    pygame.time.wait(2000)  

def main():
    global power_up_timer, game_started, power_up_active
    clock = pygame.time.Clock()
    spawn_power_up()

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
                if not game_started:
                    pygame.mixer.music.stop()
                    game_started = True


        pacman_movement()
        ghost_movement()
        food_dots()

        if power_up_active:
            power_up_timer -= 1
            if power_up_timer <= 0:
                power_up_active = False  

        check_collision()

        if win():
            show_message("You Win!", Yellow)
            pygame.quit()
            sys.exit()

        if lives == 0:
            show_message("Game Over", Red)
            pygame.quit()
            sys.exit()

        screen_game.fill(Black)
        maze_draw()
        dotsdraw()
        powerup_draw()
        draw_pacman() 
        draw_ghosts()  
        draw_score_and_lives()
        pygame.display.update()
        clock.tick(30)  
if __name__ == '__main__':
    main()