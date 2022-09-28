from ast import Pass
import sys
import pygame
from pygame.constants import QUIT
from settings import Settings
from ship import Ship
from bullets import Bullet
from alien import Alien
from time import sleep
from game_stats import Game_stats

class AlienInvasion():
    """overall class to manage game assets and behaviors"""
    def __init__(self):
        pygame.init()
        self.settings= Settings()
        self.screen= pygame.display.set_mode(self.settings.dimensions)
        pygame.display.set_caption('Alien Invasion')
        # initailize game_stats
        self.stats = Game_stats(self)
        self.ship=Ship(self)
        self.bullets_group= pygame.sprite.Group()
        self.bullet_sound= pygame.mixer.Sound("Alien_Invasion/data/sounds/bullet_sound.wav")
        self.background= pygame.image.load("Alien_Invasion/data/images/background_image.jpg")
        self.alien_fleet= pygame.sprite.Group()
        self._create_fleet()

    def run_game(self):
        """start game"""
        #print(self.ship.position)
        while True:
            # watch for keyboard movements
            self._check_events()
            if self.stats.game_active == True:
                self.ship.update_ship_position()
                self._update_bullet()
                self._update_alien()
                self._update_screen()



    def _check_events(self):
        """checking for events"""
        for event in pygame.event.get():
            if event.type== pygame.KEYDOWN:
                self._check_Keydown_events(event)
            elif event.type== pygame.KEYUP:
                self._check_KeyUp_events(event)

    def _check_Keydown_events(self, event):
        if event.key == pygame.K_q:
            sys.exit()
        elif event.key== pygame.K_RIGHT:
            self.ship.moving_right= True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left= True
        elif event.key == pygame.K_SPACE:
            self.fire_bullet()


    def _check_KeyUp_events(self, event):
        if event.key== pygame.K_RIGHT:
            self.ship.moving_right= False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left= False

    def _update_screen(self):
        """updates screen after every run"""
         # redraw the screen to fill in a different color
        self.screen.fill(self.settings.screen_color)
        #self.screen.blit(self.background,(0,0))
        self.ship.drawship()
        for bullet in self.bullets_group.sprites():
            bullet.draw_bullet()

        self.alien_fleet.draw(self.screen)
        #make most recent screen visible
        pygame.display.flip()

    def fire_bullet(self):
        """ fires a bullet from the ship with sound"""
        self.bullet_sound.play()
        new_bullet= Bullet(self)
        self.bullets_group.add(new_bullet)

    def _update_bullet(self):
        self.bullets_group.update()
        # deleting bullets
        for bullet  in self.bullets_group.copy():
            if bullet.rect.bottom <= 0:
                self.bullets_group.remove(bullet)

        self._check_collisions()
        #if pygame.sprite.spritecollideany(self.ship, self.alien_fleet):
         #   print('ship hit')


    def _check_collisions(self):
        collisions = pygame.sprite.groupcollide(self.bullets_group, self.alien_fleet, False, True)

        # check if aliens list is empty
        if len(self.alien_fleet) == 0:
            self.bullets_group.empty()
            self._create_fleet()



    def _create_fleet(self):
        alien= Alien(self)
        alien_width= alien.rect.width
        alien_height = alien.rect.height
        available_space_x= self.settings.screen_width - 2*alien_width
        number_of_aliens_x= (available_space_x//(alien_width )) -2
        available_space_y= self.settings.screen_height//2
        number_of_aliens_rows= (available_space_y//alien_height)-5

        for row in range(number_of_aliens_rows):
            for alien_number  in range(number_of_aliens_x):
                self._create_alien(alien_number, row)

    def _create_alien(self, alien_number, alien_row):
        """create alien """
        alien= Alien(self)
        alien_width= alien.rect.width
        alien_height = alien.rect.height
        alien.x = alien_width + (2*alien_width*alien_number)
        alien.y= alien_height + (alien_height* alien_row)
        alien.rect.x= alien.x
        alien.rect.y= alien.y
        self.alien_fleet.add(alien)

    def _check_fleet_edges(self):
        """ drop and change fleet direction if fleet has reached the edge"""
        for alien in self.alien_fleet.sprites():
            if alien.check_edges():
                self._change_fleet_direction()

    def _change_fleet_direction(self):
            """ changes alien fleet direction if at edge"""
            for alien in self.alien_fleet.sprites():
                alien.rect.y += self.settings.fleet_drop_speed

            self.settings.fleet_direction *= -1

    def _update_alien(self):
        """update the postion of aliens  and also check if fleet is at edge"""
        self._check_fleet_edges()
        self.alien_fleet.update()
        if pygame.sprite.spritecollideany(self.ship, self.alien_fleet):
            self._ship_hit()
        self._check_bottom_screen_aliens()

    def _ship_hit(self):
        """responds to ship being hit"""
        if self.settings.ship_limit > 0:

            self.stats.ships_left -= 1
            print(self.stats.ships_left)
            self.alien_fleet.empty()
            self.bullets_group.empty()
        # create new fleet
            self._create_fleet()
            self.ship.center_ship()
        # pause game
            sleep(1)
        else:
            self.stats.game_active = False



    def _check_bottom_screen_aliens(self):
        """ checks if aliens have hit the bottom of the screen"""
        screen_rect = self.screen.get_rect()
        for alien in self.alien_fleet.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break

if __name__ == '__main__':
    game= AlienInvasion()
    game.run_game()
