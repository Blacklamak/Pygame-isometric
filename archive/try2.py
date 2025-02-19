import pygame
import sys

# Initialize Pygame
pygame.init()

# Set the window size
window_size = (800, 600)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Pygame Window")

# Tile image (make sure you have a valid path to an image)
tile = pygame.image.load("../images/block.png").convert_alpha()

TILE_SIZE = 32

# Define colors
white = (255, 255, 255)
black = (0, 0, 0)

# Create a grid (map) that tracks tile type and height (Z-axis)
map_tile = [[[-1, 0] for x in range(window_size[0] // TILE_SIZE)] for y in range(window_size[1] // TILE_SIZE)]

def iso_points(x, y, z=0):
    """Convert grid (x, y) to isometric coordinates with a Z offset for stacking"""
    iso_x = (x - y) * TILE_SIZE // 2 + window_size[0] // 2
    iso_y = (x + y) * TILE_SIZE // 4 - (z * TILE_SIZE // 8)
    return iso_x, iso_y

def render_tilemap(tilemap):
    """Render the tilemap with consideration for Z-axis stacking"""
    for y, row in enumerate(tilemap):
        for x, tile_data in enumerate(row):
            tile_type, height = tile_data
            if tile_type == 0:  # If the tile is valid
                iso_x, iso_y = iso_points(x, y, height)
                screen.blit(tile, (iso_x, iso_y))

# Main loop
running = True
while running:
    mx, my = pygame.mouse.get_pos()
    screen.fill(white)

    # Render the grid and the tilemap
    render_tilemap(map_tile)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                # Calculate grid position
                grid_x = mx // TILE_SIZE
                grid_y = my // TILE_SIZE
                # Add a tile on top (increase Z-height)
                map_tile[grid_y][grid_x][0] = 0  # Place a tile
                map_tile[grid_y][grid_x][1] += 1  # Increase the height to stack the tile
                print(f"Tile placed at ({grid_x}, {grid_y}) with height {map_tile[grid_y][grid_x][1]}")

            if event.button == 3:
                # Remove the tile at this grid position
                grid_x = mx // TILE_SIZE
                grid_y = my // TILE_SIZE
                if map_tile[grid_y][grid_x][1] > 0:
                    map_tile[grid_y][grid_x][1] -= 1  # Decrease height (remove top tile)
                print(f"Tile removed at ({grid_x}, {grid_y})")

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
