import pygame
import random
import sys

# Inisialisasi Pygame
pygame.init()

# Dimensi layar
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pacman Game")

# Warna
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# FPS
clock = pygame.time.Clock()
FPS = 60

# Pacman
pacman_size = 30
pacman_x, pacman_y = WIDTH // 2, HEIGHT // 2
pacman_speed = 4

# Hantu
ghost_size = 30
ghost_speed = 1
ghosts = [{"x": random.randint(0, WIDTH - ghost_size), "y": random.randint(0, HEIGHT - ghost_size), "dx": ghost_speed, "dy": ghost_speed, "scared": False} for _ in range(3)]

# Buah dan Power-up
fruit_radius = 5
fruits = [{"x": random.randint(0, WIDTH), "y": random.randint(0, HEIGHT)} for _ in range(20)]
power_ups = [{"x": random.randint(0, WIDTH), "y": random.randint(0, HEIGHT)} for _ in range(5)]

# Status Game
score = 0
lives = 3
power_up_timer = 0
game_over = False

def draw_text(text, size, color, x, y):
    font = pygame.font.Font(None, size)
    render = font.render(text, True, color)
    screen.blit(render, (x, y))

def check_collision(x1, y1, x2, y2, size):
    return abs(x1 - x2) < size and abs(y1 - y2) < size

def reset_game():
    global pacman_x, pacman_y, ghosts, fruits, power_ups, score, lives, power_up_timer
    pacman_x, pacman_y = WIDTH // 2, HEIGHT // 2
    ghosts = [{"x": random.randint(0, WIDTH - ghost_size), "y": random.randint(0, HEIGHT - ghost_size), "dx": ghost_speed, "dy": ghost_speed, "scared": False} for _ in range(3)]
    fruits = [{"x": random.randint(0, WIDTH), "y": random.randint(0, HEIGHT)} for _ in range(20)]
    power_ups = [{"x": random.randint(0, WIDTH), "y": random.randint(0, HEIGHT)} for _ in range(5)]
    score = 0
    lives = 3
    power_up_timer = 0

def show_popup(message):
    global game_over
    while True:
        screen.fill(BLACK)
        draw_text(message, 60, WHITE, WIDTH // 4, HEIGHT // 3)
        draw_text("Press R to Restart or Q to Quit", 30, WHITE, WIDTH // 4, HEIGHT // 2)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    reset_game()
                    return
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        pacman_x -= pacman_speed
    if keys[pygame.K_RIGHT]:
        pacman_x += pacman_speed
    if keys[pygame.K_UP]:
        pacman_y -= pacman_speed
    if keys[pygame.K_DOWN]:
        pacman_y += pacman_speed

    # Batas layar untuk Pacman
    pacman_x = max(0, min(WIDTH - pacman_size, pacman_x))
    pacman_y = max(0, min(HEIGHT - pacman_size, pacman_y))

    # Periksa Power-up
    if power_up_timer > 0:
        power_up_timer -= 1
        for ghost in ghosts:
            ghost["scared"] = True  # Hantu menjauh
    else:
        for ghost in ghosts:
            ghost["scared"] = False  # Hantu mengejar

    # Logika Ghost
    for ghost in ghosts:
        if ghost["scared"]:
            # Kabur dari Pacman (hantu bergerak ke arah yang berlawanan)
            if ghost["x"] < pacman_x:
                ghost["x"] -= ghost_speed
            else:
                ghost["x"] += ghost_speed

            if ghost["y"] < pacman_y:
                ghost["y"] -= ghost_speed
            else:
                ghost["y"] += ghost_speed
        else:
            # Kejar Pacman
            if ghost["x"] < pacman_x:
                ghost["x"] += ghost["dx"]
            else:
                ghost["x"] -= ghost["dx"]

            if ghost["y"] < pacman_y:
                ghost["y"] += ghost["dy"]
            else:
                ghost["y"] -= ghost["dy"]

        # Pastikan hantu tidak keluar dari layar
        ghost["x"] = max(0, min(WIDTH - ghost_size, ghost["x"]))
        ghost["y"] = max(0, min(HEIGHT - ghost_size, ghost["y"]))

        # Collision dengan Pacman
        if check_collision(pacman_x, pacman_y, ghost["x"], ghost["y"], pacman_size):
            if ghost["scared"]:
                score += 50
                ghost["x"], ghost["y"] = random.randint(0, WIDTH - ghost_size), random.randint(0, HEIGHT - ghost_size)
            else:
                lives -= 1
                pacman_x, pacman_y = WIDTH // 2, HEIGHT // 2
                if lives == 0:
                    show_popup("Game Over")
                    reset_game()

    # Collision dengan Buah
    fruits = [fruit for fruit in fruits if not check_collision(pacman_x, pacman_y, fruit["x"], fruit["y"], pacman_size)]
    score += 10 * (20 - len(fruits))  # 10 poin per buah

    # Collision dengan Power-up
    for power_up in power_ups[:]:
        if check_collision(pacman_x, pacman_y, power_up["x"], power_up["y"], pacman_size):
            power_ups.remove(power_up)
            power_up_timer = 300  # 5 detik

    # Menang
    if not fruits:
        show_popup("Congratulations!")
        reset_game()

    # Gambar Objek
    screen.fill(BLACK)
    pygame.draw.rect(screen, YELLOW, (pacman_x, pacman_y, pacman_size, pacman_size))
    for ghost in ghosts:
        color = BLUE if ghost["scared"] else RED
        pygame.draw.rect(screen, color, (ghost["x"], ghost["y"], ghost_size, ghost_size))
    for fruit in fruits:
        pygame.draw.circle(screen, GREEN, (fruit["x"], fruit["y"]), fruit_radius)
    for power_up in power_ups:
        pygame.draw.circle(screen, WHITE, (power_up["x"], power_up["y"]), fruit_radius)

    # Tampilkan Skor dan Nyawa
    draw_text(f"Score: {score}", 30, WHITE, 10, 10)
    draw_text(f"Lives: {lives}", 30, WHITE, 10, 50)

    pygame.display.flip()
    clock.tick(FPS)
