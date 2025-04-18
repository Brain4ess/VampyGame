import pygame as pg
import datetime

class Timer:
    def __init__(self, screen: pg.Surface, font, color, size):
        self.screen = screen
        self.font = pg.font.Font(font, size)
        self.pos = (screen.get_width() / 2, 45)
        self.color = color
        self.size = size
        self.time = datetime.timedelta(0)
        self.timeText = self.font.render("00:00", True, self.color)
        self.pausedTime = datetime.timedelta(0)
        self.pausedAt = datetime.datetime.now()
        self.timeRect = self.timeText.get_rect(center=self.pos)

    def start(self):
        self.startTime = datetime.datetime.now()
        self.timeText = self.font.render(self.startTime.strftime("%H:%M"), True, self.color)
        self.timeRect = self.timeText.get_rect(center=self.pos)

    def pause(self, paused: bool):
        if paused:
            self.pausedAt = datetime.datetime.now()
        else:
            self.pausedAt = datetime.datetime.now() - self.pausedAt
            self.pausedTime += datetime.timedelta(self.pausedAt.days, seconds=self.pausedAt.seconds, microseconds=self.pausedAt.microseconds)

    def update(self):
        self.time = datetime.datetime.now() - self.startTime - self.pausedTime
        self.timeText = self.font.render(f"{self.time.seconds // 60}:{self.time.seconds % 60}:{self.time.microseconds // 1000 % 1000}", True, self.color, pg.color.Color(32, 32, 32, 0))
        self.screen.blit(self.timeText, self.timeRect)
