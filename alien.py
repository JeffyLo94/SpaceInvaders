import pygame
from pygame.sprite import Sprite
from random import choice


class Alien(Sprite):

    def __init__(self, ai_settings, screen, alien_type='classic'):
        super(Alien, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        self.alienType = alien_type

        # Load the alien image, and set its rect attribute.
        self.imageSet = None
        self.explosionSet = None
        self.images = None
        self.explosion_frames = None
        self.currImgInd = None
        self.expImgInd = None
        self.image = None
        self.rect = None
        self.last_frame_time = None
        self.init_images()

        self.isDead = False

        # Start each new alien near the top left of the screen.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the alien's exact position.
        self.x = float(self.rect.x)

    def check_edges(self):
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    def init_images(self):
        self.imageSet = self.ai_settings.alien_image_names[self.alienType]
        self.explosionSet = self.ai_settings.alien_explosions[self.alienType]

        self.images = [
            pygame.image.load(self.imageSet[0]),
            pygame.image.load(self.imageSet[1])
        ]
        self.explosion_frames = [
            pygame.image.load(self.explosionSet[0]),
            pygame.image.load(self.explosionSet[1]),
            pygame.image.load(self.explosionSet[2]),
            pygame.image.load(self.explosionSet[3])
        ]
        self.currImgInd = 0
        self.image = self.images[self.currImgInd]
        self.rect = self.image.get_rect()
        self.last_frame_time = pygame.time.get_ticks()

    def toggle_image(self):
        if self.currImgInd == 0:
            self.image = self.images[1]
            self.currImgInd = 1
        else:
            self.image = self.images[0]
            self.currImgInd = 0

    def flag_for_death(self):
        self.isDead = True
        self.expImgInd = 0
        self.image = self.explosion_frames[self.expImgInd]
        self.last_frame_time = pygame.time.get_ticks()

    def update(self):
        self.x += (self.ai_settings.alien_speed_factor *
                   self.ai_settings.fleet_direction)
        self.rect.x = self.x
        # animations
        curr_ticks = pygame.time.get_ticks()
        if not self.isDead:
            if abs(self.last_frame_time - curr_ticks) > self.ai_settings.alien_animate_time:
                self.last_frame_time = curr_ticks
                self.toggle_image()
        else:
            if abs(self.last_frame_time - curr_ticks) > self.ai_settings.alien_animate_expl_time:
                self.last_frame_time = curr_ticks
                self.expImgInd += 1
                if self.expImgInd < len(self.explosion_frames):
                    self.image = self.explosion_frames[self.expImgInd]
                else:
                    self.kill()

    def blitme(self):
        self.screen.blit(self.image, self.rect)


class Ufo(Sprite):
    def __init__(self, ai_settings, screen):
        super().__init__()
        # screen, settings, score values
        self.screen = screen
        self.ai_settings = ai_settings
        self.possible_scores = ai_settings.ufo_point_values
        self.score = None

        # images, score text
        self.image = pygame.image.load(ai_settings.ufo_image)
        self.rect = self.image.get_rect()
        self.score_image = None
        self.font = pygame.sysfont.SysFont(None, 32, italic=True)
        self.prep_score()

        self.expl_frames = []
        self.explosionInd = None
        # self.expl_frames.append(pygame.image.load(s))
        self.expl_frames.append(self.score_image)
        self.last_frame = None
        self.wait_interval = 500

        # initial position, speed/direction
        self.speed = ai_settings.ufo_speed * (choice([-1, 1]))
        self.rect.x = 0 if self.speed > 0 else ai_settings.screen_width
        self.rect.y = ai_settings.screen_height * 0.1

        # death flag
        self.isDead = False

    def flag_for_death(self):
        self.isDead = True
        self.explosionInd = 0
        self.image = self.expl_frames[self.explosionInd]
        self.last_frame = pygame.time.get_ticks()

    def get_score(self):
        """Get a random score from the UFO's possible score values"""
        self.score = choice(self.possible_scores)
        return self.score

    def prep_score(self):
        score_str = str(self.get_score())
        self.score_image = self.font.render(score_str, True, (255, 0, 0), self.ai_settings.bg_color)

    def update(self):
        if not self.isDead:
            self.rect.x += self.speed
            if self.speed > 0 and self.rect.left > self.ai_settings.screen_width:
                self.kill()
            elif self.rect.right < 0:
                self.kill()
        else:
            time_test = pygame.time.get_ticks()
            if abs(time_test - self.last_frame) > self.wait_interval:
                self.last_frame = time_test
                self.explosionInd += 1
                if self.explosionInd >= len(self.expl_frames):
                    self.kill()
                else:
                    self.image = self.expl_frames[self.explosionInd]
                    self.wait_interval += 500

    def blitme(self):
        self.screen.blit(self.image, self.rect)
