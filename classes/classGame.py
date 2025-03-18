import pygame as pg
from pygame.locals import *
from UI.classGameScreen import GameScreen
from classes.classBackground import BG
from classes.classCharacter import Character
from classes.classCamera import Camera
import data.Constants as const
from classes.classTimer import Timer
from classes.EnemyHandler import EnemyHandler
from UI.GameUI import UI

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
        self.timer = Timer(self.screen, const.PATHS["Fonts"]["Timer"], 'White', 30)
        self.timer.start()
        self.EnemyHandler = EnemyHandler(self.screen, self.camera, self.player, self.timer)
        self.ui = UI(self.screen, self.player)
    
    
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
            self.EnemyHandler.update()
            self.player.update(self.camera.getoffset())
            self.ui.update()
            self.camera.update(self.player)
            self.timer.update()
            pg.display.update()
            self.clock.tick(self.fps)
