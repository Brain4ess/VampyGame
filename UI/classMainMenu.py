import pygame as pg
from classes.classGame import Game
from UI.classGameScreen import GameScreen
from classes.classBackground import BG
from UI.classButton import Button

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
            self.buttons = [
            Button((self.screen.get_screen().get_width() / 2 - 100, self.screen.get_screen().get_height() / 2 + 50), (200, 50), text='Play', onClickReferences=self.playbutton),
            Button((self.screen.get_screen().get_width() / 2 - 100, self.screen.get_screen().get_height() / 2 + 150) , (200, 50), text='Settings', onClickReferences=self.switchToOptions),
            Button((self.screen.get_screen().get_width() / 2 - 100, self.screen.get_screen().get_height() / 2 + 250) , (200, 50), text='Quit', onClickReferences=self.quitGame)
            ]
            self.menu = Menu(self.screen, self.fps, "assets/images/Background/MainMenu_Background.png", self.buttons)
        
    def runCurrent(self):
        self.menu.running = True
        while self.menu.running:
            self.menu.eventListener()
            self.menu.bg.blitStatic()
            
            for button in self.buttons:
                button.handleEvent(pg.event.poll())
                button.update(self.screen.get_screen())
            pg.display.update()
            self.menu.clock.tick(self.fps)
    
    def playbutton(self):
        print("play")
    
    
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
        self.bg = BG(self.imageBG, self.screen.get_screen())
        self.running = True
        self.buttons = buttons
    
    
    def addbuttons(self, buttons: list[Button]):
        self.buttons.extend(buttons)
        
    
    def eventListener(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
    
    
    #TODO : Make main menu
    def runMenu(self):
        while self.running:
            self.eventListener()
            
            
            self.bg.blitStatic()
            
            if len(self.buttons) > 0:
                for i in self.buttons: # ts pmo sybau atp
                    for j in pg.event.get():
                        i.handleEvent(j)
                    i.update(self.screen.get_screen())
            
            pg.display.update()
            self.clock.tick(self.fps)
    
    
    #TODO : Make options menu
    def optionsMenu(self):
        self.screen.set_caption("GitSurvivors: Options")
        
        while self.running:
            pass
