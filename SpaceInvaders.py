import pygame
from pygame.sprite import Group

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from bunker import Bunker
from ship import Ship
import game_functions as gf

def run_game():
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Space Invaders")
    clock = pygame.time.Clock()


    # Create an instance to store game statistics, and a scoreboard.
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)

    # Create entities
    ship = Ship(ai_settings, screen)
    bullets = Group()
    lasers = Group()
    aliens = Group()
    ufo = Group()
    gf.create_fleet(ai_settings, screen, ship, aliens)
    bunkers = gf.resetBunkers(ai_settings, screen)

    # Game Loop
    while True:
        clock.tick(ai_settings.tick_rate)
        if not stats.is_game_active:
            isQuit = not gf.start_screen(ai_settings, stats, screen)
            if isQuit:
                pygame.quit()
                break
            bunkers = gf.resetBunkers(ai_settings,screen)
            ship = Ship(ai_settings, screen)
            gf.start_new_game(ai_settings, screen, stats, sb, ship, aliens, lasers, bullets)

        gf.check_events(ai_settings, screen, stats, ship, bullets)
        if stats.is_game_active:
            if not ship.isDead:
                ship.update()
                gf.update_lasers_bullets(ai_settings, screen, stats, sb, ship, aliens, lasers=lasers, bullets=bullets, ufo=ufo)
                gf.update_aliens(ai_settings, screen, stats, sb, ship, aliens, lasers=lasers, bullets=bullets, ufos=ufo)
            else:
                screen.fill(ai_settings.bg_color)
                ship.update()
        gf.update_screen(ai_settings=ai_settings, screen=screen, stats=stats, sb=sb, ship=ship, aliens=aliens, lasers=lasers, bullets=bullets, bunkers=bunkers, ufos=ufo)


run_game()
