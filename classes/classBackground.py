import pygame as pg
from pygame.locals import *

from pygame.transform import scale, flip
from pygame.image import load

from dataclasses import dataclass, field

@dataclass
class BG:
    imageBG: str = field(default = '')
    screen: object = field(default = None)
    speed: int = field(default = 0)
    
    def __post_init__(self):
        self.scrWidth = self.screen.get_width()
        self.scrHeight = self.screen.get_height()
        
        self.bg = scale(load(self.imageBG).convert(), (self.scrWidth, self.scrHeight))
        
        self.bgList = [self.bg for _ in range(3)]
        
        self.bgRectLeft = self.bgList[0].get_rect()
        self.bgRectCenter = self.bgList[1].get_rect()
        self.bgRectRight = self.bgList[2].get_rect()
        
    def eventKey(self):
        keys = pg.key.get_pressed()
        
        if keys[K_RIGHT]:
            self.scroll('right')
        elif keys[K_LEFT]:
            self.scroll('left')
            
    def scroll(self, direction):
        if direction == 'right':
            if self.bgRectCenter.x <= -self.scrWidth:
                self.bgRectCenter.x = 0
            self.bgRectCenter.x -= self.speed
        elif direction == 'left':
            if self.bgRectCenter.x >= self.scrWidth:
                self.bgRectCenter.x = 0
            self.bgRectCenter.x += self.speed
        
        self.bgRectLeft.x = self.bgRectCenter.x - self.scrWidth
        self.bgRectRight.x = self.bgRectCenter.x + self.scrWidth
        
    def blitBG(self):
        self.screen.blit(self.bgList[0], self.bgRectLeft)
        self.screen.blit(self.bgList[1], self.bgRectCenter)
        self.screen.blit(self.bgList[2], self.bgRectRight)
        