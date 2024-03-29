import pygame
from pygame.sprite import Sprite


class Laser(Sprite):
    def __init__(self, ai_settings, screen, alien):
        super(Laser, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        self.rect = pygame.Rect(0, 0, ai_settings.laser_width,
                                ai_settings.laser_height)
        self.rect.centerx = alien.rect.centerx
        self.rect.top = alien.rect.bottom

        self.y = float(self.rect.y)

        self.color = ai_settings.laser_color
        self.speed_factor = ai_settings.laser_speed_factor

    def update(self):
        self.y += self.speed_factor
        self.rect.y = self.y

    def draw_laser(self):
        pygame.draw.rect(self.screen, self.color, self.rect)
