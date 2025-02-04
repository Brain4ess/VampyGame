import pygame as pg
from sys import exit
from classes.classGame import Game

pg.init()

if __name__ == "__main__":
    
    Game = Game()
    Game.runGame()
    
    pg.quit()
    exit()