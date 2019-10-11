from os.path import abspath, dirname


class Settings:


    def __init__(self):
        self.BASE_PATH = abspath(dirname(__file__)) + '/assets'
        self.FONT_PATH = self.BASE_PATH + '/fonts/'
        self.IMAGE_PATH = self.BASE_PATH + '/images/'
        self.SOUND_PATH = self.BASE_PATH + '/sounds/'

        # Screen settings.
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (49, 51, 53)

        # Text Settings
        self.text_color = (255, 255, 255)
        self.font_size = 48

        # Button settings
        self.btn_color = (0, 255, 0)
        self.btn_w = 200
        self.btn_h = 50

        # Ship settings.
        self.ship_image = self.IMAGE_PATH + 'spaceship.png'
        self.ship_limit = 3

        # Bullet settings.
        self.bullet_width = 5
        self.bullet_height = 15
        self.bullet_color = 255, 48, 65
        self.bullets_allowed = 3

        # Alien settings.
        self.ufo_image = self.IMAGE_PATH + 'UFO.png'
        self.alien_classic1 = self.IMAGE_PATH + 'alien-classic-frame1.png'
        self.alien_classic2 = self.IMAGE_PATH + 'alien-classic-frame2.png'
        self.alien_creep1 = self.IMAGE_PATH + 'alien-creep-frame1.png'
        self.alien_creep2 = self.IMAGE_PATH + 'alien-creep-frame2.png'
        self.alien_ghost1 = self.IMAGE_PATH + 'alien-ghost-frame1.png'
        self.alien_ghost2 = self.IMAGE_PATH + 'alien-ghost-frame2.png'
        self.alien_squid1 = self.IMAGE_PATH + 'alien-squid-frame1.png'
        self.alien_squid2 = self.IMAGE_PATH + 'alien-squid-frame2.png'

        self.fleet_drop_speed = 10
        self.alien_points = 50
        # fleet_direction of 1 represents right, -1 represents left.
        self.fleet_direction = 1

        # init speed settings
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 1

        # How quickly the game speeds up.
        self.speedup_scale = 1.1
        # How quickly the alien point values increase.
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        # Windows Speed
        # self.ship_speed_factor = 1.5
        # self.bullet_speed_factor = 3
        # self.alien_speed_factor = 1

        # Mac Speed
        self.ship_speed_factor = 15
        self.bullet_speed_factor = 30
        self.alien_speed_factor = 10

        # Scoring.
        self.alien_points = 50

        # fleet_direction of 1 represents right, -1 represents left.
        self.fleet_direction = 1

    def increase_speed(self):
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)
