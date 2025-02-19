import sys

import pygame

from scripts.Player import Player
from scripts.utils import load_image
from scripts.playerunit import Unit
from scripts.block import IsoBlock
pygame.init()
# Initialize Pygame
class RTS:
    def __init__(self):

        # Screen dimensions
        self.screen_width = 800

        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

        #assests load
        self.assets ={
            'unit1' : load_image("player1.png")
        }
        # Load your tile image
        self.tile_image = pygame.image.load('images/block.png').convert_alpha()
        tile_width = self.tile_image.get_width()
        tile_height = self.tile_image.get_height()

        # Isometric tile dimensions
        self.iso_width = tile_width // 2
        self.iso_height = tile_height // 2

        #tilemap = load_map("tilemap.txt")
        self.player = Player(self.screen, [3, 3])

        self.clock = pygame.time.Clock()

    def load(self):
        with open("map.txt", "r") as file:
            map_tile = []  # Initialize an empty tilemap
            current_layer = [] # Temporary holder for the current layer
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
        return map_tile

    def render_tilemap(self, tilemap):

        for z, diagonal in enumerate(tilemap):
            for y, row in enumerate(diagonal):
                for x, tile_type in enumerate(row):
                    if tile_type == 0:
                        # Calculate isometric position
                        iso_x = (x - y) * self.iso_width + self.screen_width // 2
                        iso_y = (x + y) * (self.iso_height // 2) - (z * 16)

                        rect = (iso_x-16, iso_y-16, self.iso_width*2, self.iso_height)
                        self.map_tile_rect.append(rect) #append the collision property
                        print(rect)
                        self.screen.blit(self.tile_image, (iso_x-16, iso_y-16))

    def run(self):
        # Main loop
        running = True
        tilemap = self.load()
        self.map_tile_rect = []
        test1 = Unit(self)

        while running:
            #print(map_tile_rect)
            map_tile_rect = []

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.screen.fill((0, 0, 0))

            self.render_tilemap(tilemap)

            self.player.move(map_tile_rect)
            test1.render()

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()

RTS().run()