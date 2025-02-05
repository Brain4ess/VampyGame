import pygame as pg
import configparser as cfgp
from pygame.locals import *
from UI.classGameScreen import GameScreen
from classes.classBackground import BG
from classes.classCharacter import Character
from pygame.transform import scale, flip
from pygame.image import load

class Game:
    def __init__(self):
        self.imageBG = 'assets/images/placeholders/maps/BigMapPlaceholder.png'
        self.cfg = 'data/config.ini'
        config = cfgp.ConfigParser()
        config.read(self.cfg)
        try:
            self.screen = pg.display.set_mode((config.getint('Settings', 'Width'), config.getint('Settings', 'Height')))
            self.fps = config.getint('Settings', 'fps')
        except Exception as exception:
            print(f"Error: {exception}. Using default")
            self.fps = 60
            self.screen = pg.display.set_mode(GameScreen.size)
            
        self.bg = load(self.imageBG).convert()
        self.screen.blit(self.bg, (self.screen.get_width() // 2 - 512, self.screen.get_height() // 2 - 512))
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
            self.screen.blit(self.bg, (self.screen.get_width() // 2 - 512, self.screen.get_height() // 2 - 512))
            self.player.update()
            pg.display.update()
            self.clock.tick(self.fps)