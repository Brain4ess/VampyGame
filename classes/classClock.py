import pygame as pg
import time

class Timer:
    def __init__(self, screen, font, pos, color, size):
        self.screen = screen
        self.font = font
        self.pos = pos
        self.color = color
        self.size = size
        self.time = time.time()
        self.timeText = self.font.render("00:00", True, self.color)
        self.timeRect = self.timeText.get_rect(center=self.pos)


    # TODO: Write timer logic
    def update(self):
        pass