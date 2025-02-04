import pygame as pg
from pygame.locals import *
from UI.classGameScreen import GameScreen
from classes.classBackground import Background

class Game:
    def __init__(self):
        self.run = True
        self.fps = 60
        self.clock = pg.time.Clock()
        pg.display.set_mode(GameScreen.size)
        self.bg = Background(screen=GameScreen.size, image="assets/images/placeholders/maps/GitMap_cross.png", x=1024, y=1024)
        
    def eventGame(self):
        for event in pg.event.get():
            if event.type == QUIT:
                self.run = False
                
    def runGame(self):
        while self.run:
            
            self.eventGame()
            self.bg.draw()
            
            pg.display.update()
            self.clock.tick(self.fps)