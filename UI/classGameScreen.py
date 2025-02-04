import pygame as pg
from pygame.display import set_mode, set_caption, set_icon
from pygame.image import load
from dataclasses import dataclass

@dataclass
class GameScreen:
    size: tuple = (1280, 720)
    caption: str = "GitSurvivors"
    icon: str = ""
    
    def __post_init__(self):
        self.win = set_mode(self.size)
        set_caption(self.caption)
        if self.icon:
            set_icon(load(self.icon))