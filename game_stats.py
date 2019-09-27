class GameStats:

    def __init__(self, ai_settings):
        self.ai_settings = ai_settings

        # init to get rid of pep8 warning
        self.ships_left = 0
        self.score = 0
        self.level = 0

        self.reset_stats()

        # Start game in an inactive state.
        self.game_active = False

        # High score should never be reset.
        self.high_score = 0

    def reset_stats(self):
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1
