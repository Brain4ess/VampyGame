import pygame as pg
from pygame.locals import *

from pygame.transform import scale, flip
from pygame.image import load


from dataclasses import dataclass, field

@dataclass
class BG:
    imageBG: str = field(default = '')
    screen: pg.Surface = field(default = None)
    speed: int = field(default = 0)
    
    def __post_init__(self):
        self.scrWidth = self.screen.get_width()
        self.scrHeight = self.screen.get_height()
        
        self.bg = scale(load(self.imageBG).convert(), (self.scrWidth, self.scrHeight))
        
        self.bgList = [self.bg for _ in range(4)]
        
        self.bgRectLeft = self.bgList[0].get_rect()
        self.bgRectRight = self.bgList[1].get_rect()
        self.bgRectUp = self.bgList[2].get_rect()
        self.bgRectDown = self.bgList[3].get_rect()
        self.bgrects = [self.bgRectLeft, self.bgRectRight, self.bgRectUp, self.bgRectDown]
        
    def eventKey(self):
        keys = pg.key.get_pressed()
        
        if keys[K_RIGHT]:
            self.scroll('right')
        elif keys[K_LEFT]:
            self.scroll('left')
        elif keys[K_UP]:
            self.scroll('up')
        elif keys[K_DOWN]:
            self.scroll('down')
            
    def scroll(self, direction):
        if direction == 'right':
            if self.bgRectLeft.x <= -self.scrWidth:
                self.bgRectLeft.x = 0
                self.bgrect
            
            for i in range(len(self.bgList)):
                self.bgList[i].scroll(-self.speed, 0)
                
        elif direction == 'left':
            if self.bgRectRight.x >= self.scrWidth:
                self.bgRectCenter.x = 0
            self.bgRectCenter.x += self.speed
        elif direction == 'up':
            if self.bgRectCenter.y <= -self.scrHeight:
                self.bgRectCenter.y = 0
            self.bgRectCenter.y -= self.speed
        elif direction == 'down':
            if self.bgRectCenter.y >= self.scrHeight:
                self.bgRectCenter.y = 0
            self.bgRectCenter.y += self.speed
        
        self.bgRectLeft.x = self.bgRectCenter.x - self.scrWidth
        self.bgRectRight.x = self.bgRectCenter.x + self.scrWidth
        self.bgRectUp.y = self.bgRectCenter.y - self.scrHeight
        self.bgRectDown.y = self.bgRectCenter.y + self.scrHeight
        
    def blitBG(self):
        for i in range(len(self.bgList)):
            self.screen.blit(self.bgList[i], self.bgrects[i])
        