import pygame as pg
from classes.classGame import Game
from UI.classGameScreen import GameScreen
from classes.classBackground import BG
from pygame.image import load
from pygame.transform import scale
#from UI.classButton import Button
from UI.actualButton import Button

class MainMenu:
    def __init__(self, screen: GameScreen, fps: int):
        self.screen = screen
        self.fps = fps
        self.game = Game(self.screen.get_screen(), self.fps)
        self.clock = pg.time.Clock()
        self.buttons = []
    
    def buildMenu(self, type: str):
        if type == "main":
            self.screen.set_caption("Main Menu")
            self.playButton = Button(self.screen.get_screen(), 
                   scale(load('assets/images/placeholders/buttons/playButton.png'), (400,100)),
                   self.screen.get_screen().get_width() / 2,
                   self.screen.get_screen().get_height() / 2 + 50,
                   text_input='Play',
                   font = 'Algerian',
                   text_color=(176, 55, 80))
            self.settingsButton = Button(self.screen.get_screen(),
                   scale(load('assets/images/placeholders/buttons/settingsButton.png'), (400,100)),
                   self.screen.get_screen().get_width() / 2,
                   self.screen.get_screen().get_height() / 2 + 170,
                   text_input='Settings',
                   font = 'Algerian',
                   text_color=(176, 55, 80))
            self.quitButton = Button(self.screen.get_screen(),
                   scale(load('assets/images/placeholders/buttons/quitButton.png'), (400,100)),
                   self.screen.get_screen().get_width() / 2,
                   self.screen.get_screen().get_height() / 2 + 290,
                   text_input='Quit',
                   font = 'Algerian',
                   text_color=(176, 55, 80))
            self.menu = Menu(self.screen, self.fps, "assets/images/Background/MainMenu_Background.png", self.buttons)
        
    def runCurrent(self):
        self.menu.running = True
        while self.menu.running:
            self.menu.bg.blitStatic()
            
            for button in [self.playButton, self.settingsButton, self.quitButton]:
                    button.update()
                    button.changeColor(pg.mouse.get_pos())
                    
            if pg.event.poll().type == pg.MOUSEBUTTONDOWN:
                if self.playButton.checkForInput(pg.mouse.get_pos()):
                    self.playbutton()
                if self.settingsButton.checkForInput(pg.mouse.get_pos()):
                    self.switchToOptions()
                if self.quitButton.checkForInput(pg.mouse.get_pos()):
                    self.quitGame()
            if pg.event.poll().type == pg.QUIT:
                self.menu.running = False
                    
            pg.display.update()
            self.menu.clock.tick(self.fps)
    
    def playbutton(self):
        self.menu.running = False
        self.game.runGame()
    
    
    def switchToOptions(self):
        print("switch to options")
    
    
    def quitGame(self):
        e = pg.event.Event(pg.QUIT)
        pg.event.post(e)
    

class Menu:
    def __init__(self, screen: GameScreen, fps: int, imageBG: str, buttons: list[Button] = []):
        self.screen = screen
        self.fps = fps
        self.imageBG = imageBG
        self.game = Game(self.screen.get_screen(), self.fps)
        self.clock = pg.time.Clock()
        self.bg = BG(self.imageBG, self.screen.get_screen(), fill=True)
        self.running = True
        self.buttons = buttons
    
    
    def addbuttons(self, buttons: list[Button]):
        self.buttons.extend(buttons)