import pygame

from pygame.sprite import Sprite

class Cyborg(Sprite):
    
    # Initialize cyborg
    def __init__(self, game_settings, screen):
        super(Cyborg, self).__init__()
        self.screen = screen
        self.game_settings = game_settings
        self.image = pygame.image.load('images/shooter.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        self.center = float(self.rect.centerx)
        self.moving_right = False
        self.moving_left = False
    
    # Update cyborg position
    def update(self):
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.game_settings.cyborg_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.game_settings.cyborg_speed_factor
        self.rect.centerx = self.center
    
    # Draw cyborg at current location
    def blitme(self):
        self.screen.blit(self.image, self.rect)
    
    # Center cyborg
    def center_cyborg(self):
        self.center = self.screen_rect.centerx