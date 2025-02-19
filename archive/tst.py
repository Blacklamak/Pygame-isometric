import pygame
import sys

from editor import MAX_LAYERS

# Pygame Initialization
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
TILE_SIZE = 32
GRID_WIDTH, GRID_HEIGHT = SCREEN_WIDTH // TILE_SIZE, SCREEN_HEIGHT // TILE_SIZE

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

# Tile Types (for simplicity, we will use numbers to represent tiles)
TILE_TYPES = [
    pygame.Surface((TILE_SIZE, TILE_SIZE)),
    pygame.Surface((TILE_SIZE, TILE_SIZE)),
]

# Fill tile types with colors (just an example)
TILE_TYPES[0].fill((0, 255, 0))  # Green tile
TILE_TYPES[1].fill((0, 0, 255))  # Blue tile

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tilemap Editor")

# Tilemap data (2D array), default with -1 for empty tiles
tilemap = [[[-1 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT) for _ in range(MAX_LAYERS)]]


# Tile selector variables
selected_tile = 0  # Default to the first tile type

def draw_grid():
    """Draws the grid lines on the screen."""
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            pygame.draw.rect(screen, GRAY, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE), 1)

def draw_tilemap():
    """Draws the tiles based on the current tilemap data."""
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            tile_id = tilemap[y][x]
            if tile_id != -1:
                screen.blit(TILE_TYPES[tile_id], (x * TILE_SIZE, y * TILE_SIZE))

def main():
    global selected_tile
    running = True
    while running:
        screen.fill(WHITE)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click to place tile
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    grid_x, grid_y = mouse_x // TILE_SIZE, mouse_y // TILE_SIZE
                    tilemap[grid_y][grid_x] = selected_tile
                elif event.button == 3:  # Right click to remove tile
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    grid_x, grid_y = mouse_x // TILE_SIZE, mouse_y // TILE_SIZE
                    tilemap[grid_y][grid_x] = -1
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:  # Press '1' to select tile 1
                    selected_tile = 0
                elif event.key == pygame.K_2:  # Press '2' to select tile 2
                    selected_tile = 1
                elif event.key == pygame.K_s:  # Press 'S' to save the tilemap
                    save_tilemap()
                elif event.key == pygame.K_l:  # Press 'L' to load the tilemap
                    load_tilemap()

        # Drawing
        draw_grid()
        draw_tilemap()

        # Show selected tile
        pygame.draw.rect(screen, BLACK, (0, 0, TILE_SIZE, TILE_SIZE), 2)
        screen.blit(TILE_TYPES[selected_tile], (0, 0))

        pygame.display.flip()

    pygame.quit()
    sys.exit()

def save_tilemap():
    """Save the tilemap to a file using a simple 2D list."""
    with open("../tilemap.txt", "w") as file:
        for row in tilemap:
            file.write(" ".join(str(cell) for cell in row) + "\n")

def load_tilemap():
    """Load the tilemap from a file into the 2D list."""
    global tilemap
    try:
        with open("../tilemap.txt", "r") as file:
            tilemap = []
            for line in file:
                row = list(map(int, line.strip().split()))
                tilemap.append(row)
    except FileNotFoundError:
        print("Tilemap file not found. Starting with an empty tilemap.")

if __name__ == "__main__":
    main()
