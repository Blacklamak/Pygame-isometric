import pygame

ROOT = "images"
def load_image(path):
    return pygame.image.load(f"{ROOT}/{path}")