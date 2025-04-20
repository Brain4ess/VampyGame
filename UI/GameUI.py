import pygame as pg
import thorpy as tp

import data.Constants as const
from classes.classCharacter import Character
from data.Characters import CHARACTERS
from data.GuiData import IMG_BUTTON_TEXT_STYLE, MM_BUTTON_STYLES


class initui:
    def __init__(self, screen: pg.Surface):
        self.screen = screen
        self.hpbar = tp.Lifebar("", length=self.screen.get_width() / 10 * 2, height=30, bck_color=(37, 190, 106), initial_value=100 / 100, auto_adapt_length=False)
        self.hpbar.set_locked(True)
        self.hpbar.e_frame.set_bck_color(pg.color.Color(32, 32, 32))
        self.hpbar.e_frame.set_style_attr("border_color", pg.color.Color(32, 32, 32))
        self.hpbar.move(self.screen.get_width() / 2, self.screen.get_height() - 35)
        self.hpbarupd = self.hpbar.get_updater(const.FPS)

        self.lvlbar = tp.Lifebar(f"Lv. 0", length=self.screen.get_width() - 20, height=30, bck_color=(37, 150, 190), initial_value=0, auto_adapt_length=False, font_color="White")
        self.lvlbar.set_locked(True)
        self.lvlbar.e_frame.set_bck_color(pg.color.Color(32, 32, 32))
        self.lvlbar.e_frame.set_style_attr("border_color", pg.color.Color(32, 32, 32))
        self.lvlbar.move(self.screen.get_width() / 2, 10)
        self.lvlbar.life_text.move((self.screen.get_width() / 2) - 40, 0)
        self.lvlbarupd = self.lvlbar.get_updater(const.FPS)

        self.resume = tp.Button("Resume", MM_BUTTON_STYLES['normal'], MM_BUTTON_STYLES['hover'], MM_BUTTON_STYLES['pressed'])
        self.exit_to_menu = tp.Button("Exit to menu", MM_BUTTON_STYLES['normal'], MM_BUTTON_STYLES['hover'], MM_BUTTON_STYLES['pressed'])
        self.quit = tp.Button("Quit game", MM_BUTTON_STYLES['normal'], MM_BUTTON_STYLES['hover'], MM_BUTTON_STYLES['pressed'])
        self.pauseMenuButtonUpd = tp.Group([self.resume, self.exit_to_menu, self.quit], gap=10).get_updater(const.FPS)
        
        self.UpgButtons = tp.Group([], gap = 10)
        for i in range(6):
            self.UpgButtons.add_child(tp.TextAndImageButton("Shuriken", pg.transform.scale(pg.image.load(CHARACTERS["Protagonist"]["characterPreview"]), (64, 64)), reverse=True, styleNormal=MM_BUTTON_STYLES['normal'], styleHover=MM_BUTTON_STYLES['hover'], stylePressed=MM_BUTTON_STYLES['pressed'], text_style=IMG_BUTTON_TEXT_STYLE))

        self.UpgButtonsupd = self.UpgButtons.get_updater(const.FPS)


class UI:
    def __init__(self, screen: pg.Surface, player: Character, ui: initui):
        self.screen = screen
        self.player = player
        self.exit_to_menu = ui.exit_to_menu
        self.quit = ui.quit
        self.resume = ui.resume
        self.hpbar = ui.hpbar
        self.lvlbar = ui.lvlbar
        self.hpbarupd = ui.hpbarupd
        self.lvlbarupd = ui.lvlbarupd
        self.pauseMenuButtonUpd = ui.pauseMenuButtonUpd
        self.resume.at_unclick_params = {"button": self.resume}
        self.exit_to_menu.at_unclick = self.changeButtonState
        self.exit_to_menu.at_unclick_params = {"button": self.exit_to_menu}
        self.quit.at_unclick = self.changeButtonState
        self.quit.at_unclick_params = {"button": self.quit}
        self.UpgButtons = ui.UpgButtons
        for i in self.UpgButtons.children:
            i.at_unclick = self.changeButtonState
            i.at_unclick_params = {"button": i}
        self.UpgButtonsupd = ui.UpgButtonsupd


    def update(self):
        self.hpbar.set_value(self.player.hp / self.player.maxhp)
        self.hpbar.e_rect.set_bck_color(pg.color.Color.lerp(pg.color.Color(170, 35, 35), pg.color.Color(37, 190, 106), self.player.hp / self.player.maxhp))
        
        self.lvlbar.set_value(self.player.exp / self.player.exp_next)
        self.lvlbar.life_text.set_text(f"Lv. {self.player.lvl}")
        
        self.hpbarupd.update()
        self.lvlbarupd.update()


    def changeButtonState(self, button: tp.elements.Element):
        button.state = "unclicked"
        pg.mouse.set_cursor(pg.SYSTEM_CURSOR_ARROW)


    def update_Pause(self):
        self.pauseMenuButtonUpd.update()


    def update_Upgrade(self):
        self.UpgButtonsupd.update()
