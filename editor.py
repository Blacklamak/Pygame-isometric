import pygame
import sys

# Initialize Pygame
pygame.init()

# Set the window size
window_size = (800, 600)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Pygame Window")

#tile
tile = pygame.image.load("images/block.png").convert_alpha()

TILE_SIZE = 32

# Define the white color
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)

#mouse
pygame.mouse.set_visible(False)
pygame.event.set_grab(True)


map_tile = [[[-1 for x in range(window_size[0]//TILE_SIZE)] for y in range(window_size[1]//TILE_SIZE)]for z in range(5)]


def iso_points(x, y):
    iso_x = (x - y) * TILE_SIZE//2 + 400
    iso_y = (x+y) * TILE_SIZE//4
    return iso_x, iso_y

#grid normal
def grid():
    for y in range(0, window_size[1] // TILE_SIZE + 1 ):
        for x in range(0, window_size[0]// TILE_SIZE + 1):

            pygame.draw.line(screen, black, (iso_points(x, 0)), (iso_points(x, window_size[1])))
            pygame.draw.line(screen, black, (iso_points(0, y)), (iso_points(window_size[0], y)))

def pointer(pos):
    pygame.draw.circle(screen, red, pos, 5)

#render

def render_tilemap(tilemap):
    for z, diagonal in enumerate(tilemap):
        for y, row in enumerate(diagonal):
            for x, tile_type in enumerate(row):
                if tile_type == 0:
                    # Calculate isometric position
                    iso_x = (x - y) * (TILE_SIZE//2) + window_size[0] // 2
                    iso_y = (x + y) * (TILE_SIZE //4) - (z * 16)
                    screen.blit(tile, (iso_x-16, iso_y-16))

def save():
    with open("map.txt", 'w') as file:
        for z, layer in enumerate(map_tile):  # Iterate over Z-layers
            file.write(f"--layer {z}--\n")  # Add a layer separator
            for row in layer:  # Iterate over rows in the layer
                file.write(" ".join(str(u) for u in row) + "\n")
    print("saved")


def load():
    global map_tile
    with open("map.txt", "r") as file:
        map_tile = []  # Initialize an empty tilemap
        current_layer = []  # Temporary holder for the current layer
        for line in file:
            line = line.strip()
            if line.startswith("--layer"):  # Detect layer markers
                if current_layer:  # If we have data for a layer, append it
                    map_tile.append(current_layer)
                    current_layer = []  # Reset for the next layer
            else:
                # Parse the row into integers and add it to the current layer
                current_layer.append(list(map(int, line.split())))
        if current_layer:  # Add the final layer
            map_tile.append(current_layer)
    print("loaded")



# Main loop
running = True
is_drawing = False
z=0
while running:
    mx, my = pygame.mouse.get_pos()
    screen.fill(white)
    # Fill the window with white

    grid()
    render_tilemap(map_tile)
    #adjusted pointer placement
    iso_mx, iso_my = iso_points(mx, my)
    iso_mx = (iso_mx // TILE_SIZE) + 400
    iso_my = (iso_my // TILE_SIZE) - (z*16)
    pointer((iso_mx, iso_my))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                is_drawing = True
                map_tile[z][my // TILE_SIZE][mx // TILE_SIZE] = 0
                print(map_tile)
            elif event.button == 3:
                map_tile[z][my // TILE_SIZE][mx // TILE_SIZE] = -1



        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 or event.button == 3:
                is_drawing = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_s:
                save()
            if event.key == pygame.K_l:
                load()
            if event.key == pygame.K_UP:
                if z <= 4:
                    z += 1
                    print(z)
            elif event.key == pygame.K_DOWN:
                if z >= 1:
                    z -= 1
                    print(z)

    if is_drawing:
        mx, my = pygame.mouse.get_pos()
        map_tile[z][my // TILE_SIZE][mx // TILE_SIZE] = 0
        print(map_tile)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
