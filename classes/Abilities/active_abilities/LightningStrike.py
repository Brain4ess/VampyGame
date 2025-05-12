from datetime import timedelta
from os import listdir
from random import choice

import pygame as pg

from data.UsefulFunctions import get_config, load_images_from_dir

from ..classAbility import Ability


# Unleashes a lightning strike that attacks multiple targets with a slight delay
class LightningStrike(Ability):
    def __post__init__(self):
        self.sprites = load_images_from_dir(self.ability['sprite'])
        self.times_fired = 0
        self.random_sounds_pool = [pg.mixer.Sound(f"{self.ability['random-sounds-dir']}/{sound}") for sound in listdir(self.ability['random-sounds-dir'])]
        for i in self.random_sounds_pool:
            i.set_volume(get_config().getint("Settings", "sfxvolume") / 100)
        self.currsprite = 0
        self.last_targeted = timedelta(0)
        self.target = None
        self._random_sound_played = False
        self.damaged = False


    def update(self, offset: pg.math.Vector2):
        if self.enemy_group.sprites():
            if self.target == None:
                self.target = choice(self.enemy_group.sprites())

            if int(self.currsprite) == 1 and self.damaged == False:
                self.target.hp -= self.ability['damage'] * (self.level)
                self.sound.stop()
                self.sound.play()
                self.damaged = True

            if self.currsprite >= len(self.sprites):
                self.currsprite = 0
                self.times_fired += 1
                self.damaged = False
                self.target = choice(self.enemy_group.sprites())
                self.last_targeted = self.timer.time

            if (self.timer.time - self.lastfired).seconds >= (self.cooldown - ((self.level - 1) / 1.45)) - 1.3 and self.enemy_group and self._random_sound_played == False:
                choice(self.random_sounds_pool).play()
                self._random_sound_played = True

            if (self.timer.time - self.lastfired).seconds >= self.cooldown - ((self.level - 1) / 1.45) and self.enemy_group:
                    self.lastfired = self.timer.time
                    self.times_fired = 0
                    self._random_sound_played = False

            if self.times_fired <= (self.ability["max_enemies"] * self.level) + self.projectile_addition:
                self.rect = self.sprites[int(self.currsprite)].get_rect(center=self.target.rect.center, bottom=self.target.rect.bottom)
                self.follow(offset)
                self.currsprite += 0.2 + (self.level / 10) - 0.1


    def follow(self, offset: pg.math.Vector2):
        offset_pos = self.rect.topleft - offset
        self.screen.blit(self.sprites[int(self.currsprite)], offset_pos)
