from random import choice

import pygame as pg

from classes.Entities import Projectile
from data.Constants import FPS

from ..classAbility import Ability


# Fires a shuriken that flies into a random enemy position
class Shuriken(Ability):
    def __post__init__(self):
        self.sprites = []
        self.lifetime = self.ability['lifetime']
        for i in range((FPS // 2)):
            self.sprites.append(pg.transform.rotate(self.sprite, i * (360 // (FPS // 2))))
        
        self.projectiles = []
        self.target = []
        
    
    def update(self, offset: pg.math.Vector2):
        self.projectile_amount = self.projectile_addition + int((self.level / 2) + 1)
        if self.projectiles:
            for i in self.projectiles:
                if (self.timer.time - i.firedAt).seconds >= self.lifetime:
                    self.projectiles.remove(i)
                    self.group.remove(i)
        if (self.timer.time - self.lastfired).seconds >= max(self.lifetime + self.cooldown - ((self.level - 1) / 1.45), 0.25)and self.enemy_group:
            self.lastfired = self.timer.time
            self.projectiles.extend([Projectile(self.screen,
                                                self.ability,
                                                self.sprites,
                                                self.player,
                                                self.group,
                                                self.timer.time,
                                                choice(self.enemy_group.sprites()).rect.copy()) for _ in range(self.projectile_amount)])
            # self.sound.play()
        if self.projectiles:
            for i in self.projectiles:
                i.update(offset)
