import os
os.environ['SDL_AUDIODRIVER'] = 'dummy'

import pygame
import random

# المتغيرات الأساسية
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_SIZE = 25
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# الألوان
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)

COLORS = [RED, GREEN, BLUE, CYAN, MAGENTA, YELLOW, ORANGE]

# القطع
SHAPES = [
    [[1, 1, 1, 1]],
    [[1, 1], [1, 1]],
    [[1, 0, 0], [1, 1, 1]],
    [[0, 0, 1], [1, 1, 1]],
    [[0, 1, 1], [1, 1, 0]],
    [[1, 1, 0], [0, 1, 1]],
    [[1, 1, 1], [0, 1, 0]],
]

# دوال القطع
def rotate(shape):
    return list(zip(*reversed(shape)))

def create_shape():
    shape = random.choice(SHAPES)
    return shape

def draw_shape(screen, shape, x, y, color):
    for row in range(len(shape)):
        for col in range(len(shape[row])):
            if shape[row][col]:
                pygame.draw.rect(screen, color, (x + col * GRID_SIZE, y + row * GRID_SIZE, GRID_SIZE, GRID_SIZE))

def check_collision(shape, x, y, grid):
    for row in range(len(shape)):
        for col in range(len(shape[row])):
            if shape[row][col]:
                if x + col < 0 or x + col >= GRID_WIDTH or y + row >= GRID_HEIGHT or grid[y + row][x + col]:
                    return True
    return False

def merge_shape(shape, x, y, grid):
    for row in range(len(shape)):
        for col in range(len(shape[row])):
            if shape[row][col]:
                grid[y + row][x + col] = True

def check_rows(grid):
    full_rows = []
    for row in range(GRID_HEIGHT):
        if all(grid[row]):
            full_rows.append(row)
    return full_rows

def remove_rows(grid, rows):
    for row in rows:
        del grid[row]
        grid.insert(0, [False] * GRID_WIDTH)

# بداية اللعبة
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris")

clock = pygame.time.Clock()

grid = [[False] * GRID_WIDTH for _ in range(GRID_HEIGHT)]

current_shape = create_shape()
current_shape_x = GRID_WIDTH // 2 - len(current_shape[0]) // 2
current_shape_y = 0
shape_color = random.choice(COLORS)

score = 0

# إضافة شاشة البداية
font = pygame.font.Font(None, 48)
developer_text = font.render("Developed by Ibrahim Said", True, WHITE)
github_text = font.render("GitHub: github.com/Blackhat-red-team", True, WHITE)

start_screen = True

while start_screen:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            start_screen = False
        elif event.type == pygame.KEYDOWN:
            start_screen = False

    screen.fill(BLACK)

    screen.blit(developer_text, (SCREEN_WIDTH // 2 - developer_text.get_width() // 2, SCREEN_HEIGHT // 2 - developer_text.get_height()))
    screen.blit(github_text, (SCREEN_WIDTH // 2 - github_text.get_width() // 2, SCREEN_HEIGHT // 2))

    pygame.display.flip()

running = True
game_over = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if not game_over:
                if event.key == pygame.K_LEFT:
                    if not check_collision(current_shape, current_shape_x - 1, current_shape_y, grid):
                        current_shape_x -= 1
                elif event.key == pygame.K_RIGHT:
                    if not check_collision(current_shape, current_shape_x + 1, current_shape_y, grid):
                        current_shape_x += 1
                elif event.key == pygame.K_DOWN:
                    if not check_collision(current_shape, current_shape_x, current_shape_y + 1, grid):
                        current_shape_y += 1
                elif event.key == pygame.K_UP:
                    rotated_shape = rotate(current_shape)
                    if not check_collision(rotated_shape, current_shape_x, current_shape_y, grid):
                        current_shape = rotated_shape

    if not game_over:
        if not check_collision(current_shape, current_shape_x, current_shape_y + 1, grid):
            current_shape_y += 1
        else:
            merge_shape(current_shape, current_shape_x, current_shape_y, grid)
            full_rows = check_rows(grid)
            if full_rows:
                remove_rows(grid, full_rows)
                score += len(full_rows)
            current_shape = create_shape()
            current_shape_x = GRID_WIDTH // 2 - len(current_shape[0]) // 2
            current_shape_y = 0
            if check_collision(current_shape, current_shape_x, current_shape_y, grid):
                game_over = True

    screen.fill(BLACK)

    for row in range(GRID_HEIGHT):
        for col in range(GRID_WIDTH):
            if grid[row][col]:
                pygame.draw.rect(screen, WHITE, (col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE), 1)

    draw_shape(screen, current_shape, current_shape_x * GRID_SIZE, current_shape_y * GRID_SIZE, shape_color)

    if game_over:
        font = pygame.font.Font(None, 48)
        text = font.render("Game Over", True, WHITE)
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))

    pygame.display.flip()
    clock.tick(10)

pygame.quit()

