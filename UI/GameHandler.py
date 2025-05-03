import configparser as cfgp

import pygame as pg

import UI.classMainMenu as mm
from classes.classGame import Game
from data.Constants import PATHS
from UI.classGameScreen import GameScreen
from UI.GameUI import initui

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
                    CharacterSelectorOption = self.mainMenu.runCurrent(self.mainMenu.CharSelectorMenu, [self.mainMenu.CharSelectorButtonsGupd, self.mainMenu.backButtonupd])
                    if CharacterSelectorOption[0] == "Back":
                        self.mainMenu.changeMenu("CharSelector", "main")
                        break
                    if CharacterSelectorOption[0] != "QUIT" and CharacterSelectorOption[0] != "Back":
                        self.mainMenu.changeMenu("CharSelector", "MapSelector")
                        MapSelectorOption = self.mainMenu.runCurrent(self.mainMenu.MapSelectorMenu, [self.mainMenu.MapSelectorButtonsGupd, self.mainMenu.backButtonupd])
                        if MapSelectorOption[0] == "Back":
                            self.mainMenu.changeMenu("MapSelector", "CharSelector")
                            continue

                        if MapSelectorOption[0] != "QUIT" and MapSelectorOption[0] != "Back":
                            pg.mouse.set_cursor(pg.SYSTEM_CURSOR_WAIT)
                            self.mainMenu.changeMenu("MapSelector", "Game")
                            self.screen.set_caption("VampyGame")
                            pg.mixer.music.stop()
                            self.game = Game(self.screen.get_screen(), PATHS['Maps'][MapSelectorOption[0]], CharacterSelectorOption[0], self.ui)
                            pg.mouse.set_cursor(pg.SYSTEM_CURSOR_ARROW)
                            GameReturned = self.game.runGame()
                            if GameReturned == "QUIT":
                                break
                            if GameReturned == "ToMenu":
                                del self.game
                                break
                if CharacterSelectorOption[0] == "Back":
                    continue
                if GameReturned == "QUIT":
                    break
                if GameReturned == "ToMenu":

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
