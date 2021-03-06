import sys
from time import sleep

import pygame

from bullet import Bullet
from alien import Alien

def check_keydown_events(event, main_settings, screen, stats, ship, bullets):
    """ Respond to keypress """
    if event.key == pygame.K_RIGHT:
        # Move the ship to the right.
        ship.moving_right = True
                
    elif event.key == pygame.K_LEFT:
        # Move the ship to the left
        ship.moving_left = True
    
    elif event.key == pygame.K_SPACE:
        if stats.game_active:
            # Create a new bullet and add it to the bullets group.
            fire_bullet(main_settings, screen, ship, bullets)
        else:
            stats.game_active = True
    
    elif event.key == pygame.K_q:
        # Exit game when press q
        sys.exit()

        
def fire_bullet(main_settings, screen, ship, bullets):
    """Fire a bullet if limit not reached yet."""
    # Create a new bullet and add it to the bullets group.
    if len(bullets) < main_settings.bullets_allowed:
        new_bullet = Bullet(main_settings, screen, ship)
        bullets.add(new_bullet)
        
    
def check_keyup_events(event, ship):
    """ Respont to key releases """
    if event.key  == pygame.K_RIGHT:
        ship.moving_right = False
                
    if event.key == pygame.K_LEFT:
        ship.moving_left = False 


def check_events(main_settings, screen, stats, sb, play_button, ship, aliens, bullets):
    """ Respond to keypess and mouse events """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, main_settings, screen, stats, ship, bullets)
            
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(main_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y)
    
            
def check_play_button(main_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    """Start a new game when the player clicks Play."""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        
        # Reset the games settings
        main_settings.initialize_dynamic_settings()
        # Hide the mouse cursor.
        pygame.mouse.set_visible(False)
        # Reset the game statistics.
        stats.reset_stats()
        stats.game_active = True
        
        # Resey the scoreboard images
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()
        
        # Empty the list of aliens and bullets.
        aliens.empty()
        bullets.empty()
        # Create a new fleet and center the ship.
        create_fleet(main_settings, screen, ship, aliens)
        ship.center_ship()


def ship_hit(main_settings, screen, stats, sb, ship, aliens, bullets):
    """Respond to ship being hit by alien."""
    if stats.ships_left > 0:
        # Decrement ships_left.
        stats.ships_left -= 1
        # Update scoreboard
        sb.prep_ships()
        # Empty the list of aliens and bullets.
        if stats.ships_left < 0:
            print("Game Over!!! :(")
        aliens.empty()
        bullets.empty()
        # Create a new fleet and center the ship.
        create_fleet(main_settings, screen, ship, aliens)
        ship.center_ship()
        # Pause.
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)
            
            
def update_screen(main_settings, screen, stats, sb, ship, aliens, bullets, play_button):
    """Update images on the screen and flip to the new screen."""
    screen.fill(main_settings.bg_color)
    # Redraw all bullets behind ship and aliens.
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)
    sb.show_score()
    # Draw the play button if the game is inactive.
    if not stats.game_active:
        play_button.draw_button()
    # Make the most recently drawn screen visible.
    pygame.display.flip()
    
    
def update_bullets(main_settings, screen, stats, sb, ship, aliens, bullets):
    """Update position of bullets and get rid of old bullets."""
    # Update bullets position
    bullets.update()         
    # Get rid of bullets that have disappeared
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_alien_collisions(main_settings, screen, stats, sb, ship, aliens, bullets)
        
        
def check_bullet_alien_collisions(main_settings, screen, stats, sb, ship, aliens, bullets):
    """Respond to bullet-alien collisions."""
    # Remove any bullets and aliens that have collided. 
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    # If all aliens have been destroyed, remove existing bullets and create new fleet.
    if len(aliens) == 0:
        # If the entire fleet is destroyed, start a new level.
        bullets.empty()
        main_settings.increase_speed()
        
        # Increase level
        stats.level += 1
        sb.prep_level()
        
        create_fleet(main_settings, screen, ship, aliens)
    
    if collisions:    
        for aliens in collisions.values():
            stats.score += main_settings.alien_points*len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)
   
            
def get_number_aliens_x(main_settings, alien_width):
    """Determine the number of aliens that fit in a row."""
    available_space_x = main_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def create_alien(main_settings, screen, aliens, alien_number, row_number):
    """Create an alien and place it in the row."""
    alien = Alien(main_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def create_fleet(main_settings, screen, ship, aliens):
    """Create a full fleet of aliens."""
    # Create an alien and find the number of aliens in a row.
    alien = Alien(main_settings, screen)
    number_aliens_x = get_number_aliens_x(main_settings, alien.rect.width)
    number_rows = get_number_rows(main_settings, ship.rect.height, alien.rect.height)
    
    # Create the fleet of aliens.
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(main_settings, screen, aliens, alien_number, row_number)
        
        
def get_number_rows(main_settings, ship_height, alien_height):
    """Determine the number of rows of aliens that fit on the screen."""
    available_space_y = (main_settings.screen_height -  (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height)) 
    return number_rows


def update_aliens(main_settings, screen, stats, sb, ship, aliens, bullets):
    """ Check if the fleet is at an edge, and then update the postions of all aliens in the fleet. """
    check_fleet_edges(main_settings, aliens)
    aliens.update()
    # Look for alien-ship collisions.
    if pygame.sprite.spritecollideany(ship, aliens):
        print("Mayday, Mayday!!!")
        ship_hit(main_settings, screen, stats, sb, ship, aliens, bullets)
    # Look for aliens hitting the bottom of the screen.
    check_aliens_bottom(main_settings, screen, stats, sb, ship, aliens, bullets)
    

def check_fleet_edges(main_settings, aliens):
    """Respond appropriately if any aliens have reached an edge."""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(main_settings, aliens)
            break


def change_fleet_direction(main_settings, aliens):
    """Drop the entire fleet and change the fleet's direction."""
    for alien in aliens.sprites():
        alien.rect.y += main_settings.fleet_drop_speed
    main_settings.fleet_direction *= -1
        
        
def check_aliens_bottom(main_settings, screen, stats, sb, ship, aliens, bullets):
    """Check if any aliens have reached the bottom of the screen."""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Treat this the same as if the ship got hit.
            ship_hit(main_settings, screen, stats, sb, ship, aliens, bullets)
            break
        

def check_high_score(stats, sb):
    """Check to see if there's a new high score."""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()
    