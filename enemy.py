import pygame

from pygame.sprite import Sprite

class Enemy(Sprite):
    
    # Initialize enemy
    def __init__(self, game_settings, screen):
        super(Enemy, self).__init__()
        self.screen = screen
        self.game_settings = game_settings
        self.image = pygame.image.load('images/enemy.bmp')
        self.rect = self.image.get_rect()
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        self.x = float(self.rect.x)
    
    # Draw enemy in current location
    def blitme(self):
        self.screen.blit(self.image, self.rect)
    
    # Return true if enemy hits edge
    def check_edges(self):
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True
    
    # Move enemy
    def update(self):
        self.x += (self.game_settings.enemy_speed_factor * self.game_settings.fleet_direction)
        self.rect.x = self.x