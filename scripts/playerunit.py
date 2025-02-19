import pygame
class Unit:
    def __init__(self,script):
        self.script = script
        self.TILE_SIZE = 32
    def render(self):
        x = 0
        y = 0
        x, y = self.iso_points(x, y)
        self.script.screen.blit(self.script.assets['unit1'], (x, y))

    #normal coordinate to isometric coordintate
    def iso_points(self, x, y):
        iso_x = (x - y) * self.TILE_SIZE // 2 + 400
        iso_y = (x + y) * self.TILE_SIZE // 4
        return iso_x, iso_y