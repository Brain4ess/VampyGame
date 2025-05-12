from random import choice

import pygame as pg

from classes.Entities import Projectile
from data.UsefulFunctions import load_images_from_dir

from ..classAbility import Ability


# Launches a homing shot that flies until it reaches its target (if the target is gone, it flies to the point where it died and then disappears)
class HomingShot(Ability):
        def __post__init__(self):
            self.sprites = load_images_from_dir(self.ability['sprite'])
            self.projectiles = []
            self.target = []
        
        def update(self, offset: pg.math.Vector2):
            if self.projectiles:
                for i in self.projectiles:
                    if i.hp <= 0 or i.distance <= 4:
                        self.projectiles.remove(i)
                        self.group.remove(i)
            if (self.timer.time - self.lastfired).seconds >= max(self.cooldown - ((self.level - 1) / 1.45), 0.1) and self.enemy_group:
                self.lastfired = self.timer.time
                self.projectiles.extend([Projectile(self.screen,
                                                    self.ability,
                                                    self.sprites,
                                                    self.player,
                                                    self.group,
                                                    self.timer.time,
                                                    damagable=True,
                                                    followEnemy=True,
                                                    target=choice(self.enemy_group.sprites()).rect) for _ in range(self.projectile_amount + self.projectile_addition)])
                #self.sound.play()
            if self.projectiles:
                for i in self.projectiles:
                    i.update(offset)
