import pygame as pg
import UI.classMainMenu as mm
from classes.classGame import Game
from UI.classGameScreen import GameScreen
from data.Constants import PATHS
from UI.GameUI import initui
import configparser as cfgp

cfg = cfgp.ConfigParser()
cfg.read('data/config.ini')

class GameHandler:
    def __init__(self, screen: GameScreen, ui: initui):
        self.screen = screen
        self.ui = ui
        self.mainMenu = mm.MainMenu(self.screen)
        self.running = True
        self.screen.set_caption("VampyGame: Main Menu")
        pg.mixer.music.load(PATHS['Music']['Menu'])
        pg.mixer.music.set_volume(cfg.getint("Settings", "musicvolume") / 100)
        pg.mixer.music.play(-1)

    def mainloop(self):
        while self.running:
            returned = self.mainMenu.runCurrent(self.mainMenu.menu, [self.mainMenu.buttonGroupupd])
            if not returned[1]:
                self.running = False
                break

            if returned[0] == "Play":
                pg.mouse.set_cursor(pg.SYSTEM_CURSOR_ARROW)
                self.mainMenu.changeMenu("main", "CharSelector")
                while True:
                    Creturned = self.mainMenu.runCurrent(self.mainMenu.CharSelectorMenu, [self.mainMenu.CharSelectorButtonsGupd, self.mainMenu.backButtonupd])
                    if Creturned[0] == "Back":
                        self.mainMenu.changeMenu("CharSelector", "main")
                        break
                    if Creturned[0] != "QUIT" and Creturned[0] != "Back":
                        self.mainMenu.changeMenu("CharSelector", "MapSelector")
                        Mreturned = self.mainMenu.runCurrent(self.mainMenu.MapSelectorMenu, [self.mainMenu.MapSelectorButtonsGupd, self.mainMenu.backButtonupd])
                        if Mreturned[0] == "Back":
                            self.mainMenu.changeMenu("MapSelector", "CharSelector")
                            continue

                        if Mreturned[0] != "QUIT" and Mreturned[0] != "Back":
                            pg.mouse.set_cursor(pg.SYSTEM_CURSOR_WAIT)
                            self.mainMenu.changeMenu("MapSelector", "Game")
                            self.screen.set_caption("VampyGame")
                            pg.mixer.music.stop()
                            self.game = Game(self.screen.get_screen(), PATHS['Maps'][Mreturned[0]], Creturned[0], self.ui)
                            pg.mouse.set_cursor(pg.SYSTEM_CURSOR_ARROW)
                            Greturned = self.game.runGame()
                            if Greturned == "QUIT":
                                break
                            if Greturned == "ToMenu":
                                del self.game
                                break
                if Creturned[0] == "Back":
                    continue
                if Greturned == "QUIT":
                    break
                if Greturned == "ToMenu":

                    self.mainMenu.changeMenu("Game", "main")
                    pg.mixer.music.load(PATHS['Music']['Menu'])
                    pg.mixer.music.set_volume(cfg.getint("Settings", "musicvolume") / 100)
                    pg.mixer.music.play(-1)
                    continue


            elif returned[0] == "Quit":
                self.running = False
                break

            elif returned[0] == "Settings":
                self.mainMenu.changeMenu("main", "settings")
                Sreturned = self.mainMenu.runCurrent(self.mainMenu.settingsMenu, self.mainMenu.settingsElementsupd)
                if Sreturned[0] == "Back":
                    self.mainMenu.changeMenu("settings", "main")
                    continue
                elif not Sreturned[1]:
                    self.running = False
                    break
