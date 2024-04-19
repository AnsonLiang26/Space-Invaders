class GameStats():
    # Initialize game stats
    def __init__(self, game_settings):
        self.game_settings = game_settings
        self.reset_stats()
        self.game_active = False
        self.high_score = 0
    
    # Reset stats
    def reset_stats(self):
        self.cyborgs_left = self.game_settings.cyborg_limit
        self.score = 0
        self.level = 1