import pygame as pg
from pygame.locals import *
from pygame.sprite import Sprite
from pygame.image import load

class Character(Sprite):
    
    def __init__(self, screen: pg.Surface = None, speed: int = 0):
        super().__init__()
        self.screen = screen
        self.speed = speed
        self.flRight = False
        self.flLeft = False
        self.flJump = False
        self.side = 'right'
        self.__post_init__()

    def __post_init__(self):
        self.scrWidth = self.screen.get_width()
        self.scrHeight = self.screen.get_height()
        
        self.sprHeroLeft = list()
        self.sprHeroRight = list()
        self.sprHeroJumpLeft = list()
        self.sprHeroJumpRight = list()
        
        self.heroCreate()
        self.rect = self.sprHeroRight[0].get_rect(center = (self.scrWidth / 2, self.scrHeight / 2))
        self.oldY = self.rect.y
        
    def heroCreate(self):
        self.sprHeroRight.append(load('assets/images/placeholders/character/characterplaceholder.png'))
    
    def eventKey(self, event = None):
        keys = pg.key.get_pressed()
        
        if keys[K_RIGHT]:
            self.flRight = True
            self.flLeft = False
            self.side = 'right'
        elif keys[K_LEFT]:
            self.flRight = False
            self.flLeft = True
            self.side = 'left'
        else:
            if not self.flJump:
                self.flRight = False
                self.flLeft = False
                self.animation = 0
                
    def direction(self):
        if self.side == 'right' and self.animation == 0:
            self.screen.blit(self.sprHeroRight[0], self.rect)
        elif self.side == 'left' and self.animation == 0:
            self.screen.blit(self.sprHeroLeft[0], self.rect)
    
    def update(self):
        self.eventKey()
        self.direction()
    