from pygame import sprite, Surface, PixelArray
from random import randrange


class Bunker(sprite.Sprite):
    def __init__(self, ai_settings, screen, row, col):
        super().__init__()
        self.screen = screen
        self.height = ai_settings.bunker_size_h
        self.width = ai_settings.bunker_size_w
        self.color = ai_settings.bunker_color
        self.image = Surface((self.width, self.height))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.row = row
        self.col = col
        self.dmg = False

    def damage(self, top):
        if not self.dmg:
            px_arr = PixelArray(self.image)
            if top:
                for i in range(self.height * 3):
                    px_arr[randrange(0, self.width - 1),
                           randrange(0, self.height // 2)] = (0, 0, 0, 0)
            else:
                for i in range(self.height * 3):
                    px_arr[randrange(0, self.width - 1),
                           randrange(self.height // 2, self.height - 1)] = (0, 0, 0, 0)
            self.dmg = True
        else:
            self.kill()

    def update(self):
        self.screen.blit(self.image, self.rect)
