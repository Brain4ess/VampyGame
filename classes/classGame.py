import pygame as pg
import configparser as cfgp
from pygame.locals import *
from UI.classGameScreen import GameScreen
from classes.classBackground import BG
from classes.classCharacter import Character
from pygame.transform import scale, flip
from pygame.image import load
from classes.classCamera import Camera

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
        self.run = True
        self.camera = Camera(self.screen, self.bg.get_width(), self.bg.get_height())
        self.clock = pg.time.Clock()
        self.player = Character(self.screen, 5)
        
        
    def eventGame(self):
        for event in pg.event.get():
            if event.type == QUIT:
                self.run = False
                
    def runGame(self):
        while self.run:
            
            self.eventGame()
            
            offsetbg = self.bg.get_rect().topleft - self.camera.getoffset()
            self.screen.blit(self.bg, offsetbg)
            
            self.player.update(self.camera.getoffset())
            self.camera.update(self.player)
            pg.display.update()
            self.clock.tick(self.fps)