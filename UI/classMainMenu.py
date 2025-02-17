import pygame as pg
from classes.classGame import Game
from UI.classGameScreen import GameScreen
from classes.classBackground import BG
from pygame.image import load
from pygame.transform import scale
from UI.actualButton import Button
import data.Constants as const
import thorpy as tp
from data.GuiData import MM_BUTTON_STYLES


class Menu:
    def __init__(self, screen: GameScreen, imageBG: str):
        self.screen = screen
        self.fps = const.FPS
        self.imageBG = imageBG
        self.bg = BG(self.imageBG, self.screen.get_screen(), fill=True)
        self.running = True

class MainMenu:
    def __init__(self, screen: GameScreen):
        self.screen = screen
        self.fps = const.FPS
        self.game = Game(self.screen.get_screen())
        self.clock = pg.time.Clock()
        self.buttons = []
        self.fonts = const.PATHS['Fonts']['mainMenu']
    
    
    # def buildMenu(self, type: str):
    #     if type == "main":
    #         self.screen.set_caption("GitSurvivors: Main Menu")
    #         self.playButton = Button(self.screen.get_screen(), 
    #                scale(load(const.PATHS['Buttons']['playButton']), (400, 100)),
    #                self.screen.get_screen().get_width() / 2,
    #                self.screen.get_screen().get_height() / 2 + 50,
    #                text_input='Play',
    #                font = self.fonts['Buttons_caps'],
    #                text_color=(176, 55, 80))
            
    #         self.quitButton = Button(self.screen.get_screen(),
    #                scale(load(const.PATHS['Buttons']['quitButton']), (400, 100)),
    #                self.screen.get_screen().get_width() / 2,
    #                self.screen.get_screen().get_height() / 2 + 170,
    #                text_input='Quit',
    #                font = self.fonts['Buttons_caps'],
    #                text_color=(176, 55, 80))
            
    #         self.menu = Menu(self.screen, const.PATHS['Backgrounds']['mainMenu'])
    
    def buildMenu(self, type: str):
        if type == "main":
            self.screen.set_caption("GitSurvivors: Main Menu")
            self.playButton = tp.Button("Play", MM_BUTTON_STYLES['normal'], MM_BUTTON_STYLES['hover'], MM_BUTTON_STYLES['pressed'])
            self.settingsButton = tp.Button("Settings", MM_BUTTON_STYLES['normal'], MM_BUTTON_STYLES['hover'], MM_BUTTON_STYLES['pressed'])
            self.quitButton = tp.Button("Quit", MM_BUTTON_STYLES['normal'], MM_BUTTON_STYLES['hover'], MM_BUTTON_STYLES['pressed'])
            self.quitButton.at_unclick = self.quitGame
            self.playButton.at_unclick = self.playbutton
            self.buttonGroup = tp.Group([self.playButton, self.settingsButton, self.quitButton], gap=20)
            self.buttonGroup.move(0, 100)
            self.buttonGroup.get_updater().manually_updated = True
            self.menu = Menu(self.screen, const.PATHS['Backgrounds']['mainMenu'])
        if type == "settings":
            self.screen.set_caption("GitSurvivors: Settings")
            self.menu = Menu(self.screen, const.PATHS['Backgrounds']['settingsMenu'])
        
    
    def runCurrent(self, menu: Menu, buttonGroup: tp.Group):
        menu.running = True
        while menu.running:
            menu.bg.blitStatic()
            buttonGroup.get_updater(self.fps).update()
            if pg.event.poll().type == pg.QUIT:
                menu.running = False
                    
            pg.display.update()
            self.clock.tick(self.fps)
    
    
    def switchToOptions(self):
        self.menu.running = False
        self.buttonGroup.set_invisible(True, True)
        pg.mouse.set_cursor(pg.SYSTEM_CURSOR_ARROW)
        self.buildMenu("settings")
        self.runCurrent()
    
    def playbutton(self):
        self.menu.running = False
        self.buttonGroup.set_invisible(True, True)
        pg.mouse.set_cursor(pg.SYSTEM_CURSOR_ARROW)
        self.game.runGame()
    
    
    def quitGame(self):
        event = pg.event.Event(pg.QUIT)
        pg.event.post(event)
    

