import configparser as cfgp

import pygame as pg
import thorpy as tp
from pygame.image import load
from pygame.transform import scale

import data.Constants as const
from classes.classBackground import BG
from data.Characters import CHARACTERS
from data.GuiData import (IMG_BUTTON_TEXT_STYLE, MM_BUTTON_STYLES,
                          SM_BUTTON_STYLES)
from UI.classGameScreen import GameScreen

cfg = cfgp.ConfigParser()
cfg.read('data/config.ini')

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
        self.clock = pg.time.Clock()
        self.buttons = []
        self.fonts = const.PATHS['Fonts']['mainMenu']
        self.buttonclickSound = pg.mixer.Sound(file=const.PATHS['SFX']['buttonClick1'])
        self.buttonclickSound.set_volume(cfg.getint('Settings', 'sfxvolume') / 100)
        tp.Button.default_at_unclick = self.buttonclickSound.play
        self.__post_init__()


    def __post_init__(self):
        self.playButton = tp.Button("Play", MM_BUTTON_STYLES['normal'], MM_BUTTON_STYLES['hover'], MM_BUTTON_STYLES['pressed'])
        self.settingsButton = tp.Button("Settings", MM_BUTTON_STYLES['normal'], MM_BUTTON_STYLES['hover'], MM_BUTTON_STYLES['pressed'])
        self.quitButton = tp.Button("Quit", MM_BUTTON_STYLES['normal'], MM_BUTTON_STYLES['hover'], MM_BUTTON_STYLES['pressed'])

        self.playButton.at_unclick = self.changeButtonState
        self.playButton.at_unclick_params = {"button": self.playButton}
        self.settingsButton.at_unclick = self.changeButtonState
        self.settingsButton.at_unclick_params = {"button": self.settingsButton}
        self.quitButton.at_unclick = self.changeButtonState
        self.quitButton.at_unclick_params = {"button": self.quitButton}

        self.buttonGroup = tp.Group([self.playButton, self.settingsButton, self.quitButton], gap=20)
        self.buttonGroup.move(0, 100)
        self.buttonGroup.get_updater().manually_updated = True

        self.menu = Menu(self.screen, const.PATHS['Backgrounds']['mainMenu'])

        self.applyButton = tp.Button("Apply", SM_BUTTON_STYLES['normal'], SM_BUTTON_STYLES['hover'], SM_BUTTON_STYLES['pressed'])
        self.backButton = tp.Button("Back", SM_BUTTON_STYLES['normal'], SM_BUTTON_STYLES['hover'], SM_BUTTON_STYLES['pressed'])

        self.masterSlider = tp.SliderWithText("Master", 0, 100, cfg.getint('Settings', 'mastervolume'), 100)
        self.SFXSlider = tp.SliderWithText("SFX", 0, 100, cfg.getint('Settings', 'sfxvolume'), 100)
        self.musicSlider = tp.SliderWithText("Music", 0, 100, cfg.getint('Settings', 'musicvolume'), 100)
        self.audioGroup = tp.Group([self.masterSlider, self.SFXSlider, self.musicSlider], gap=20)

        self.reslist = pg.display.list_modes()
        self.reslist = [str(self.reslist[i][0]) + "x" + str(self.reslist[i][1]) for i in range(len(self.reslist))]
        self.resolutionDD = tp.DropDownListButton(self.reslist, cfg.get('Settings', 'width') + "x" + cfg.get('Settings', 'height'), SM_BUTTON_STYLES['normal'], style_hover=SM_BUTTON_STYLES["hover"], style_pressed=SM_BUTTON_STYLES["pressed"], style_locked=SM_BUTTON_STYLES["locked"], generate_shadow=(True, True), size_limit=["auto", 250])
        self.resolutionDD.move(self.screen.get_screen().get_width() - SM_BUTTON_STYLES['normal'].margins[0] + 75, self.screen.get_screen().get_height() / 2 - SM_BUTTON_STYLES['normal'].margins[1] - 30)
        self.resolutionText = tp.Text("Resolution", font_size=30, font_color=SM_BUTTON_STYLES['normal'].font_color, style_normal=IMG_BUTTON_TEXT_STYLE)
        self.resolutionText.move(self.screen.get_screen().get_width() - (SM_BUTTON_STYLES['normal'].margins[0] + 75) - 100, self.screen.get_screen().get_height() / 2 - SM_BUTTON_STYLES['normal'].margins[1] - 30)
        self.resolutionText.default_at_unclick = self.do_nothing

        self.fullscreenCheckbox = tp.Checkbox(value=cfg.getboolean("Settings", "Fullscreen"),style_normal=SM_BUTTON_STYLES["normal"], style_hover=SM_BUTTON_STYLES["hover"], style_pressed=SM_BUTTON_STYLES["pressed"])
        self.FullscreenText = tp.Text("Fullscreen", font_size=30, font_color=SM_BUTTON_STYLES['normal'].font_color, style_normal=IMG_BUTTON_TEXT_STYLE)
        self.FullscreenText.default_at_unclick = self.do_nothing
        self.fullscreenCheckbox.move(self.screen.get_screen().get_width() / 2 - (SM_BUTTON_STYLES['normal'].margins[0] + 75) - 100, self.screen.get_screen().get_height() / 2 - SM_BUTTON_STYLES['normal'].margins[1] - 30)
        self.FullscreenText.move(self.screen.get_screen().get_width() / 2 - (SM_BUTTON_STYLES['normal'].margins[0] + 75) - 180, self.screen.get_screen().get_height() / 2 - SM_BUTTON_STYLES['normal'].margins[1] - 33)
        
        self.applyButton.move(self.screen.get_screen().get_width() - SM_BUTTON_STYLES['normal'].margins[0] + 75, self.screen.get_screen().get_height() - SM_BUTTON_STYLES['normal'].margins[1] - 30)
        self.backButton.move(SM_BUTTON_STYLES['normal'].margins[0] - 75, self.screen.get_screen().get_height() - SM_BUTTON_STYLES['normal'].margins[1]  - 30)

        self.applyButton.at_unclick = self.applySettings
        self.backButton.at_unclick = self.changeButtonState
        self.backButton.at_unclick_params = {"button": self.backButton}

        self.settingsElements = [self.applyButton, self.backButton, self.audioGroup, self.fullscreenCheckbox, self.FullscreenText, self.resolutionText, self.resolutionDD]
        self.settingsMenu = Menu(self.screen, const.PATHS['Backgrounds']['settingsMenu'])

        self.characterSelectorButtons = []
        for keys, values in CHARACTERS.items():
            self.characterSelectorButtons.append(tp.TextAndImageButton(text=keys, img=scale(load(values['characterPreview']), (32, 32)), mode="v", styleNormal=SM_BUTTON_STYLES['normal'], styleHover=SM_BUTTON_STYLES['hover'], stylePressed=SM_BUTTON_STYLES['pressed'], text_style=IMG_BUTTON_TEXT_STYLE))

        for i in self.characterSelectorButtons:
            i.at_unclick = self.changeButtonState
            i.at_unclick_params = {"button": i}
            for j in i.children:
                j.default_at_unclick = self.do_nothing

        self.characterSelectorButtonsG = tp.Group(self.characterSelectorButtons, gap=20, mode="h")
        self.characterSelectorButtonsGupd = self.characterSelectorButtonsG.get_updater(self.fps)
        self.backButtonupd = self.backButton.get_updater(self.fps)

        self.settingsElementsupd = [i.get_updater(self.fps) for i in self.settingsElements]
        self.buttonGroupupd = self.buttonGroup.get_updater(self.fps)
        self.characterSelectorMenu = Menu(self.screen, const.PATHS['Backgrounds']['CharacterSelector'])

        self.MapSelectorButtons = []
        for keys, values in const.PATHS['Maps'].items():
            self.MapSelectorButtons.append(tp.TextAndImageButton(text=keys, img=scale(load(values), (128, 128)), mode="h", margins=(10, 15), reverse=True, styleNormal=SM_BUTTON_STYLES['normal'], styleHover=SM_BUTTON_STYLES['hover'], stylePressed=SM_BUTTON_STYLES['pressed'], text_style=IMG_BUTTON_TEXT_STYLE))

        for i in self.MapSelectorButtons:
            i.at_unclick = self.changeButtonState
            i.at_unclick_params = {"button": i}
            for j in i.children:
                j.default_at_unclick = self.do_nothing

        self.MapSelectorButtonsG = tp.Group(self.MapSelectorButtons, gap=20, mode="v")
        self.MapSelectorMenu = Menu(self.screen, const.PATHS['Backgrounds']['MapSelector'])
        self.MapSelectorButtonsGupd = self.MapSelectorButtonsG.get_updater(self.fps)

    def do_nothing(self):
        pass

    def runCurrent(self, menu: Menu, buttonGroup: list[tp.Group] | list[tp.elements.Element]):
        menu.running = True
        while menu.running:
            menu.bg.blitStatic()

            for i in buttonGroup:
                i.update()

            if menu == self.menu:
                if self.playButton.state == "unclicked":
                    return ["Play", True]

                if self.settingsButton.state == "unclicked":
                    return ["Settings", True]

                if self.quitButton.state == "unclicked":
                    return ["Quit", True]

            if menu == self.settingsMenu or menu == self.characterSelectorMenu or menu == self.MapSelectorMenu:
                if self.backButton.state == "unclicked":
                    return ["Back", True]

            if menu == self.characterSelectorMenu:
                for i in self.characterSelectorButtons:
                    if i.state == "unclicked":
                        return [i.children[0].text, True]

            if menu == self.MapSelectorMenu:
                for i in self.MapSelectorButtons:
                    if i.state == "unclicked":
                        return [i.children[1].text, True]

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

    def changeMenu(self, From: str, To: str):
        if From == "main" and To == "settings":
            self.screen.set_caption("VampyGame: Settings")
            self.buttonGroup.set_invisible(True, True)
            self.applyButton.set_invisible(False, True)
            self.backButton.set_invisible(False, True)
            pg.mouse.set_cursor(pg.SYSTEM_CURSOR_ARROW)

        if From == "settings" and To == "main":
            self.screen.set_caption("VampyGame: Main Menu")
            self.applyButton.set_invisible(True, True)
            self.backButton.set_invisible(True, True)
            self.buttonGroup.set_invisible(False, True)
            pg.mouse.set_cursor(pg.SYSTEM_CURSOR_ARROW)

        if From == "main" and To == "CharacterSelector":
            self.screen.set_caption("VampyGame: Character Selector")
            self.buttonGroup.set_invisible(True, True)
            self.characterSelectorButtonsG.set_invisible(False, True)
            self.backButton.set_invisible(False, True)
            pg.mouse.set_cursor(pg.SYSTEM_CURSOR_ARROW)

        if From == "CharacterSelector" and To == "main":
            self.screen.set_caption("VampyGame: Main Menu")
            self.buttonGroup.set_invisible(False, True)
            self.characterSelectorButtonsG.set_invisible(True, True)
            self.backButton.set_invisible(True, True)
            pg.mouse.set_cursor(pg.SYSTEM_CURSOR_ARROW)

        if From == "CharacterSelector" and To == "MapSelector":
            self.screen.set_caption("VampyGame: Map Selector")
            self.characterSelectorButtonsG.set_invisible(True, True)
            self.MapSelectorButtonsG.set_invisible(False, True)
            self.backButton.set_invisible(False, True)
            pg.mouse.set_cursor(pg.SYSTEM_CURSOR_ARROW)

        if From == "MapSelector" and To == "CharacterSelector":
            self.screen.set_caption("VampyGame: Character Selector")
            self.MapSelectorButtonsG.set_invisible(True, True)
            self.characterSelectorButtonsG.set_invisible(False, True)
            self.backButton.set_invisible(False, True)
            pg.mouse.set_cursor(pg.SYSTEM_CURSOR_ARROW)

        if From == "Game" and To == "main":
            self.screen.set_caption("VampyGame: Main Menu")
            self.buttonGroup.set_invisible(False, True)
            self.characterSelectorButtonsG.set_invisible(True, True)
            self.MapSelectorButtonsG.set_invisible(True, True)
            self.backButton.set_invisible(True, True)
            pg.mouse.set_cursor(pg.SYSTEM_CURSOR_ARROW)

    def changeButtonState(self, button: tp.elements.Element):
        button.state = "unclicked"

    def applySettings(self):
        if self.resolutionDD.get_value() != None:
            res = self.resolutionDD.get_value().split("x")
            cfg.set('Settings', 'width', res[0])
            cfg.set('Settings', 'height', res[1])
        cfg.set('Settings', 'fullscreen', str(self.fullscreenCheckbox.get_value()))
        cfg.set('Settings', 'mastervolume', str(self.masterSlider.get_value()))
        cfg.set('Settings', 'musicvolume', str(self.musicSlider.get_value()))
        cfg.set('Settings', 'sfxvolume', str(self.SFXSlider.get_value()))
        with open('data/config.ini', 'w') as configfile:
            cfg.write(configfile)

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
