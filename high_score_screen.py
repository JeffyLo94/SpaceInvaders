from start_screen import Title

class HighScoreScreen:
    def __init__(self, ai_settings, screen, game_stats):
        self.score_text = []
        self.score_text.append(Title(ai_settings.bg_color, screen, 'High Scores'))
        for counter, obj in enumerate(game_stats.high_scores_list, 1):
            self.score_text.append(Title(ai_settings.bg_color, screen, str(counter) + '.   ' + str(obj['score']) + '    ' + str(obj['name']),
                                         text_color=ai_settings.alt_text_color))

        OFFSSET_FACTOR = 0.06
        y_offset = ai_settings.screen_height * 0.10
        for text in self.score_text:
            text.prep_image()
            text.image_rect.centerx = ai_settings.screen_width // 2
            text.image_rect.centery = y_offset
            y_offset += ai_settings.screen_height * OFFSSET_FACTOR

    def show_scores(self):
        for text in self.score_text:
            text.blitme()