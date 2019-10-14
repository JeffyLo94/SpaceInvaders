from os.path import abspath, dirname
# from pygame import *
from text import Text


class Settings:

    def __init__(self):
        self.player_name = 'PL1'

        self.WHITE = (255, 255, 255)
        self.GREEN = (78, 255, 87)
        self.YELLOW = (241, 255, 0)
        self.BLUE = (80, 255, 239)
        self.PURPLE = (203, 0, 255)
        self.RED = (237, 28, 36)

        self.BASE_PATH = abspath(dirname(__file__)) + '/assets'
        self.IMAGE_PATH = self.BASE_PATH + '/images/'
        self.SOUND_PATH = self.BASE_PATH + '/sounds/'
        self.DATA_PATH = self.BASE_PATH + '/data/'

        self.high_score_datafile = self.DATA_PATH + 'highscores.json'

        self.tick_rate = 60

        # Screen settings.
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (49, 51, 53)

        # Text Settings
        self.text_color = (255, 255, 255)
        self.alt_text_color = (0, 255, 0)
        self.font_size = 48

        self.titleText = Text(None, 50, 'Space Invaders', self.WHITE, 164, 155)
        self.titleText2 = Text(None, 25, 'Press any key to continue', self.WHITE,
                               201, 225)
        self.gameOverText = Text(None, 50, 'Game Over', self.WHITE, 250, 270)
        self.nextRoundText = Text(None, 50, 'Next Round', self.WHITE, 240, 270)
        self.enemy1Text = Text(None, 25, '   =   10 pts', self.GREEN, 368, 270)
        self.enemy2Text = Text(None, 25, '   =  20 pts', self.BLUE, 368, 320)
        self.enemy3Text = Text(None, 25, '   =  30 pts', self.PURPLE, 368, 370)
        self.enemy4Text = Text(None, 25, '   =  ?????', self.RED, 368, 420)

        # Button settings
        self.btn_color = (0, 255, 0)
        self.btn_w = 200
        self.btn_h = 50

        # Bunker settings
        self.bunker_size_h = 10
        self.bunker_size_w = 15
        self.bunker_color = (0, 255, 0)
        self.destruction_factor = 2
        self.bunker_rows = 5
        self.bunker_cols = 9

        # Ship settings.
        self.ship_image = self.IMAGE_PATH + 'spaceship.png'
        self.ship_explosions = [self.IMAGE_PATH +
                                'ship_explosion1.png',
                                self.IMAGE_PATH + 'ship_explosion2.png',
                                self.IMAGE_PATH + 'ship_explosion3.png',
                                self.IMAGE_PATH + 'ship_explosion4.png',
                                self.IMAGE_PATH + 'ship_explosion5.png',
                                self.IMAGE_PATH + 'ship_explosion6.png',
                                self.IMAGE_PATH + 'ship_explosion7.png',
                                self.IMAGE_PATH + 'ship_explosion8.png']
        self.ship_explosion_time = 200
        self.ship_limit = 3

        # Bullet settings.
        self.bullet_width = 5
        self.bullet_height = 15
        self.bullet_color = 255, 48, 65
        self.bullets_allowed = 3

        # Alien Lazer setting
        self.laser_width = 5
        self.laser_height = 10
        self.laser_color = 65, 48, 255
        self.lasers_allowed = 1
        self.laser_stamp = None
        self.laser_time = 1000

        # Alien settings.
        self.ufo_image = self.IMAGE_PATH + 'UFO.png'

        self.alien_explosions = {
            'classic': [self.IMAGE_PATH + 'purple_explosion1.png',
                        self.IMAGE_PATH + 'purple_explosion2.png',
                        self.IMAGE_PATH + 'purple_explosion3.png',
                        self.IMAGE_PATH + 'purple_explosion4.png'],
            'ghost': [self.IMAGE_PATH + 'blue_explosion1.png',
                      self.IMAGE_PATH + 'blue_explosion2.png',
                      self.IMAGE_PATH + 'blue_explosion3.png',
                      self.IMAGE_PATH + 'blue_explosion4.png'],
            'creeper': [self.IMAGE_PATH + 'green_explosion1.png',
                        self.IMAGE_PATH + 'green_explosion2.png',
                        self.IMAGE_PATH + 'green_explosion3.png',
                        self.IMAGE_PATH + 'green_explosion4.png']
        }
        self.alien_classic1 = self.IMAGE_PATH + 'alien-classic-frame1.png'
        self.alien_classic2 = self.IMAGE_PATH + 'alien-classic-frame2.png'
        self.alien_creep1 = self.IMAGE_PATH + 'alien-creep-frame1.png'
        self.alien_creep2 = self.IMAGE_PATH + 'alien-creep-frame2.png'
        self.alien_ghost1 = self.IMAGE_PATH + 'alien-ghost-frame1.png'
        self.alien_ghost2 = self.IMAGE_PATH + 'alien-ghost-frame2.png'
        self.alien_squid1 = self.IMAGE_PATH + 'alien-squid-frame1.png'
        self.alien_squid2 = self.IMAGE_PATH + 'alien-squid-frame2.png'
        self.alien_image_names = {
            'classic': [self.alien_classic1, self.alien_classic2],
            'ghost': [self.alien_ghost1, self.alien_ghost2],
            'creeper': [self.alien_creep1, self.alien_creep2]
        }
        # time in ms
        self.alien_animate_time = 1000
        self.alien_animate_expl_time = 50

        self.fleet_drop_speed = 10
        self.alien_points = {
            'classic': 10,
            'ghost': 20,
            'creeper': 40
        }
        self.ufo_point_values = [100, 200, 300]
        self.last_ufo = None
        self.ufo_spawn_time = 10000
        self.num_alien_rows = 5
        # fleet_direction of 1 represents right, -1 represents left.
        self.fleet_direction = 1

        # init speed settings
        # Windows
        # self.ship_speed_factor = 1.5
        # self.bullet_speed_factor = 3
        # self.laser_speed_factor = 3
        # self.alien_speed_factor = 1
        # self.base_alien_speed = 1.5

        # MAC
        self.ship_speed_factor = 7
        self.bullet_speed_factor = 15
        self.laser_speed_factor = 10
        self.alien_speed_factor = 5
        self.base_alien_speed = 5
        self.alien_speed_limit = None
        self.alien_base_limit = None
        self.ufo_speed = None

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
        self.ship_speed_factor = 7
        self.bullet_speed_factor = 15
        self.laser_speed_factor = 10
        self.alien_speed_factor = 5

        # fleet_direction of 1 represents right, -1 represents left.
        self.fleet_direction = 1

        self.alien_speed_limit = self.alien_speed_factor * 5
        self.alien_base_limit = self.alien_speed_limit / 2
        self.ufo_speed = self.alien_speed_factor * 2

    def increase_speed(self):
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)

    def increase_alien_base_speed(self):
        if self.base_alien_speed < self.alien_base_limit:
            self.base_alien_speed *= self.speedup_scale

    def increase_alien_speed(self):
        self.alien_speed_factor *= self.speedup_scale

    def reset_alien_speed(self):
        self.alien_speed_factor = self.base_alien_speed
