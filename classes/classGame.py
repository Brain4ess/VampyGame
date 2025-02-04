import pygame as pg
from pygame.locals import *
from UI.classGameScreen import GameScreen
from classes.classBackground import BG

class Game:
    def __init__(self):
        self.run = True
        self.fps = 60
        self.clock = pg.time.Clock()
        self.screen = pg.display.set_mode(GameScreen.size)
        self.bg = BG(screen=self.screen, imageBG="assets/images/placeholders/maps/GitMap_cross.png", speed=4)
        self.bg.blitBG()
        
    def eventGame(self):
        for event in pg.event.get():
            if event.type == QUIT:
                self.run = False
                
    def runGame(self):
        while self.run:
            
            self.eventGame()
            
            
            pg.display.update()
            self.clock.tick(self.fps)