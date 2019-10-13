import pygame.font


class Button:

    def __init__(self, ai_settings, screen, msg, ypos_percent=0.55):
        # init class attributes to none - getting rid of pycharm issues
        self.ai_settings = ai_settings
        self.msg_image = None
        self.msg_image_rect = None

        self.screen = screen
        self.screen_rect = screen.get_rect()
        # self.ai_settings = ai_settings

        # Set the dimensions and properties of the button.
        # self.width, self.height = 200, 50
        # self.button_color = (0, 255, 0)
        # self.text_color = (255, 255, 255)
        # self.font = pygame.font.SysFont(None, 48)
        self.width, self.height = ai_settings.btn_w, ai_settings.btn_h
        self.button_color = ai_settings.btn_color
        self.text_color = ai_settings.text_color
        self.font = pygame.font.SysFont(None, ai_settings.font_size)
        self.ypos_percentage = ypos_percent


        # Build the button's rect object, and center it.
        # self.rect = pygame.Rect(0, 0, self.width, self.height)
        # self.rect.center = self.screen_rect.center

        # The button message only needs to be prepped once.
        self.prep_msg(msg)

    def prep_msg(self, msg):
        self.msg_image = self.font.render(msg, True, self.text_color,
                                          self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.centerx = self.ai_settings.screen_width // 2
        self.msg_image_rect.centery = int(self.ai_settings.screen_height * self.ypos_percentage)

    def check_button(self, mouse_x, mouse_y):
        return self.msg_image_rect.collidepoint(mouse_x, mouse_y)


    def draw_button(self):
        # Draw blank button, then draw message.
        self.screen.blit(self.msg_image, self.msg_image_rect)
