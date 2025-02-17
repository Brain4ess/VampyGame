import pygame as pg
import UI.classMainMenu as mm
from classes.classGame import Game

class GameHandler:
    def __init__(self, screen):
        self.screen = screen
        self.game = Game(self.screen.get_screen())
        self.mainMenu = mm.MainMenu(self.screen)
        self.running = True
        self.mainMenu.buildMenu("main")
        self.mainMenu.buildMenu("settings")
    
    def mainloop(self):
        while self.running:
            self.mainMenu.applyButton.set_invisible(True, True)
            self.mainMenu.backButton.set_invisible(True, True)
            self.mainMenu.buttonGroup.set_invisible(False, True)
            returned = self.mainMenu.runCurrent(self.mainMenu.menu, [self.mainMenu.buttonGroup])
            if not returned[1]:
                self.running = False
                break
            if returned[0] == "Play":
                Greturned = self.game.runGame()
                if Greturned == "QUIT":
                    break
                continue
            elif returned[0] == "Quit":
                self.running = False
                break
            elif returned[0] == "Settings":
                self.mainMenu.applyButton.set_invisible(False, True)
                self.mainMenu.backButton.set_invisible(False, True)
                self.mainMenu.buttonGroup.set_invisible(True, True)
                Sreturned = self.mainMenu.runCurrent(self.mainMenu.settingsMenu, [self.mainMenu.applyButton, self.mainMenu.backButton])
                if Sreturned[0] == "Back":
                    continue
    #             elif Sreturned[0] == "Apply": # смену настроек и подтягивание всех элементов интерфейса сделать методом класса меню, возвращать не надо ничего
    #                 self.applySettings()
    #             elif not Sreturned[1]:
    #                 self.running = False
    #                 break
        
    # def applySettings():
    #     pass