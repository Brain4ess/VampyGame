import pygame as pg
import thorpy as tp
import data.Constants as const
from classes.classCharacter import Character

class UI:
    def __init__(self, screen: pg.Surface, player: Character):
        self.screen = screen
        self.player = player
        self.hpbar = tp.Lifebar("", length=self.screen.get_width() / 10 * 2, height=30, bck_color=(37, 190, 106), initial_value=player.hp / 100, auto_adapt_length=False)
        self.hpbar.set_locked(True)
        self.hpbar.e_frame.set_bck_color(pg.color.Color(32, 32, 32))
        self.hpbar.e_frame.set_style_attr("border_color", pg.color.Color(32, 32, 32))
        self.hpbar.move(self.screen.get_width() / 2, self.screen.get_height() - 35)
        self.hpbarupd = self.hpbar.get_updater(const.FPS)
        
    def update(self):
        self.hpbar.set_value(self.player.hp / 100)
        self.hpbar.e_rect.set_bck_color(pg.color.Color.lerp(pg.color.Color(170, 35, 35), pg.color.Color(37, 190, 106), self.player.hp / 100))
        self.hpbarupd.update()
    
    