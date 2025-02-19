import pygame

class IsoBlock:
    def __init__(self, x, y, z, iso_width, iso_height):
        self.x = x
        self.y = y
        self.z = z  # Elevation for 3D isometric perspective
        self.iso_width = iso_width
        self.iso_height = iso_height

        # Define top face as a diamond shape (polygon)
        self.top_face = [
            (x, y - z),  # Top point
            (x + iso_width // 2, y + iso_height // 2 - z),  # Right point
            (x, y + iso_height - z),  # Bottom point
            (x - iso_width // 2, y + iso_height // 2 - z)  # Left point
        ]

        # Define left face (rectangle)
        self.left_face = pygame.Rect(x - iso_width // 2, y + iso_height // 2 - z, iso_width // 2, iso_height // 2)
        # Define right face (rectangle)
        self.right_face = pygame.Rect(x, y + iso_height // 2 - z, iso_width // 2, iso_height // 2)

    def draw(self, screen, color):
        # Draw top face
        pygame.draw.polygon(screen, color, self.top_face)
        # Draw left face
        pygame.draw.rect(screen, (color[0] // 2, color[1] // 2, color[2] // 2), self.left_face)
        # Draw right face
        pygame.draw.rect(screen, (color[0] // 3, color[1] // 3, color[2] // 3), self.right_face)

    def detect_collision(self, player_rect, block):
        # Check if the player overlaps with any of the block's collision regions
        collision_type = None

        # Top collision (using the top face polygon)
        if pygame.Rect(player_rect).collidepoint(block.top_face[0]) or \
           pygame.Rect(player_rect).collidepoint(block.top_face[2]):
            collision_type = "top"

        # Left collision
        if player_rect.colliderect(block.left_face):
            collision_type = "left"

        # Right collision
        if player_rect.colliderect(block.right_face):
            collision_type = "right"

        return collision_type
