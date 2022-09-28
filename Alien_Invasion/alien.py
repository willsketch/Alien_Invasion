import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """contains the alien object"""
    def __init__(self, ai_game):
        """ intialize alien and set its starting position"""
        super().__init__()
        self.screen= ai_game.screen
        self.image= pygame.image.load("Alien_Invasion/data/images/alien.bmp")
        self.rect = self.image.get_rect()
        self.settings = ai_game.settings

        # initialize the position of the alien on screen
        self.rect.x= self.rect.width
        self.rect.y = self.rect.height
        self.x= float(self.rect.x) # store exact location of alien
        self.y= float(self.rect.y)

    def update(self):
        self.x += (self.settings.alien_speed*self.settings.fleet_direction)
        self.rect.x= self.x

    def check_edges(self):
        """ returns true if the alien is at the edge"""
        screen_rect= self.screen.get_rect()
        if screen_rect.right <= self.rect.right or self.rect.left <= 0:
            return True
