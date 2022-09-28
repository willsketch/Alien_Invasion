import pygame
class Ship():
    """loading ship"""
    def __init__(self, ai_game):
        self.screen = ai_game.screen
        self.screen_rectangle= ai_game.screen.get_rect()
        #load image
        #self.image= pygame.image.load(r'C:\Users\willi\OneDrive\Bureaublad\battleship\images\ship.bmp')
        self.image= pygame.image.load('Alien_Invasion/data/images/new_rocket.png').convert_alpha()
        self.rect=self.image.get_rect()
        #screen rectangle is equal to image rectangle
        self.rect.midbottom= self.screen_rectangle.midbottom
        self.x_position= float(self.rect.x)
        # movement flags
        self.moving_right = False
        self.moving_left = False
        #ship settings
        self.settings= ai_game.settings


    def update_ship_position(self):
        if self.moving_right and self.rect.bottomright != self.screen_rectangle.bottomright:
            self.x_position+= self.settings.ship_speed
        if self.moving_left and self.rect.bottomleft != self.screen_rectangle.bottomleft:
            self.x_position -= self.settings.ship_speed
        self.rect.x =self.x_position



    def center_ship(self):
        """centers ship """
        self.rect.midbottom = self.screen_rectangle.midbottom
        self.x_position = float(self.rect.x)


    def drawship(self):
        self.screen.blit(self.image , self.rect)
