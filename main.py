import pygame as pg
from sys import exit
import configparser as cfgp
from UI.classGameScreen import GameScreen
from classes.classGame import Game

cfg = cfgp.ConfigParser()
cfg.read('data/config.ini')
if not cfg.has_section('Settings'):
    cfg.add_section('Settings')
    cfg.set('Settings', 'Width', '1280')
    cfg.set('Settings', 'Height', '720')
    cfg.set('Settings', 'fps', '60')
    with open('data/config.ini', 'w') as configfile:
        cfg.write(configfile)

pg.init()

if __name__ == "__main__":
    screen = GameScreen((cfg.getint('Settings', 'Width'), cfg.getint('Settings', 'Height')), "GitSurvivors")
    Game = Game(screen.get_screen(), cfg.getint('Settings', 'fps'))
    Game.runGame()
    
    pg.quit()
    exit()
