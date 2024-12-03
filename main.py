import pygame
import sys
from pygame.locals import *
import random
import math
from collections import deque

# Menginisialisasi Pygame dan suara
pygame.init()
pygame.mixer.init()

# Mengatur ukuran layar dan judul game
screen_width = 448
screen_height = 608
screen_game = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('PAC-MAN')

# Mendefinisikan warna yang digunakan di game
Black = (0, 0, 0)
Yellow = (255, 255, 0)
Blue = (0, 0, 255)
White = (255, 255, 255)
Red = (255, 0, 0)
Green = (0, 255, 0) 
Purple = (255, 0, 255)

# Variabel yang menandakan apakah permainan sudah dimulai
game_started = False

# Memainkan musik latar saat permainan dimulai
pygame.mixer.music.load("assets/game_start.wav")  
pygame.mixer.music.play(-1)

# Memuat efek suara untuk saat Pac-Man makan titik
eat_sound1 = pygame.mixer.Sound("assets/munch_1.wav")
eat_sound2 = pygame.mixer.Sound("assets/munch_2.wav")
eat_sounds = [eat_sound1, eat_sound2]
current_sound_index = 0 

death_Sound = pygame.mixer.Sound("assets/death_1.wav")
Powerup_Sound = pygame.mixer.Sound("assets/power_pellet.wav")

eat_ghost = pygame.mixer.Sound("assets/eat_ghost.wav")


# Memuat gambar Pac-Man dan gambar hantu
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

# mengatur ukuran pacman dan hantu
pacman_image = pygame.transform.scale(pacman_image, (24, 24))  
ghost_images = [pygame.transform.scale(ghost, (24, 24)) for ghost in ghost_images]  
blue_ghost_images = [pygame.transform.scale(ghost, (24, 24)) for ghost in blue_ghost_images]  

# posisi awal dan pergerakan
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

# Nilai awal untuk skor, jumlah nyawa, dan status power-up
score = 0
lives = 3
power_up_active = False
power_up_timer = 0
power_up_duration = 100

# Maze yang berisi tembok ('X'), titik makanan ('.'), dan power-up ('P')
Maze_1 = [
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
    "XXXXXX    X      X    XXXXXX",
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
    "XPXXXXXXXXXX.XX.XXXXXXXXXXPX",
    "X..........................X",
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXX",
]

# Maze for level 2
Maze_2 = [
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "X..........................X",
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
    "XXXXXX    X      X    XXXXXX",
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
    "X............P.............X",
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXX",
]

# Maze for level 3
Maze_3 = [
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "X....X................X....X",
    "X.XXXX.XXXXX.XX.XXXXX.XXXX.X",
    "XPXXXX.XXXXX.XX.XXXXX.XXXX.X",
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
    "XXXXXX    X      X    XXXXXX",
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
    "X.XXXXXXXXXX.XX.XXXXXXXXXXPX",
    "X..........................X",
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXX",
]

mazedots_1 = [[(col_idx * 16 + 8, row_idx * 16 + 8) for col_idx, col in enumerate(row) if col == '.'] for row_idx, row in enumerate(Maze_1)]
mazedots_2 = [[(col_idx * 16 + 8, row_idx * 16 + 8) for col_idx, col in enumerate(row) if col == '.'] for row_idx, row in enumerate(Maze_2)]
mazedots_3 = [[(col_idx * 16 + 8, row_idx * 16 + 8) for col_idx, col in enumerate(row) if col == '.'] for row_idx, row in enumerate(Maze_3)]

# Fungsi untuk menggambar Pac-Man di layar
def draw_pacman():
    screen_game.blit(pacman_image, (pos[0] - 10, pos[1] - 10))  

# Fungsi untuk menggambar hantu di layar, menyesuaikan dengan status power-up
def draw_ghosts():
    for i, ghost in enumerate(ghosts):
        if power_up_active:  
            screen_game.blit(blue_ghost_images[i], (ghost["pos"][0] - 10, ghost["pos"][1] - 10))
        else:  
            screen_game.blit(ghost_images[i], (ghost["pos"][0] - 10, ghost["pos"][1] - 10))

# Fungsi untuk mereset posisi hantu setelah Pac-Man kehilangan nyawa
def reset_ghosts():
    global ghosts
    ghosts = [
        {"pos": [224, 224], "speed": 2},
        {"pos": [224, 352], "speed": 2},
        {"pos": [352, 224], "speed": 2},
        {"pos": [352, 352], "speed": 2}
    ]

# Fungsi untuk menggambar maze
def maze_draw(Maze, color):
    for row_idx, row in enumerate(Maze):
        for col_idx, col in enumerate(row):
            if col == "X":
                x = col_idx * 16
                y = row_idx * 16
                if row_idx == 0 or Maze[row_idx - 1][col_idx] != "X":
                    pygame.draw.line(screen_game, color, (x, y), (x + 16, y), 2)
                if row_idx == len(Maze) - 1 or Maze[row_idx + 1][col_idx] != "X":
                    pygame.draw.line(screen_game, color, (x, y + 16), (x + 16, y + 16), 2)
                if col_idx == 0 or Maze[row_idx][col_idx - 1] != "X":
                    pygame.draw.line(screen_game, color, (x, y), (x, y + 16), 2)
                if col_idx == len(row) - 1 or Maze[row_idx][col_idx + 1] != "X":
                    pygame.draw.line(screen_game, color, (x + 16, y), (x + 16, y + 16), 2)

def dotsdraw(mazedots):
    for row in mazedots:
        for mazedot in row:
            pygame.draw.circle(screen_game, White, mazedot, 3)

# Fungsi untuk menggerakkan Pac-Man berdasarkan input pengguna
def pacman_movement(Maze):
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
            Powerup_Sound.play()
            power_up_timer = power_up_duration

# Fungsi untuk menggerakkan hantu
def ghost_movement(Maze):
    for ghost in ghosts:
        pos_ghost = ghost["pos"]
        ghost_row, ghost_col = int(pos_ghost[1] / 16), int(pos_ghost[0] / 16)
        pacman_row, pacman_col = int(pos[1] / 16), int(pos[0] / 16)
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        queue = deque([(ghost_row, ghost_col, [])])
        visited = set()
        
        if power_up_active:
            # Gerakan hantu saat power-up aktif (hantu menjauh dari Pac-Man)
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
            # Gerakan hantu biasa (menuju Pac-Man)
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

# Fungsi untuk mengecek tabrakan antara Pac-Man dan hantu
def check_collision():
    global lives, pos, score, power_up_active
    pacman_rect = pygame.Rect(pos[0] - radius, pos[1] - radius, radius * 2, radius * 2)

    # Mengecek apakah Pac-Man bertabrakan dengan hantu
    for ghost in ghosts:
        ghost_rect = pygame.Rect(ghost["pos"][0] - radius, ghost["pos"][1] - radius, radius * 2, radius * 2)

         # Jika ada tabrakan antara Pac-Man dan hantu
        if pacman_rect.colliderect(ghost_rect):
            if power_up_active:
                score += 50  
                ghost["pos"] = [224, 224]  
                eat_ghost.play()
            else:
                death_Sound.play()
                lives -= 1
                pos[:] = [224, 288]  
                reset_ghosts()  
                break

# Fungsi untuk mengecek apakah Pac-Man makan titik makanan
def food_dots(mazedots):
    global current_sound_index
    center = (pos[0], pos[1])
    food_eaten = False 
    for row in mazedots:
        initial_length = len(row)
         # Menghapus titik makanan yang berada dalam jangkauan Pac-Man
        row[:] = [mazedot for mazedot in row if not ((center[0] - mazedot[0]) ** 2 + (center[1] - mazedot[1]) ** 2 < (radius + 3) ** 2)]
        if len(row) < initial_length:  # Cek jika makanan berkurang
            food_eaten = True
    if food_eaten:
        # Mainkan suara makan berdasarkan indeks saat ini
        eat_sounds[current_sound_index].play()
        # Perbarui indeks untuk memilih suara berikutnya
        current_sound_index = (current_sound_index + 1) % len(eat_sounds)  # Mainkan efek suara saat makanan dimakan

# Fungsi untuk mengecek apakah pemain telah memenangkan permainan
def win(mazedots):
    return all(not row for row in mazedots)  

# Fungsi untuk menggambar skor dan jumlah nyawa di layar
def draw_score_and_lives():
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, White)
    lives_text = font.render(f"Lives: {lives}", True, White)
    screen_game.blit(score_text, (10, screen_height - 30))
    screen_game.blit(lives_text, (screen_width - 100, screen_height - 30))

# Fungsi untuk menggambar power-up di maze
def powerup_draw(Maze):
    for row_idx, row in enumerate(Maze):
        for col_idx, col in enumerate(row):
            if col == 'P':  
                x = col_idx * 16 + 8
                y = row_idx * 16 + 8
                pygame.draw.circle(screen_game, Red, (x, y), 6)

# Fungsi untuk memunculkan power-up di maze
def spawn_power_up(Maze):
    global power_up_pos
    empty_cells = [] 
    for row_idx, row in enumerate(Maze):
        for col_idx, col in enumerate(row):
            if col == 'P':  
                empty_cells.append((row_idx, col_idx))
    if empty_cells:
        power_up_pos = random.choice(empty_cells)
        Maze[power_up_pos[0]] = Maze[power_up_pos[0]][:power_up_pos[1]] + 'P' + Maze[power_up_pos[0]][power_up_pos[1] + 1:]

# Fungsi untuk menampilkan pesan (misalnya, ketika menang atau game over)
def show_message(message, color):
    screen_game.fill(Black)
    font = pygame.font.Font(None, 74)
    text = font.render(message, True, color)
    text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2))
    screen_game.blit(text, text_rect)
    pygame.display.update()
    pygame.time.wait(2000)  

# Fungsi utama untuk menjalankan permainan
def main():
    global pos, game_started, Maze, mazedots, score, lives, power_up_timer, power_up_active
    level = 1 
    Maze = Maze_1 
    mazedots = mazedots_1  
    maze_color = Blue 
    clock = pygame.time.Clock()

    spawn_power_up(Maze)  # Memunculkan power-up pertama

    while True:
        # Mengambil input dari pemain
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_LEFT:
                    direction[0], direction[1] = -1, 0
                elif event.key == K_RIGHT:
                    direction[0], direction[1] = 1, 0
                elif event.key == K_UP:
                    direction[0], direction[1] = 0, -1
                elif event.key == K_DOWN:
                    direction[0], direction[1] = 0, 1
                if not game_started:
                    pygame.mixer.music.stop()
                    game_started = True

        # Logika permainan
        pacman_movement(Maze) 
        ghost_movement(Maze) 
        food_dots(mazedots)

        # Hitung timer power-up
        if power_up_active:
            power_up_timer -= 1
            if power_up_timer <= 0:
                power_up_active = False

        # Cek tabrakan dan status permainan
        check_collision()
        if win(mazedots):
            # Perpindahan level
            if level == 1:
                print("Level 1 Selesai! Lanjut ke Level 2.")
                level, Maze, mazedots, maze_color = 2, Maze_2, mazedots_2, Green
                pos = [224, 288] 
                reset_ghosts()  
            elif level == 2:
                print("Level 2 Selesai! Lanjut ke Level 3.")
                level, Maze, mazedots, maze_color = 3, Maze_3, mazedots_3, Purple
                pos = [224, 288]
                reset_ghosts()
            else:
                # Pemain menang
                show_message("You Win!", Yellow)
                pygame.quit()
                sys.exit()

        if lives == 0:
            # Game over
            show_message("Game Over", Red)
            pygame.quit()
            sys.exit()

        # Rendering tampilan game
        screen_game.fill(Black)
        maze_draw(Maze, maze_color)
        dotsdraw(mazedots)
        powerup_draw(Maze)
        draw_pacman()
        draw_ghosts()
        draw_score_and_lives()

        pygame.display.update()
        clock.tick(30)
  
if __name__ == '__main__':
    main()