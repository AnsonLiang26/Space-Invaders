class Settings():

    # Initialize game settings
    def __init__(self):
        self.screen_width = 1600
        self.screen_height = 1000
        self.bg_color = (230, 255, 255)

        # Cyborg settings
        self.cyborg_speed_factor = 1.5
        self.cyborg_limit = 3

        # Laser settings
        self.laser_speed_factor = 3
        self.laser_width = 3
        self.laser_height = 15
        self.laser_color = 255, 60, 60
        self.lasers_allowed = 3
        
        # Enemy settings
        self.fleet_drop_speed = 10

        # Level up settings
        self.speedup_scale = 1.1
        self.score_scale = 1.5
        self.initialize_dynamic_settings()

    # Initialize settings
    def initialize_dynamic_settings(self):
        self.cyborg_speed_factor = 1.5
        self.laser_speed_factor = 3
        self.enemy_speed_factor = 1
        self.fleet_direction = 1
        self.enemy_points = 10

    # Increase speed
    def increase_speed(self):
        self.cyborg_speed_factor *= self.speedup_scale
        self.laser_speed_factor *= self.speedup_scale
        self.enemy_speed_factor *= self.speedup_scale
        self.enemy_points = int(self.enemy_points * self.score_scale)