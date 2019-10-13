import pygame
from pygame.sprite import Sprite


class Ship(Sprite):

    def __init__(self, ai_settings, screen):
        super(Ship, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # Load the ship image, and get its rect.
        self.image = pygame.image.load(ai_settings.ship_image)
        self.expl_frames = [
            pygame.image.load(ai_settings.ship_explosions[i]) for i in range(len(ai_settings.ship_explosions))
        ]
        self.last_frame_timer = None
        self.expl_ind = None

        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # Start each new ship at the bottom center of the screen.
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        # Store a decimal value for the ship's center.
        self.center = float(self.rect.centerx)

        # Movement flags.
        self.moving_right = False
        self.moving_left = False

        self.isDead = False

    def center_ship(self):
        self.center = self.screen_rect.centerx

    def update(self):
        if not self.isDead:
            # Update the ship's center value, not the rect.
            if self.moving_right and self.rect.right < self.screen_rect.right:
                self.center += self.ai_settings.ship_speed_factor
            if self.moving_left and self.rect.left > 0:
                self.center -= self.ai_settings.ship_speed_factor

            # Update rect object from self.center.
            self.rect.centerx = self.center
        else:
            curr_tick = pygame.time.get_ticks()
            if abs(self.last_frame_timer - curr_tick) > self.ai_settings.ship_explosion_time:
                self.expl_ind += 1
                if self.expl_ind < len(self.expl_frames):
                    # self.image = self.expl_frames[self.expl_ind]
                    self.image = pygame.image.load(self.ai_settings.ship_explosions[self.expl_ind])
                    # print(self.ai_settings.ship_explosions[self.expl_ind])
                    self.last_frame_timer = curr_tick
                else:
                    self.isDead = False
                    self.image = pygame.image.load(self.ai_settings.ship_image)

    def trigger_death(self):
        self.isDead = True
        self.expl_ind = 0
        self.image = self.expl_frames[self.expl_ind]
        self.last_frame_timer = pygame.time.get_ticks()

    def blitme(self):
        # self.rect = self.image.get_rect()
        self.screen.blit(self.image, self.rect)
