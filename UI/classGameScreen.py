import pygame as pg
from pygame.display import set_mode, set_caption, set_icon
from pygame.image import load
from dataclasses import dataclass

@dataclass
class GameScreen(pg.Surface):
    size: tuple = (1280, 720)
    caption: str = ""
    icon: str = ""
    fullscreen: bool = False
    
    def __post_init__(self):
        if self.fullscreen:
            self.win = set_mode(self.size, pg.FULLSCREEN)
        else:
            self.win = set_mode(self.size)
        set_caption(self.caption)
        if self.icon:
            set_icon(load(self.icon))

    def get_screen(self):
        return self.win

    def set_caption(self, caption: str):
        set_caption(caption)
