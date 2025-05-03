import pygame as pg
from data.UsefulFuncs import get_config
import datetime as dt


class Ability():
    def __init__(self, screen: pg.Surface, ability: dict, player, group: pg.sprite.Group, enemy_group: pg.sprite.Group, timer):
        self.screen = screen
        self.group = group
        self.timer = timer
        self.enemy_group = enemy_group
        self.sprite = pg.transform.scale(pg.image.load(ability['icon']), (64, 64))
        self.rect = self.sprite.get_rect()
        self.old_rect = self.rect.copy()
        self.player = player
        self.ability = ability
        self.name = ability['name']
        if ability['sound']:
            cfg = get_config()
            self.sound = pg.mixer.Sound(ability["sound"])
            self.sound.set_volume(cfg.getint("Settings", "sfxvolume") / 100)
        self.level = 1
        self.max_level = ability['max_level']
        self.cooldown = ability['cooldown']
        self.projectile_amount = 1
        self.lastfired = dt.timedelta(0)
        self.projectile_addition = 0
        self.__post__init__()
    
    def __post__init__(self):
        pass
