import pygame as pg
import configparser as cfgp
from pygame.locals import *
from UI.classGameScreen import GameScreen
from classes.classBackground import BG
from classes.classCharacter import Character

class Game:
    def __init__(self):
        cfg = './data/config.ini'
        config = cfgp.ConfigParser()
        config.read(cfg)
        try:
            self.screen = pg.display.set_mode((config.getint('Game', 'width'), config.getint('Game', 'height')))
            self.fps = config.getint('Game', 'fps')
        except Exception as exception:
            print(f"Error: {exception}. Using default")
            self.fps = 60
            self.screen = pg.display.set_mode(GameScreen.size)
        self.run = True
        self.clock = pg.time.Clock()
        self.player = Character(self.screen, 5)
        
        
    def eventGame(self):
        for event in pg.event.get():
            if event.type == QUIT:
                self.run = False
                
    def runGame(self):
        while self.run:
            
            self.eventGame()
            
            #self.player.update()
            pg.display.update()
            self.clock.tick(self.fps)