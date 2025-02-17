import pygame as pg
from classes.classGame import Game
from UI.classGameScreen import GameScreen
from classes.classBackground import BG
from pygame.image import load
from pygame.transform import scale
from UI.actualButton import Button
import data.Constants as const
import thorpy as tp
from data.GuiData import MM_BUTTON_STYLES, SM_BUTTON_STYLES

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
    
    
    def buildMenu(self, type: str):
        if type == "main":
            self.screen.set_caption("GitSurvivors: Main Menu")
            
            self.playButton = tp.Button("Play", MM_BUTTON_STYLES['normal'], MM_BUTTON_STYLES['hover'], MM_BUTTON_STYLES['pressed'])
            self.settingsButton = tp.Button("Settings", MM_BUTTON_STYLES['normal'], MM_BUTTON_STYLES['hover'], MM_BUTTON_STYLES['pressed'])
            self.quitButton = tp.Button("Quit", MM_BUTTON_STYLES['normal'], MM_BUTTON_STYLES['hover'], MM_BUTTON_STYLES['pressed'])
            
            # self.playButton.at_unclick = self.playbutton
            # self.settingsButton.at_unclick = self.switchToSettings
            # self.quitButton.at_unclick = self.quitGame
            
            # Rename the buttons
            self.buttonGroup = tp.Group([self.playButton, self.settingsButton, self.quitButton], gap=20)
            self.buttonGroup.move(0, 100)
            self.buttonGroup.get_updater().manually_updated = True
            
            self.menu = Menu(self.screen, const.PATHS['Backgrounds']['mainMenu'])
            
            
        if type == "settings":
            self.screen.set_caption("GitSurvivors: Settings")
            
            self.applyButton = tp.Button("Apply", SM_BUTTON_STYLES['normal'], SM_BUTTON_STYLES['hover'], SM_BUTTON_STYLES['pressed'])
            self.backButton = tp.Button("Back", SM_BUTTON_STYLES['normal'], SM_BUTTON_STYLES['hover'], SM_BUTTON_STYLES['pressed'])
            
            # self.applyButtonGroup = tp.Group([self.applyButton], gap=20)
            # self.backButtonGroup = tp.Group([self.backButton], gap=20)
            
            self.applyButton.move(self.screen.get_screen().get_width() - SM_BUTTON_STYLES['normal'].margins[0] + 75, self.screen.get_screen().get_height() - SM_BUTTON_STYLES['normal'].margins[1] - 30)
            self.backButton.move(SM_BUTTON_STYLES['normal'].margins[0] - 75, self.screen.get_screen().get_height() - SM_BUTTON_STYLES['normal'].margins[1]  - 30)
            
            # self.applyButton.at_unclick = 
            # self.backButton.at_unclick = self.switchToMain
            
            self.settingsMenu = Menu(self.screen, const.PATHS['Backgrounds']['settingsMenu'])
        
    
    def runCurrent(self, menu: Menu, buttonGroup: list[tp.Group] | list[tp.Button]):
        menu.running = True
        while menu.running:
            menu.bg.blitStatic()
            
            for i in buttonGroup:
                i.get_updater(self.fps).update()
                
            # for i in buttonGroup:
            #     if i is not tp.Group:
            #         if i.state == "pressed":
            #             return [i.text, True]
            #     else:
            #         for j in i.elements:
            #             if j.state == "pressed":
            #                 return [j.text, True]
            if self.playButton.state == "pressed":
                return ["Play", True]
            if self.settingsButton.state == "pressed":
                return ["Settings", True]
            if self.quitButton.state == "pressed":
                return ["Quit", True]
            if self.applyButton.state == "pressed":
                return ["Apply", True]
            if self.backButton.state == "pressed":
                return ["Back", True]
            
            # buttonGroup.get_updater(self.fps).update()
            
            if pg.event.poll().type == pg.QUIT:
                menu.running = False
                return ["Quit", False]
                    
            pg.display.update()
            self.clock.tick(self.fps)
    
    
    def switchToSettings(self):
        self.menu.running = False
        self.buttonGroup.set_invisible(True, True)
        pg.mouse.set_cursor(pg.SYSTEM_CURSOR_ARROW)
        self.buildMenu("settings")
        self.runCurrent(self.settingsMenu, [self.applyButton, self.backButton])
    
    
    def playbutton(self):
        self.menu.running = False
        self.buttonGroup.set_invisible(True, True)
        pg.mouse.set_cursor(pg.SYSTEM_CURSOR_ARROW)
        self.game.runGame()
    
    
    def switchToMain(self):
        self.settingsMenu.running = False
        self.menu.running = True
        self.applyButton.set_invisible(True, True)
        self.backButton.set_invisible(True, True)
        self.buttonGroup.set_invisible(False, True)
        self.runCurrent(self.menu, [self.buttonGroup])
    
    def quitGame(self):
        event = pg.event.Event(pg.QUIT)
        pg.event.post(event)
    

