import pygame as pg
from classes.classGame import Game
from UI.classGameScreen import GameScreen

class Menu:
    def __init__(self, screen: GameScreen, fps: int):
        self.screen = screen
        self.fps = fps
        self.game = Game(self.screen.get_screen(), self.fps)
        self.clock = pg.time.Clock()
        self.running = True
    
    
    #TODO : Make main menu
    def mainMenu(self):
        self.screen.set_caption("GitSurvivors: Main Menu")
        
        while self.running:
            pass
    
    
    #TODO : Make options menu
    def optionsMenu(self):
        self.screen.set_caption("GitSurvivors: Options")
        
        while self.running:
            pass
