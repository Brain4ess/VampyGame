"""This module need you to run the game"""
from sys import exit as sys_exit
import pygame as pg

pg.font.init()

import configparser as cfgp

import thorpy as tp

from UI.game_screen import GameScreen
from UI.game_handler import GameHandler
from UI.game_ui import InitUI

cfg = cfgp.ConfigParser()
cfg.read('data/config.ini')
if not cfg.has_section('Settings'):
    cfg.add_section('Settings')
    cfg.set('Settings', 'Width', '1280')
    cfg.set('Settings', 'Height', '720')
    cfg.set('Settings', 'MasterVolume', '50')
    cfg.set('Settings', 'MusicVolume', '50')
    cfg.set('Settings', 'SFXVolume', '50')
    cfg.set('Settings', 'Fullscreen', 'False')
    with open('data/config.ini', 'w', encoding='utf-8') as configfile:
        cfg.write(configfile)

pg.init()

if __name__ == "__main__":
    screen = GameScreen(
        (
            cfg.getint('Settings', 'Width'),
            cfg.getint('Settings', 'Height')
        ),
        "VampyGame",
        fullscreen=cfg.getboolean('Settings', 'Fullscreen')
    )

    tp.init(screen.get_screen(), tp.theme_human)
    ui = InitUI(screen.get_screen())

    game_handler = GameHandler(screen, ui)
    game_handler.mainloop()

    pg.quit()
    sys_exit(0)
