from pygame import sprite, Surface, PixelArray
from random import randrange


class Bunker(sprite.Sprite):
    def __init__(self, ai_settings, screen, row, col):
        super().__init__()
        self.screen = screen
        self.height = ai_settings.bunker_size_h
        self.width = ai_settings.bunker_size_w
        self.color = ai_settings.bunker_color
        self.destroy_f = ai_settings.destruction_factor
        self.image = Surface((self.width, self.height))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.row = row
        self.col = col
        self.dmg = False

    def damage(self, top):
        if not self.dmg:
            arr = PixelArray(self.image)
            self.set_damage(arr, top)
            self.dmg = True
        else:
            self.kill()

    def set_damage(self, pixel_arr, top=False):
        x_range_low = 0
        x_range_high = self.width-1
        if top:
            y_range_low = 0
            y_range_high = int(self.height/2)
        else:
            y_range_low = int(self.height / 2)
            y_range_high = self.height - 1

        for i in range(self.height * self.destroy_f):
            pixel_arr[randrange(x_range_low, x_range_high),
                   randrange(y_range_low, y_range_high)] = (0, 0, 0, 0)

    def update(self):
        self.screen.blit(self.image, self.rect)
