import pygame as pg

pg.font.init()

from sys import exit
import configparser as cfgp
from UI.classGameScreen import GameScreen
from classes.classGame import Game
from UI.classButton import Button
from UI.classMainMenu import MainMenu
from data.Constants import FPS
import thorpy as tp

cfg = cfgp.ConfigParser()
cfg.read('data/config.ini')
if not cfg.has_section('Settings'):
    cfg.add_section('Settings')
    cfg.set('Settings', 'Width', '1280')
    cfg.set('Settings', 'Height', '720')
    with open('data/config.ini', 'w') as configfile:
        cfg.write(configfile)


pg.init()

if __name__ == "__main__":
    screen = GameScreen((cfg.getint('Settings', 'Width'), cfg.getint('Settings', 'Height')), "GitSurvivors")
    tp.init(screen.get_screen(), tp.theme_human)
    mainMenu = MainMenu(screen)
    mainMenu.buildMenu("main")
    mainMenu.runCurrent(mainMenu.menu, mainMenu.buttonGroup)
    
    
    pg.quit()
    exit()
