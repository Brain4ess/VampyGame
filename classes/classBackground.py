import pygame as pg
from pygame.locals import *
from pygame.transform import scale, flip
from pygame.image import load
from classes.classCamera import Camera

class BG: 
    def __init__(self, imageBG: str, screen: pg.Surface, speed: int = 0, spawnpoint: pg.math.Vector2 = pg.math.Vector2(0,0)):
        self.imageBG = imageBG
        self.screen = screen
        self.speed = speed
        self.spawnpoint = (spawnpoint[0] - self.screen.get_width() / 2, spawnpoint[1] - self.screen.get_height() / 2)
        self.__post_init__()
    
    def __post_init__(self):
        self.bg = load(self.imageBG).convert()
        self.width = self.bg.get_width()
        self.height = self.bg.get_height()
        
    
    def blitBG(self, offset: pg.math.Vector2):
        self.screen.blit(self.bg, self.bg.get_rect().topleft - (offset + self.spawnpoint))
        self.topleftpos = self.bg.get_rect().topleft - (offset + self.spawnpoint)
        