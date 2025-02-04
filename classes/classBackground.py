import pygame as pg
from UI.classGameScreen import GameScreen

class Background:
    def __init__(self, screen, image, x, y):
        self.screen = pg.Surface((1280, 720))
        self.image = pg.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self):
        self.screen.blit(self.image, self.rect)