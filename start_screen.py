from pygame import sysfont, display, time, image


class EnemyDisplay:
    def __init__(self, ai_settings, screen, y_start):
        self.screen = screen
        self.settings = ai_settings
        self.aliens = []

        images = [
            image.load(ai_settings.alien_classic1),
            image.load(ai_settings.alien_ghost1),
            image.load(ai_settings.alien_creep1),
            image.load(ai_settings.ufo_image)
        ]
        for img in images:
            self.aliens.append((img, img.get_rect()))
        self.example_scores = [
            TextLabel(ai_settings.bg_color,
                      self.screen,
                      ' = ' + str(ai_settings.alien_points['classic']) + 'PTS',
                      text_color=ai_settings.text_color),
            TextLabel(ai_settings.bg_color, self.screen,
                      ' = ' + str(ai_settings.alien_points['ghost']) + 'PTS',
                      text_color=ai_settings.text_color),
            TextLabel(ai_settings.bg_color, self.screen,
                      ' = ' + str(ai_settings.alien_points['creeper']) + 'PTS',
                      text_color=ai_settings.text_color),
            TextLabel(ai_settings.bg_color, self.screen, ' = ???' + 'PTS',
                      text_color=ai_settings.text_color)
        ]
        self.score_images = []
        self.y_start = y_start
        self.prep_images()

    def prep_images(self):
        y_offset = self.y_start
        for a, es in zip(self.aliens, self.example_scores):
            a[1].centery = y_offset
            a[1].centerx = (self.settings.screen_width // 2) - a[1].width
            es.prep_image()
            es.image_rect.centery = y_offset
            es.image_rect.centerx = (self.settings.screen_width // 2) + a[1].width
            y_offset += int(a[1].height * 1.5)

    def show_examples(self):
        for a in self.aliens:
            self.screen.blit(a[0], a[1])
        for es in self.example_scores:
            es.blitme()


class Title:
    def __init__(self, bg_color, screen, text, text_size=56, text_color=(0, 255, 0)):
        self.bg_color = bg_color
        self.screen = screen
        self.text = text
        self.text_color = text_color
        self.font = sysfont.SysFont(None, text_size)
        self.image = None
        self.image_rect = None

    def prep_image(self):
        self.image = self.font.render(self.text, True, self.text_color, self.bg_color)
        self.image_rect = self.image.get_rect()

    def blitme(self):
        self.screen.blit(self.image, self.image_rect)


class TextLabel:
    def __init__(self, bg_color, screen, text, text_size=48, text_color=(0, 255, 0)):
        self.bg_color = bg_color
        self.screen = screen
        self.text = text
        self.text_color = text_color
        self.font = sysfont.SysFont(None, text_size)
        self.image = None
        self.image_rect = None

    def prep_image(self):
        self.image = self.font.render(self.text, True, self.text_color, self.bg_color)
        self.image_rect = self.image.get_rect()

    def blitme(self):
        self.screen.blit(self.image, self.image_rect)


class Intro:
    def __init__(self, settings, game_stats, screen):
        # settings, settings, stats
        self.settings = settings
        self.game_stats = game_stats
        self.screen = screen

        # text/image information
        self.title = Title(settings.bg_color, self.screen, 'SPACE', text_size=72)
        self.subtitle = TextLabel(settings.bg_color, self.screen, 'INVADERS', text_size=62)
        self.enemy_display = EnemyDisplay(settings, self.screen, self.settings.screen_height // 3)
        self.prep_image()

    def prep_image(self):
        self.title.prep_image()
        self.title.image_rect.centerx = (self.settings.screen_width // 2)
        self.title.image_rect.centery = (self.settings.screen_height // 5) - self.title.image_rect.height
        self.subtitle.prep_image()
        self.subtitle.image_rect.centerx = (self.settings.screen_width // 2)
        self.subtitle.image_rect.centery = (self.settings.screen_height // 5) + (self.title.image_rect.height // 3)

    def show_menu(self):
        self.title.blitme()
        self.subtitle.blitme()
        self.enemy_display.show_examples()


def level_intro(ai_settings, screen, stats):
    if stats.is_game_active:
        level_text = Title(ai_settings.bg_color, screen, 'Level: ' + str(stats.level))
        level_text.prep_image()
        level_text.image_rect.centerx = (ai_settings.screen_width // 2)
        level_text.image_rect.centery = (ai_settings.screen_height // 2) - level_text.image_rect.height
        start_time = time.get_ticks()
        while abs(start_time - time.get_ticks()) <= 1500:
            screen.fill(ai_settings.bg_color)
            level_text.blitme()
            display.flip()
