import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """ contains all attributes and everything to do with game bullets"""
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color= self.settings.bullet_color

        
        #creating  a bullet 
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop
        # creating a y position to adjust speed later
        self.y_position = float(self.rect.y)

    def update(self):
        """move bullets up the screen"""
        self.y_position -= self.settings.bullet_speed
        self.rect.y= self.y_position
    

    def draw_bullet(self):
        """" draws bullet"""
        pygame.draw.rect(self.screen, self.settings.bullet_color, self.rect)


