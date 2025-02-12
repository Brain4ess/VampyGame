import pygame as pg
from pygame.locals import *
from pygame.sprite import Sprite
from pygame.image import load
from pygame.transform import scale, flip

class Character(Sprite):
    def __init__(self, bg, screen: pg.Surface = None, speed: int = 0):
        super().__init__()
        self.screen = screen
        self.speed = speed
        self.curspeed = self.speed 
        self.size = (64, 64)
        self.side = 'right'
        self.bg = bg
        self.__post_init__()
    
    
    def __post_init__(self):
        self.scrWidth = self.screen.get_width()
        self.scrHeight = self.screen.get_height()
        
        self.sprHeroLeft: list[pg.Surface] = list()
        self.sprHeroRight: list[pg.Surface] = list()
        self.sgroup = pg.sprite.Group()
        
        self.heroCreate()
        self.rect = self.sprHeroRight[0].get_rect(center = (self.scrWidth / 2, self.scrHeight / 2))
        self.oldY = self.rect.y
    
    
    def heroCreate(self):
        self.sprHeroRight.append(scale(load('assets/images/placeholders/character/characterplaceholder.png'), self.size))
        self.sprHeroLeft.append(flip(self.sprHeroRight[0], True, False))
    
    
    def eventKey(self, event = None):
        keys = pg.key.get_pressed()
        if keys[K_d] and keys[K_s] or keys[K_a] and keys[K_s] or keys[K_d] and keys[K_w] or keys[K_a] and keys[K_w]:
            self.curspeed = self.speed / 1.4
        else:
            self.curspeed = self.speed
        if keys[K_d]:
            self.side = 'right'
            self.rect.x += self.curspeed
        if keys[K_a]:
            self.side = 'left'
            self.rect.x -= self.curspeed
        if keys[K_w]:
            self.rect.y -= self.curspeed
        if keys[K_s]:
            self.rect.y += self.curspeed
    
    
    def direction(self, offset: pg.math.Vector2 = (0, 0)):
        offset_pos = self.rect.topleft - offset
        if self.side == 'right':
            self.screen.blit(self.sprHeroRight[0], offset_pos)
        if self.side == 'left':
            self.screen.blit(self.sprHeroLeft[0], offset_pos)
    
    
    def update(self, offset: pg.math.Vector2 = (0, 0)):
        # When the player reaches the threshold value we stop moving in the direction the player has reached the end of a background
        self.rect.x = max(-self.bg.spawnpoint[0], min(self.bg.width - self.size[0] - self.bg.spawnpoint[0], self.rect.centerx - (self.size[0] / 2)))
        self.rect.y = max(-self.bg.spawnpoint[1], min(self.bg.height - self.size[1] - self.bg.spawnpoint[1], self.rect.centery - (self.size[1] / 2)))
        
        self.eventKey()
        self.direction(offset)
        # print(self.rect.center) # DEBUG
