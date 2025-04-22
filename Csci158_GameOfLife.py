import pygame
import numpy as np 

#Patterns 
patterns = {
    "glider": [(1, 0), (2, 1), (0, 2), (1, 2), (2, 2)],
    "blinker": [(1, 0), (1, 1), (1, 2)],
    "glider_gun":  [
            (5, 1), (5, 2), (6, 1), (6, 2), (5, 11), (6, 11), (7, 11),
            (4, 12), (8, 12), (3, 13), (9, 13), (3, 14), (9, 14), (6, 15),
            (4, 16), (8, 16), (5, 17), (6, 17), (7, 17), (6, 18), (3, 21),
            (4, 21), (5, 21), (3, 22), (4, 22), (5, 22), (2, 23), (6, 23), 
            (1, 25), (2, 25), (6, 25), (7, 25), (3, 35), (4,35), (3,36), (4,36)
    ],
    "acorn": [(10, 10), (11, 10), (11, 12), (13, 11), (14, 10), (15, 10), (16, 10)]
}

#  Init 
WIDTH, HEIGHT = 800, 800
cell_size = 20 

def get_grid_size():
    return HEIGHT // cell_size, WIDTH // cell_size

# Colors 
ALIVE = (0, 200, 225) # LIGHT BLUE
DEAD = (20, 20, 20)   # DARK BLACK 
GRID_COLOR = (40, 40, 40) # DARK GRAY

#Start grid 
ROWS = 400 
COLS = 400
grid = np.zeros((ROWS, COLS), dtype = int) 
game_ended = False
counter = 0

# Set up
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Conway's Game of Life")
clock = pygame.time.Clock()

# Button 
def draw_button(screen, text, rect, color, text_color):
    pygame.draw.rect(screen, color, rect)
    font = pygame.font.SysFont("Arial", 32)
    label = font.render(text, True, text_color)
    label_rect = label.get_rect(center=rect.center)
    screen.blit(label, label_rect)

#Game logic 
def update(grid):
    new_grid = grid.copy()
    for i in range(ROWS):
        for j in range(COLS):
            total = 0
            #looks for alive neighbors
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if dx == 0 and dy == 0:
                        continue
                    ni, nj = i + dx, j + dy
                    if 0 <= ni < ROWS and 0 <= nj < COLS:
                        total += grid[ni, nj]
            # rules
            if grid[i, j] == 1 and total not in [2, 3]:
                new_grid[i, j] = 0
            elif grid[i, j] == 0 and total == 3:
                new_grid[i, j] = 1
    return new_grid

# Draw Grid 
def draw_grid(grid):
    global game_ended
    screen.fill(DEAD)
    # Draw Alive and Dead cells
    for i in range (ROWS): 
        for j in range(COLS):
            if grid[i, j] == 1:
                rect = pygame.Rect(j * cell_size, i * cell_size, cell_size, cell_size)
                pygame.draw.rect(screen, ALIVE, rect)
    # Draw grid lines
    for x in range(0, COLS * cell_size, cell_size):
        pygame.draw.line(screen, GRID_COLOR, (x, 0), (x, HEIGHT)) #Vertical 
    for y in range(0, ROWS * cell_size, cell_size):
        pygame.draw.line(screen, GRID_COLOR, (0, y), (WIDTH, y)) #Horizontal
    
    font = pygame.font.SysFont("Arial", 24)
    text = font.render(f"Generation: {counter}", True, (200, 200, 200))
    screen.blit(text, (10, 10))

    if game_ended:
        font = pygame.font.SysFont("Arial", 40)
        text = font.render("Life has ended", True , (255, 0, 0))
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text, text_rect)
    pygame.display.flip()
    
#Main Meneu 
def main_menu():
    menu_running = True
    while menu_running:
        screen.fill((30, 30, 30))
        mx, my = pygame.mouse.get_pos()

        play_button = pygame.Rect(WIDTH // 2 - 100, 200, 200, 60)
        sample_button = pygame.Rect(WIDTH // 2 - 100, 300, 200, 60)
        quit_button = pygame.Rect(WIDTH // 2 - 100, 400, 200, 60)

        draw_button(screen, "Play", play_button, (70, 130, 180), (255, 255, 255))
        draw_button(screen, "Samples", sample_button, (100, 180, 100), (255, 255, 255))
        draw_button(screen, "Quit", quit_button, (180, 70, 70), (255, 255, 255))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.collidepoint(mx, my): 
                    return "play"
                elif sample_button.collidepoint(mx, my):
                    return "sample"
                elif quit_button.collidepoint(mx, my):
                    pygame.quit()
                    exit()
        pygame.display.flip()
        clock.tick(60)

#Pattern Menu
def pattern_menu():
    selecting = True
   
    glider_button = pygame.Rect(WIDTH // 2 - 100, 200, 200, 60)
    blinker_button = pygame.Rect(WIDTH // 2 - 100, 300, 200, 60)
    glider_gun_button = pygame.Rect(WIDTH // 2 - 100, 400, 200, 60)
    acorn_button = pygame.Rect(WIDTH // 2 - 100, 500, 200, 60)

    while selecting:
        screen.fill((30, 30, 30))
        mx, my = pygame.mouse.get_pos()

        font = pygame.font.SysFont("Arial", 36)
        title = font.render("Select a Pattern", True, (255, 255, 255))
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 100))

        draw_button(screen, "Glider", glider_button, (100, 160, 255), (255, 255, 255))
        draw_button(screen, "Blinker", blinker_button, (100, 200, 100), (255, 255, 255))
        draw_button(screen, "Glider Gun", glider_gun_button, (200, 100, 100), (255, 255, 255))
        draw_button(screen, "Acorn", acorn_button, (200,100,200), (255, 255, 255))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if glider_button.collidepoint(mx, my):
                    return "glider"
                elif blinker_button.collidepoint(mx, my):
                    return "blinker"
                elif glider_gun_button.collidepoint(mx, my):
                    return "glider_gun"
                elif acorn_button.collidepoint(mx, my):
                    return "acorn"
        pygame.display.flip()
        clock.tick(60)

# Patterns 
def load_patterns(name):
    global grid 
    if name in patterns:
        pattern = patterns[name]
        grid = np.zeros((ROWS, COLS), dtype=int)
        offset_x = ROWS // 4
        offset_y = COLS // 4
        for x, y in pattern:
            if 0 <= offset_x + x < ROWS and 0 <= offset_y + y < COLS:
                grid[offset_x + x, offset_y + y] = 1
    else: 
        print(f"Pattern '{name}' not found in predefined patterns.")

# Main 
def game_loop(mode):
    global grid, cell_size, game_ended, counter
    running = True 
    playing = False 
    
    if mode == "sample":
        selected_pattern = pattern_menu()
        load_patterns(selected_pattern)
    elif mode == "play":
        grid = np.zeros((ROWS, COLS), dtype=int)
    
    while running:
        clock.tick(0)
        previous_grid = grid.copy()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:    # Start or pause the game
                    playing = not playing
                elif event.key == pygame.K_c:      # Clear grid
                    grid = np.zeros((ROWS, COLS), dtype=int)
                    game_ended = False
                    counter = 0
                elif event.key == pygame.K_r:      # Reset gamr
                    grid = np.zeros((ROWS, COLS), dtype=int)
                    playing = False
                    game_ended = False
                    counter = 0
                elif event.key == pygame.K_EQUALS or event.key == pygame.K_PLUS:
                    if cell_size < 100:
                        cell_size += 2
                elif event.key == pygame.K_MINUS or event.key == pygame.K_UNDERSCORE:
                    if cell_size > 4:
                        cell_size -= 2
                elif event.key == pygame.K_ESCAPE:
                    return
            elif pygame.mouse.get_pressed()[0]:
                x,y = pygame.mouse.get_pos()
                row = y // cell_size
                col = x // cell_size
                if 0 <= row < ROWS and 0 <= col < COLS:
                    grid[row, col] = 1

        if playing:
            grid = update(grid)
            counter += 1
            if np.array_equal(previous_grid, grid):
                playing = False 
                game_ended = True

        draw_grid(grid)

while True:
    mode = main_menu()
    game_loop(mode)

pygame.quit()