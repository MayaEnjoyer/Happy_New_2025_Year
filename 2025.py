import os
import sys
import pygame
import random
import math

pygame.init()

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

song_path = resource_path("song.mp3")

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Happy New Year 2025!")
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BROWN = (139, 69, 19)
TREE_COLOR = (34, 139, 34)
SNOWMAN_COLOR = (255, 255, 255)
ORANGE = (255, 165, 0)
RED = (255, 0, 0)
font = pygame.font.SysFont('Comic Sans MS', 50)

snowflakes = [[random.randint(0, WIDTH), random.randint(0, HEIGHT)] for _ in range(100)]

text = "Happy New Year 2025"
text_length = len(text)
current_char = 0
char_delay = 5
char_timer = 0

def draw_tree(surface, position, size):
    x, y = position
    for i in range(3):
        pygame.draw.polygon(surface, TREE_COLOR, [
            (x, y - size - i * 30),
            (x - size - i * 10, y),
            (x + size + i * 10, y)
        ])
    pygame.draw.rect(surface, BROWN, (x - 10, y, 20, 30))

def draw_snowman(surface, position):
    x, y = position
    pygame.draw.circle(surface, SNOWMAN_COLOR, (x, y), 20)
    pygame.draw.circle(surface, SNOWMAN_COLOR, (x, y + 30), 30)
    pygame.draw.circle(surface, SNOWMAN_COLOR, (x, y + 80), 40)
    pygame.draw.polygon(surface, ORANGE, [(x, y), (x + 15, y + 5), (x, y + 10)])
    pygame.draw.circle(surface, BLACK, (x - 8, y - 8), 3)
    pygame.draw.circle(surface, BLACK, (x + 8, y - 8), 3)

def draw_heart(surface, position, size):
    x, y = position
    points = [(x + size * math.sin(angle) ** 3, y - size * (0.75 * math.cos(angle) - 0.3125 * math.cos(2 * angle) - 0.125 * math.cos(3 * angle))) for angle in [i * math.pi / 180 for i in range(360)]]
    pygame.draw.polygon(surface, RED, points)

try:
    pygame.mixer.music.load(song_path)
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)
except pygame.error as e:
    print(f"Не удалось загрузить музыку: {e}")

running = True
while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for flake in snowflakes:
        flake[1] += random.randint(1, 3)
        flake[0] += random.randint(-1, 1)
        if flake[1] > HEIGHT:
            flake[1] = 0
            flake[0] = random.randint(0, WIDTH)
        pygame.draw.circle(screen, WHITE, flake, 3)

    pygame.draw.rect(screen, WHITE, (0, HEIGHT - 50, WIDTH, 50))
    draw_tree(screen, (WIDTH // 2, HEIGHT - 80), 100)
    draw_snowman(screen, (WIDTH // 2 - 150, HEIGHT - 150))

    char_timer += 1
    if char_timer >= char_delay and current_char < text_length:
        current_char += 1
        char_timer = 0

    display_text = text[:current_char]
    text_surface = font.render(display_text, True, WHITE)
    text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 4))
    screen.blit(text_surface, text_rect)

    if current_char >= text_length:
        draw_heart(screen, (WIDTH // 2, HEIGHT // 2), 50)

    pygame.display.flip()
    clock.tick(30)

pygame.mixer.music.stop()
pygame.quit()
sys.exit()
