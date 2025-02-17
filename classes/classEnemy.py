import pygame as pg

class Enemy:
    def __init__(self, screen: pg.Surface, image: str, pos: tuple):
        self.screen = screen
        self.image = pg.image.load(image)
        self.rect = self.image.get_rect(topleft=pos)
        self.mask = pg.mask.from_surface(self.image)
        self.speed = 1
        self.direction = pg.math.Vector2(0, 0)