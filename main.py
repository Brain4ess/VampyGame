import pygame as pg

pg.font.init()

from sys import exit
import configparser as cfgp
from UI.classGameScreen import GameScreen
from UI.GameHandler import GameHandler
import thorpy as tp
from UI.GameUI import initui

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
    with open('data/config.ini', 'w') as configfile:
        cfg.write(configfile)

pg.init()

if __name__ == "__main__":
    screen = GameScreen((cfg.getint('Settings', 'Width'), cfg.getint('Settings', 'Height')), "GitSurvivors", fullscreen=cfg.getboolean('Settings', 'Fullscreen'))
    tp.init(screen.get_screen(), tp.theme_human)
    ui = initui(screen.get_screen())

    gameHandler = GameHandler(screen, ui)
    gameHandler.mainloop()

    pg.quit()
    exit()
