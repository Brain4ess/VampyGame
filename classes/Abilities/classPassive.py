from abc import ABC, abstractmethod

import pygame as pg


class Passive(ABC):
    def __init__(self, screen: pg.Surface, passive: dict, player, timer):
        self.screen = screen
        self.player = player
        self.timer = timer
        self.passive = passive
        self.name = passive['name']
        self.level = 0
        self.max_level = passive['max_level']
        self.sprite = pg.transform.scale(pg.image.load(passive['icon']), (64, 64))
        self.__post__init__()

    @abstractmethod
    def __post__init__(self):
        pass

    def onAbilityAdd(self, ability):
        pass

    def onPassiveAdd(self, passive):
        pass
