import pygame as pg
from pygame.locals import *
from UI.classGameScreen import GameScreen
from classes.classBackground import BG
from classes.classCharacter import Character
from classes.classCamera import Camera
import data.Constants as const

class Game:
    def __init__(self, screen: GameScreen, mapImage: str, character: str):
        self.mapImage = mapImage
        self.fps = const.FPS
        self.screen = screen
        self.bg = BG(self.mapImage, self.screen, spawnpoint=(500, 500))
        self.run = True
        self.camera = Camera(self.screen, self.bg.width, self.bg.height, self.bg)
        self.player = Character(self.bg, character, self.screen, 5)
        self.clock = pg.time.Clock()
    
    
    def eventGame(self):
        for event in pg.event.get():
            if event.type == QUIT:
                self.run = False
    
    
    def runGame(self):
        while self.run:
            
            for event in pg.event.get():
                if event.type == QUIT:
                    self.run = False
                    return "QUIT"
            
            self.bg.blitBG(self.camera.getoffset())
            
            self.player.update(self.camera.getoffset())
            self.camera.update(self.player)
            
            pg.display.update()
            self.clock.tick(self.fps)
