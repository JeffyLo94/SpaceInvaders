import sys

import pygame
import random

from bullet import Bullet
from laser import Laser
from alien import Alien, Ufo
from start_screen import level_intro, Intro
from button import Button
from high_score_screen import HighScoreScreen


def check_keydown_events(event, ai_settings, screen, ship, bullets):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()


def check_keyup_events(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_events(ai_settings, screen, stats, ship, bullets):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            stats.save_scores(ai_settings.player_name)
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)


def start_new_game(ai_settings, screen, stats, sb,
                   ship, aliens, beams, bullets):
    # Hide the mouse
    pygame.mouse.set_visible(False)
    # Reset settings
    ai_settings.initialize_dynamic_settings()
    # Reset game stats
    stats.reset_stats()
    stats.is_game_active = True
    # Reset scoreboard images
    sb.prep_score()
    sb.prep_high_score()
    sb.prep_level()
    sb.prep_ships()
    # Clear Entities
    aliens.empty()
    bullets.empty()
    beams.empty()
    # New fleet
    create_fleet(ai_settings, screen, ship, aliens)
    stats.next_speedup = len(aliens) - (len(aliens) // 5)
    stats.aliens_left = len(aliens)
    ship.center_ship()

# def check_play_button(ai_settings, screen, stats, sb, play_button, ship,
#                       aliens, bullets, mouse_x, mouse_y):
#     button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
#     if button_clicked and not stats.is_game_active:
#         # Reset the game settings.
#         ai_settings.initialize_dynamic_settings()
#
#         pygame.mouse.set_visible(False)
#
#         # Reset the game statistics.
#         stats.reset_stats()
#         stats.is_game_active = True
#
#         # Reset the scoreboard images.
#         sb.prep_score()
#         sb.prep_high_score()
#         sb.prep_level()
#         sb.prep_ships()
#
#         # Empty the list of aliens and bullets.
#         aliens.empty()
#         bullets.empty()
#
#         # Create a new fleet and center the ship.
#         create_fleet(ai_settings, screen, ship, aliens)
#         ship.center_ship()


def fire_bullet(ai_settings, screen, ship, bullets):
    # Create a new bullet, add to bullets group.
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def fire_laser(ai_settings, screen, aliens, lasers):
    shooting_alien = random.choice(aliens.sprites())
    if len(lasers) < ai_settings.lasers_allowed and \
            (ai_settings.laser_stamp is None or
             (abs(pygame.time.get_ticks() - ai_settings.laser_stamp) > ai_settings.laser_time)):
        laser = Laser(ai_settings, screen, shooting_alien)
        lasers.add(laser)


def update_screen(ai_settings, screen, stats, sb, ship, aliens, lasers, bullets, bunkers, ufos):
    # Redraw the screen, each pass through the loop.
    screen.fill(ai_settings.bg_color)
    if stats.is_game_active:
        ufo_event_check(ai_settings, screen, ufos)

    # Redraw all bullets, behind ship and aliens.
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    for laser in lasers.sprites():
        laser.draw_laser()

    if ufos:
        ufos.update()
        for u in ufos.sprites():
            u.blitme()
    ship.blitme()
    aliens.draw(screen)
    check_bunker_collision(bullets, lasers, bunkers)
    bunkers.update()
    # Draw the score information.
    sb.show_score()

    # Make the most recently drawn screen visible.
    pygame.display.flip()


def ufo_event_check(ai_settings, screen, ufos):
    if ( (not ai_settings.last_ufo) or (abs(ai_settings.last_ufo - pygame.time.get_ticks()) > ai_settings.ufo_spawn_time) ) and not ufos:
        ai_settings.last_ufo, some_ufo = create_random_ufo(ai_settings, screen)
        if some_ufo:
            ufos.add(some_ufo)


def create_random_ufo(ai_settings, screen):
    ufo = None
    if random.randrange(0, 100) <= 15:
        ufo = Ufo(ai_settings, screen)
    time = pygame.time.get_ticks()
    return (time, ufo)


def update_lasers_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets, lasers, ufo):
    lasers.update()
    bullets.update()

    # Get rid of bullets that have disappeared.
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    for laser in lasers.copy():
        if laser.rect.bottom > ai_settings.screen_height:
            lasers.remove(laser)
    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship,
                                  aliens, lasers, bullets, ufo)
    check_laser_ship_collisions(ai_settings, screen, stats, sb, ship,
                                  aliens, lasers, bullets, ufo)


def check_high_score(stats, sb):
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()


def alien_bullet_collision(bullet, alien):
    if alien.isDead:
        return False
    return pygame.sprite.collide_rect(bullet, alien)


def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, lasers, bullets, ufo):
    # Remove any bullets and aliens that have collided.
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, False, collided= alien_bullet_collision)

    if collisions:
        for aliens in collisions.values():
            for i in aliens:
                stats.score += ai_settings.alien_points[str(i.alienType)]
                i.flag_for_death()
            sb.prep_score()
        check_high_score(stats, sb)
    ufo_collide = pygame.sprite.groupcollide(bullets, ufo, True, False, collided=alien_bullet_collision)
    if ufo_collide:
        for ufo in ufo_collide.values():
            for i in ufo:
                stats.score += i.score
                i.flag_for_death()
            sb.prep_score()
        check_high_score(stats, sb)
    if len(aliens) == 0:
        # CLEAN UP BOARD
        if ufo:
            for i in ufo.sprites():
                i.kill()
        bullets.empty()
        lasers.empty()

        level_intro(ai_settings, screen, stats)
        ai_settings.increase_alien_base_speed()
        ai_settings.reset_alien_speed()

        # Increase level.
        stats.level += 1
        sb.prep_level()

        create_fleet(ai_settings, screen, ship, aliens)
        stats.next_speedup = len(aliens) - (len(aliens) // 5)
    stats.aliens_left = len(aliens)
    if stats.aliens_left <= stats.next_speedup and ai_settings.alien_speed_factor < ai_settings.alien_speed_limit:
        stats.next_speedup = stats.aliens_left - (stats.next_speedup//5)


def check_bunker_collision(bullets, lasers, bunker):
    # if lasers:
    #     return
    laserCollide = pygame.sprite.groupcollide(lasers, bunker, True, False)
    # laserCollide = pygame.sprite.spritecollide(lasers,bunker, True)
    for l in laserCollide.values():
        for blockpart in l:
            blockpart.damage(top=True)
    bulletCollide = pygame.sprite.groupcollide(bullets, bunker, True, False )
    for l in bulletCollide.values():
        for blockpart in l:
            blockpart.damage(top=False)



def check_laser_ship_collisions(ai_settings, screen, stats, sb, ship, aliens, lasers, bullets, ufo):
    if pygame.sprite.spritecollideany(ship, lasers):
        ship_hit(ai_settings,screen, stats, sb, ship, aliens, bullets, lasers, ufo)


def check_fleet_edges(ai_settings, aliens):
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets, lasers, ufos):
    if ufos:
        for ufo in ufos.sprites():
            ufo.kill()
    ship.trigger_death()
    ship.update()


    if stats.ships_left > 0:
        # Decrement ships_left.
        stats.ships_left -= 1

        aliens.empty()
        lasers.empty()
        bullets.empty()

        # Create a new fleet, and center the ship.
        ai_settings.reset_alien_speed()
        create_fleet(ai_settings, screen, ship, aliens)
        stats.next_speedup = len(aliens) - (len(aliens) // 5)
        stats.aliens_left = len(aliens.sprites())
        ship.center_ship()

        # Update scoreboard.
        sb.prep_ships()

    else:
        stats.is_game_active = False
        pygame.mouse.set_visible(True)
        stats.save_scores(ai_settings.player_name)


def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets, lasers, ufos):
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Treat this the same as if the ship got hit.
            ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets, lasers, ufos)
            break


def update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets, lasers, ufos):
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # Look for alien-ship collisions.
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets, lasers, ufos)

    # Look for aliens hitting the bottom of the screen.
    check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets, lasers, ufos)
    if aliens.sprites():
        fire_laser(ai_settings, screen, aliens, lasers)


def get_number_aliens_x(ai_settings, alien_width):
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def get_number_rows(ai_settings, ship_height, alien_height):
    # available_space_y = (ai_settings.screen_height -
    #                      (4 * alien_height) - ship_height)
    # print('avail space y:' + str(available_space_y))
    # print('alien_height' + str(alien_height))
    #
    # number_rows = int(available_space_y / ( alien_height))
    number_rows = ai_settings.num_alien_rows
    return number_rows


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    if row_number < 1:
        alien_type = 'creeper'
    elif row_number < 3:
        alien_type = 'ghost'
    else:
        alien_type = 'classic'
    alien = Alien(ai_settings, screen, alien_type)
    alien_width = alien.rect.width
    alien.x = alien_width + 1.25 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 1 * alien.rect.height * row_number
    alien.rect.y += int(ai_settings.screen_height/8)
    aliens.add(alien)


def create_fleet(ai_settings, screen, ship, aliens):
    # Create an alien, and find number of aliens in a row.
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height,
                                  alien.rect.height)

    # Create the fleet of aliens.
    # print('rows: ' + str(number_rows))
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number,
                         row_number)


def display_high_score_screen(ai_settings, game_stats, screen):
    highScores = HighScoreScreen(ai_settings, screen, game_stats)
    back_button = Button(ai_settings, screen, 'Back To Menu', 0.85)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.check_button(*pygame.mouse.get_pos()):
                    return True
        screen.fill(ai_settings.bg_color)
        highScores.show_scores()
        back_button.draw_button()
        pygame.display.flip()


def start_screen(ai_settings, game_stats, screen):
    menu = Intro(ai_settings, game_stats, screen)
    play_button = Button(ai_settings, screen, 'Play Game', 0.80)
    hs_button = Button(ai_settings, screen, 'High Scores', 0.90)
    showStart = True

    while showStart:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                click_x, click_y = pygame.mouse.get_pos()
                game_stats.is_game_active = play_button.check_button(click_x, click_y)
                # print("game active: " + str(game_stats.is_game_active))
                showStart = not game_stats.is_game_active
                if hs_button.check_button(click_x, click_y):
                    ret_hs = display_high_score_screen(ai_settings, game_stats, screen)
                    if not ret_hs:
                        return False
        screen.fill(ai_settings.bg_color)
        menu.show_menu()
        hs_button.draw_button()
        play_button.draw_button()
        pygame.display.flip()
    return True
