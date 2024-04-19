import sys
import pygame

from time import sleep
from laser import Laser
from enemy import Enemy

# Movement/ fire laser/ exit
def check_keydown_events(event, game_settings, screen, cyborg, lasers):
    if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
        cyborg.moving_right = True
    elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
        cyborg.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_laser(game_settings, screen, cyborg, lasers)
    elif event.key == pygame.K_q:
        sys.exit()

# Fire laser until limit is reached
def fire_laser(game_settings, screen, cyborg, lasers):
        if len(lasers) < game_settings.lasers_allowed:
            new_laser = Laser(game_settings, screen, cyborg)
            lasers.add(new_laser)

# Stop movement 
def check_keyup_events(event, cyborg):
    if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
        cyborg.moving_right = False
    elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
        cyborg.moving_left = False

# Mouse inputs
def check_events(game_settings, screen, stats, sb, play_button, cyborg, enemies, lasers):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, game_settings, screen, cyborg, lasers)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, cyborg)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(game_settings, screen, stats, sb, play_button, cyborg, enemies, lasers, mouse_x, mouse_y)

# Play button clicked
def check_play_button(game_settings, screen, stats, sb, play_button, cyborg, enemies, lasers, mouse_x, mouse_y):
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # Reset game
        game_settings.initialize_dynamic_settings()
        pygame.mouse.set_visible(False)
        stats.reset_stats()
        stats.game_active = True

        # Reset objects
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_cyborgs()

        enemies.empty()
        lasers.empty()

        # Create a new fleet and cyborg
        create_fleet(game_settings, screen, cyborg, enemies)
        cyborg.center_cyborg()

# Update objects on the screen
def update_screen(game_settings, screen, stats, sb, cyborg, enemies, lasers, play_button):
    screen.fill(game_settings.bg_color)
    for laser in lasers.sprites():
        laser.draw_laser()
    cyborg.blitme()
    enemies.draw(screen)
    sb.show_score()
    if not stats.game_active:
        play_button.draw_button()
    pygame.display.flip()

# Update lasers
def update_lasers(game_settings, screen, stats, sb, cyborg, enemies, lasers):
    lasers.update()
    for laser in lasers.copy():
        if laser.rect.bottom <= 0:
            lasers.remove(laser)
    check_laser_enemy_collisions(game_settings, screen, stats, sb, cyborg, enemies, lasers)

# Check if laser hit
def check_laser_enemy_collisions(game_settings, screen, stats, sb, cyborg, enemies, lasers):
    collisions = pygame.sprite.groupcollide(lasers, enemies, True, True)
    if collisions:
        for enemies in collisions.values():
            stats.score += game_settings.enemy_points * len(enemies)
            sb.prep_score()
        check_high_score(stats, sb)

    # If all enemies defeated, create new level
    if len(enemies) == 0:
        lasers.empty()
        game_settings.increase_speed()
        stats.level += 1
        sb.prep_level()
        create_fleet(game_settings, screen, cyborg, enemies)

# Calculate number of enemies
def get_number_enemies_x(game_settings, enemy_width):
    """Determine the number of aliens that fit in a row."""
    available_space_x = game_settings.screen_width - 2 * enemy_width
    number_enemies_x = int(available_space_x / (2 * enemy_width))
    return number_enemies_x

# Calculate number of enemy rows
def get_number_rows(game_settings, cyborg_height, enemy_height):
    available_space_y = (game_settings.screen_height - (3 * enemy_height) - cyborg_height)
    number_rows = int(available_space_y / (2 * enemy_height))
    return number_rows

# Create enemy in the row
def create_enemy(game_settings, screen, enemies, enemy_number, row_number):
    enemy = Enemy(game_settings, screen)
    enemy_width = enemy.rect.width
    enemy.x = enemy_width + 2 * enemy_width * enemy_number
    enemy.rect.x = enemy.x
    enemy.rect.y = enemy.rect.height + 2 * enemy.rect.height * row_number
    enemy.add(enemies)

# Create fleet of enemies
def create_fleet(game_settings, screen, cyborg, enemies):
    enemy = Enemy(game_settings, screen)
    number_enemies_x = get_number_enemies_x(game_settings, enemy.rect.width)
    number_rows = get_number_rows(game_settings, cyborg.rect.height, enemy.rect.height)
    for row_number in range(number_rows):
        for enemy_number in range(number_enemies_x):
            create_enemy(game_settings, screen, enemies, enemy_number, row_number)

# If an edge is hit, change directions
def check_fleet_edges(game_settings, enemies):
    for enemy in enemies.sprites():
        if enemy.check_edges():
            change_fleet_direction(game_settings, enemies)
            break

# Change directions
def change_fleet_direction(game_settings, enemies):
    for enemy in enemies.sprites():
        enemy.rect.y += game_settings.fleet_drop_speed
    game_settings.fleet_direction *= -1

# If enemies hit the bottom, lose a life
def check_enemies_bottom(game_settings, screen, stats, sb, cyborg, enemies, lasers):
    screen_rect = screen.get_rect()
    for enemy in enemies.sprites():
        if enemy.rect.bottom >= screen_rect.bottom:
            cyborg_hit(game_settings, screen, stats, sb, cyborg, enemies, lasers)
            break

# Once an edge is hit, lower the row
def update_enemies(game_settings, screen, stats, sb, cyborg, enemies, lasers):
    check_fleet_edges(game_settings, enemies)
    enemies.update()
    if pygame.sprite.spritecollideany(cyborg, enemies):
        cyborg_hit(game_settings, screen, stats, sb, cyborg, enemies, lasers)
    check_enemies_bottom(game_settings, screen, stats, sb, cyborg, enemies, lasers)

# Cyborg is hit
def cyborg_hit(game_settings, screen, stats, sb, cyborg, enemies, lasers):
    if stats.cyborgs_left > 0:
        stats.cyborgs_left -= 1
        sb.prep_cyborgs()
        enemies.empty()
        lasers.empty()
        create_fleet(game_settings, screen, cyborg, enemies)
        cyborg.center_cyborg()
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

# Check high score
def check_high_score(stats, sb):
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()