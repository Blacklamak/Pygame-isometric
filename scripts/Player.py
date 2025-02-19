import pygame
class Player:
    def __init__(self, screen, start_pos):
        self.screen = screen
        self.player = pygame.image.load('images/wiz.png').convert_alpha()
        self.start_pos = start_pos
        self.pos = [float(start_pos[0]), float(start_pos[0]), 0.0]  # x, y, z positions
        self.vel = [0.0, 0.0, 0.0]  # x, y, z velocities
        self.is_jumping = False
        self.gravity = -0.05
        self.jump_strength = 0.5
        self.player_width = self.player.get_width()
        self.player_height = self.player.get_height()

    def pos_iso(self):
        # Calculate isometric positio                                           n
        screen_width = self.screen.get_width()
        iso_width = self.player_width // 2
        iso_height = self.player_height // 2
        iso_x = (self.pos[0] - self.pos[1]) * iso_width + screen_width // 2
        iso_y = (self.pos[0] + self.pos[1]) * (iso_height // 2) - (self.pos[2] * 16)
        return iso_x, iso_y

    def move(self, tile_rect):
        # Update position based on velocity
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]

        # Update z-position (jump and gravity)
        if self.is_jumping:
            self.pos[2] += self.vel[2]
            self.vel[2] += self.gravity
            if self.pos[2] <= 0:  # Reset if landed
                self.pos[2] = 0
                self.vel[2] = 0
                self.is_jumping = False

        # Check for key presses
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.vel[1] = -0.2
        elif keys[pygame.K_s]:
            self.vel[1] = 0.2
        else:
            self.vel[1] = 0

        if keys[pygame.K_a]:
            self.vel[0] = -0.2
        elif keys[pygame.K_d]:
            self.vel[0] = 0.2
        else:
            self.vel[0] = 0

        # Jumping logic
        if keys[pygame.K_SPACE] and not self.is_jumping:
            self.is_jumping = True
            self.vel[2] = self.jump_strength

        # Calculate isometric position and update collision rect
        iso_x, iso_y = self.pos_iso()
        self.player_rect = pygame.Rect(
            iso_x, iso_y, self.player_width, self.player_height
        )  # Update collision rectangle

        # Collision check
        self.check_collision(tile_rect)

        # Render player at isometric position
        self.screen.blit(self.player, (iso_x, iso_y))

    def check_collision(self, tile_rect):
        for rect in tile_rect:
            tile_collision_rect = pygame.Rect(*rect)
            if self.player_rect.colliderect(tile_collision_rect):
                print(f"Collision with tile at: {tile_collision_rect}")
