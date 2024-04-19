import pygame
import game_functions

from pygame.sprite import Group
from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from cyborg import Cyborg
from enemy import Enemy

def run_game():
    # Initialize game, settings, and screen. Add name.
    pygame.init()
    game_settings = Settings()
    screen = pygame.display.set_mode((game_settings.screen_width, game_settings.screen_height))
    pygame.display.set_caption("Space Invaders")

    # Create the play button
    play_button = Button(game_settings, screen, "Play!")

    # Create an instance for stats and scoreboard.
    stats = GameStats(game_settings)
    sb = Scoreboard(game_settings, screen, stats)

    # Create a cyborg, lasers, and enemies.
    cyborg = Cyborg(game_settings, screen)
    lasers = Group()
    enemies = Group()

    # Create the fleet of enemies.
    game_functions.create_fleet(game_settings, screen, cyborg, enemies)

    # Make an enemy.
    enemy = Enemy(game_settings, screen)

    # Main game
    while True:
        game_functions.check_events(game_settings, screen, stats, sb, play_button, cyborg, enemies, lasers)

        if stats.game_active:
            cyborg.update()
            game_functions.update_lasers(game_settings, screen, stats, sb, cyborg, enemies, lasers)
            game_functions.update_enemies(game_settings, screen, stats, sb, cyborg, enemies, lasers)

        game_functions.update_screen(game_settings, screen, stats, sb, cyborg , enemies, lasers, play_button)

run_game()