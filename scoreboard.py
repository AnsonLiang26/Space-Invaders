import pygame.font

from pygame.sprite import Group
from cyborg import Cyborg

class Scoreboard():

    # Initialize scoreboard
    def __init__(self, game_settings, screen, stats):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.game_settings = game_settings
        self.stats = stats
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)

        # Prepare images.
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_cyborgs()
    
    # Prepare score image
    def prep_score(self):
        rounded_score = int(round(self.stats.score, -1))
        score_str = "Score: {:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True, self.text_color, self.game_settings.bg_color)
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20
    
    # Display score image
    def show_score(self):
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.screen.blit(self.lives_image, self.lives_rect)
        self.cyborgs.draw(self.screen)
    
    # Prepare high score image
    def prep_high_score(self):
        high_score = int(round(self.stats.high_score, -1))
        high_score_str = "High Score: {:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True, self.text_color, self.game_settings.bg_color)
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top
    
    # Prepare level image
    def prep_level(self):
        current_level = int(self.stats.level)
        current_level_str = "Level: {:,}".format(current_level, -1)
        self.level_image = self.font.render(current_level_str, True, self.text_color, self.game_settings.bg_color)
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10
    
    # Prepare cyborgs remaining image
    def prep_cyborgs(self):
        current_lives_str = "Lives: "
        self.lives_image = self.font.render(current_lives_str, True, self.text_color, self.game_settings.bg_color)
        self.lives_rect = self.lives_image.get_rect()
        self.lives_rect.left = self.screen_rect.left
        self.lives_rect.top = self.score_rect.top
        self.cyborgs = Group()
        for cyborg_number in range(self.stats.cyborgs_left):
            cyborg = Cyborg(self.game_settings, self.screen)
            cyborg.rect.x = 100 + cyborg_number * cyborg.rect.width
            cyborg.rect.y = 10
            self.cyborgs.add(cyborg)