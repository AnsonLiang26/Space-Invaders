import pygame

from pygame.sprite import Sprite

class Laser(Sprite):
    
    # Initialize laser
    def __init__(self, game_settings, screen, cyborg):
        super(Laser, self).__init__()
        self.screen = screen
        self.rect = pygame.Rect(0, 0, game_settings.laser_width, game_settings.laser_height)
        self.rect.centerx = cyborg.rect.centerx
        self.rect.top = cyborg.rect.top
        self.y = float(self.rect.y)
        self.color = game_settings.laser_color
        self.speed_factor = game_settings.laser_speed_factor

    # Update laser
    def update(self):
        self.y -= self.speed_factor
        self.rect.y = self.y
    
    # Draw laser image
    def draw_laser(self):
        pygame.draw.rect(self.screen, self.color, self.rect)