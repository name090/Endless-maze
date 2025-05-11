import pygame
import random
import time
from collections import deque

# Історія: Славетного лицаря якого вязали в замку його завданя вийти з ного, і я не знаю що він робитеме на волі траву нухати? чи що?

# Ініціалізація pygame
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load('music/background music.mp3')
pygame.mixer.music.play(-1)

# Визначення кольорів
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0) 
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Розміри екрану
WIDTH, HEIGHT = 800, 608
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Лабіринт")
pygame.display.set_icon(pygame.image.load("image/icon.ico"))

# Розміри клітин
CELL_SIZE = 32

# Завантаження зображень
background_image = pygame.image.load("image/background.png")
wall_image = pygame.image.load("image/wall.png")
exit_image = pygame.image.load("image/exit.png")
background_menu_image = pygame.image.load("image/background_menu.png")
background_menu_image = pygame.transform.scale(background_menu_image, (WIDTH, HEIGHT))
player_images = {
    "down": pygame.image.load("image/hero1.png"),
    "left": pygame.image.load("image/hero2.png"),
    "up": pygame.image.load("image/hero3.png"),
    "right": pygame.image.load("image/hero4.png")
}

# Завантаження зображень для кнопок
start_m_image = pygame.image.load("image/start_m.png")
start_hover_image = pygame.image.load("image/start_m2.png")
exit_m_image = pygame.image.load("image/exit_m.png")
exit_hover_image = pygame.image.load("image/exit_m2.png")

# Масштабування зображень
wall_image = pygame.transform.scale(wall_image, (CELL_SIZE, CELL_SIZE))
exit_image = pygame.transform.scale(exit_image, (CELL_SIZE, CELL_SIZE))
for key in player_images:
    player_images[key] = pygame.transform.scale(player_images[key], (CELL_SIZE, CELL_SIZE))

# Масштабування зображень кнопок
button_width, button_height = 200, 80
start_m_image = pygame.transform.scale(start_m_image, (button_width, button_height))
start_hover_image = pygame.transform.scale(start_hover_image, (button_width, button_height))
exit_m_image = pygame.transform.scale(exit_m_image, (button_width, button_height))
exit_hover_image = pygame.transform.scale(exit_hover_image, (button_width, button_height))

# Генерація лабіринту
def generate_maze(level):
    wall_chance = min(0.2 + level * 0.02, 0.5)
    while True:
        maze = [[1 if random.random() < wall_chance else 0 for _ in range(WIDTH // CELL_SIZE)] for _ in range(HEIGHT // CELL_SIZE)]
        maze[0][0] = 0  # Стартова точка
        exit_x, exit_y = generate_exit(maze)

        if bfs(maze, (0, 0), (exit_x, exit_y)):
            return maze, (exit_x, exit_y)

# BFS для перевірки шляху
def bfs(maze, start, goal):
    queue = deque([start])
    visited = set()
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    while queue:
        x, y = queue.popleft()
        if (x, y) == goal:
            return True
        
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(maze[0]) and 0 <= ny < len(maze) and maze[ny][nx] == 0 and (nx, ny) not in visited:
                queue.append((nx, ny))
                visited.add((nx, ny))
    return False

# Генерація виходу
def generate_exit(maze):
    height, width = len(maze), len(maze[0])
    candidates = []

    for x in range(width):
        if maze[height - 1][x] == 0:
            candidates.append((x, height - 1))
    for y in range(height):
        if maze[y][width - 1] == 0:
            candidates.append((width - 1, y))

    return random.choice(candidates) if candidates else (width - 1, height - 1)

# Головне меню
def menu():
    while True:
        SCREEN.blit(background_menu_image, (0, 0))
        
        # Позиції кнопок
        start_button_rect = pygame.Rect(WIDTH // 2 - button_width // 2, HEIGHT // 2 - 100, button_width, button_height)
        exit_button_rect = pygame.Rect(WIDTH // 2 - button_width // 2, HEIGHT // 2 + 50, button_width, button_height)
        
        # Отримання позиції миші
        mouse_pos = pygame.mouse.get_pos()
        
        # Відображення кнопок з урахуванням наведення
        if start_button_rect.collidepoint(mouse_pos):
            SCREEN.blit(start_hover_image, start_button_rect.topleft)
        else:
            SCREEN.blit(start_m_image, start_button_rect.topleft)
        
        if exit_button_rect.collidepoint(mouse_pos):
            SCREEN.blit(exit_hover_image, exit_button_rect.topleft)
        else:
            SCREEN.blit(exit_m_image, exit_button_rect.topleft)
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button_rect.collidepoint(mouse_pos):
                    return "normal"
                if exit_button_rect.collidepoint(mouse_pos):
                    pygame.quit()
                    return None

# Основна гра
def game():
    mode = menu()
    if mode is None:
        return
    
    level = 1
    player_x, player_y = 0, 0
    player_speed = 16
    player_direction = "down"
    clock = pygame.time.Clock()
    start_time = time.time()
    running = True
    
    while running:
        if level > 10:
            font = pygame.font.SysFont(None, 55)
            text = font.render("You Win!", True, YELLOW)
            SCREEN.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
            pygame.display.flip()
            pygame.time.wait(2000)
            running = False
            break
        
        maze, (exit_x, exit_y) = generate_maze(level)
        
        while running:
            SCREEN.fill(GREEN)
            for i in range(len(maze)):
                for j in range(len(maze[i])):
                    SCREEN.blit(wall_image if maze[i][j] else background_image, (j * CELL_SIZE, i * CELL_SIZE))
            
            player_rect = pygame.Rect(player_x, player_y, CELL_SIZE, CELL_SIZE)
            SCREEN.blit(player_images[player_direction], (player_x, player_y))
            exit_rect = pygame.Rect(exit_x * CELL_SIZE, exit_y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            SCREEN.blit(exit_image, (exit_x * CELL_SIZE, exit_y * CELL_SIZE))
            
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    return
            
            if player_rect.colliderect(exit_rect):
                level += 1
                player_x, player_y = 0, 0
                break
            
            elapsed_time = time.time() - start_time
            if elapsed_time >= 300:  # 5 хвилин
                font = pygame.font.SysFont(None, 55)
                text = font.render("Time's Up!", True, YELLOW)
                SCREEN.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
                pygame.display.flip()
                pygame.time.wait(2000)
                running = False
                break
            
            # Відображення таймера та рівня
            font = pygame.font.SysFont(None, 30)
            timer_text = font.render(f"Time: {int(300 - elapsed_time)}", True, BLUE)
            SCREEN.blit(timer_text, (10, 10))
            level_text = font.render(f"Level: {level}", True, BLUE)
            SCREEN.blit(level_text, (WIDTH - level_text.get_width() - 10, 10))
            
            keys = pygame.key.get_pressed()
            new_x, new_y = player_x, player_y
            
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                new_x -= player_speed
                player_direction = "left"
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                new_x += player_speed
                player_direction = "right"
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                new_y -= player_speed
                player_direction = "up"
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                new_y += player_speed
                player_direction = "down"

            new_rect = pygame.Rect(new_x, new_y, CELL_SIZE - 2, CELL_SIZE - 2)

            collision = False
            for i in range(len(maze)):
                for j in range(len(maze[i])):
                    if maze[i][j] == 1:  # Wall
                        wall_rect = pygame.Rect(j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                        if new_rect.colliderect(wall_rect):
                            collision = True
                            break
                if collision:
                    break
            
            if not collision:
                player_x, player_y = new_x, new_y

            player_x = max(0, min(player_x, WIDTH - CELL_SIZE))
            player_y = max(0, min(player_y, HEIGHT - CELL_SIZE))
            
            pygame.display.flip()
            clock.tick(10)
    
    pygame.quit()

if __name__ == "__main__":
    game()