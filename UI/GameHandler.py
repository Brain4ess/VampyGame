import pygame as pg
import UI.classMainMenu as mm
from classes.classGame import Game
from UI.classGameScreen import GameScreen
from data.Constants import PATHS

class GameHandler:
    def __init__(self, screen: GameScreen):
        self.screen = screen
        self.mainMenu = mm.MainMenu(self.screen)
        self.running = True
        self.screen.set_caption("GitSurvivors: Main Menu")
    
    def mainloop(self):
        while self.running:
            returned = self.mainMenu.runCurrent(self.mainMenu.menu, [self.mainMenu.buttonGroup])
            if not returned[1]:
                self.running = False
                break
            
            if returned[0] == "Play":
                pg.mouse.set_cursor(pg.SYSTEM_CURSOR_ARROW)
                self.mainMenu.changeMenu("main", "CharSelector")
                while True:
                    Creturned = self.mainMenu.runCurrent(self.mainMenu.CharSelectorMenu, [self.mainMenu.CharSelectorButtonsG, self.mainMenu.backButton])
                    if Creturned[0] == "Back":
                        self.mainMenu.changeMenu("CharSelector", "main")
                        break
                    if Creturned[0] != "QUIT" and Creturned[0] != "Back":
                        self.mainMenu.changeMenu("CharSelector", "MapSelector")
                        Mreturned = self.mainMenu.runCurrent(self.mainMenu.MapSelectorMenu, [self.mainMenu.MapSelectorButtonsG, self.mainMenu.backButton])
                        if Mreturned[0] == "Back":
                            self.mainMenu.changeMenu("MapSelector", "CharSelector")
                            continue
                        
                        if Mreturned[0] != "QUIT" and Mreturned[0] != "Back":
                            pg.mouse.set_cursor(pg.SYSTEM_CURSOR_WAIT)
                            self.mainMenu.changeMenu("MapSelector", "Game")
                            self.screen.set_caption("GitSurvivors")
                            self.game = Game(self.screen.get_screen(), PATHS['Maps'][Mreturned[0]], PATHS['Characters'][Creturned[0]])
                            pg.mouse.set_cursor(pg.SYSTEM_CURSOR_ARROW)
                            Greturned = self.game.runGame()
                            if Greturned == "QUIT":
                                break                
                if Creturned[0] == "Back":
                    continue
                if Greturned == "QUIT":
                    break

            
            elif returned[0] == "Quit":
                self.running = False
                break
            
            elif returned[0] == "Settings":
                self.mainMenu.changeMenu("main", "settings")
                Sreturned = self.mainMenu.runCurrent(self.mainMenu.settingsMenu, self.mainMenu.settingsElements)
                if Sreturned[0] == "Back":
                    self.mainMenu.changeMenu("settings", "main")
                    continue
                elif not Sreturned[1]:
                    self.running = False
                    break
                