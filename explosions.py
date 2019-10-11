from pygame import *
from pygame.sprite import Sprite

class alien_explosion(Sprite):
    def __init__(self, enemy, ai_settings, screen, *groups):
        super(alien_explosion, self).__init__(*groups)
        self.ai_settings = ai_settings
        self.image = transform.scale(self.get_image(enemy.row), (40, 35))
        self.image2 = transform.scale(self.get_image(enemy.row), (50, 45))
        self.rect = self.image.get_rect(topleft=(enemy.rect.x, enemy.rect.y))
        self.timer = time.get_ticks()

    # @staticmethod
    def get_image(self, row):
        img_colors = ['purple', 'blue', 'blue', 'green', 'green']
        IMAGES = { name: image.load(self.ai_settings.IMAGE_PATH + {} )}
        return IMAGES['explosion{}'.format(img_colors[row])]

    def update(self, current_time, *args):
        passed = current_time - self.timer
        if passed <= 100:
            game.screen.blit(self.image, self.rect)
        elif passed <= 200:
            game.screen.blit(self.image2, (self.rect.x - 6, self.rect.y - 6))
        elif 400 < passed:
            self.kill()