from ..classAbility import Ability
import pygame as pg
from random import choice

from data.UsefulFuncs import get_config, load_images_from_dir

class Starfall(Ability):
    def __post__init__(self):
        self.right_sprites, self.left_sprites = load_images_from_dir(self.ability['sprite'], with_flip=True)
        self.currsprite = 0
        self.target = None
        self.damaged = False
        self.direction = 'r'
    
    def update(self, offset):
        if self.enemy_group.sprites():
            if self.target == None:
                self.target = choice(self.enemy_group.sprites())

            if int(self.currsprite) == 10 and self.damaged == False:
                self.target.hp -= self.ability['damage'] * (self.level)
                # self.sound.stop()
                # self.sound.play()
                self.damaged = True
                

            if (self.timer.time - self.lastfired).seconds >= self.cooldown - ((self.level - 1) / 1.45) and self.enemy_group:
                    self.lastfired = self.timer.time
                    self.currsprite = 0
                    self.damaged = False
                    self.target = choice(self.enemy_group.sprites())
                    if self.target.old_rect.x > self.target.rect.x:
                        self.direction = 'r'
                    else:
                        self.direction = 'l'

            if self.currsprite <= len(self.right_sprites) - 1:
                if self.direction == 'r':
                    self.rect = self.right_sprites[int(self.currsprite)].get_rect(center=self.target.rect.center, right=self.target.rect.right)
                else:
                    self.rect = self.left_sprites[int(self.currsprite)].get_rect(center=self.target.rect.center, left=self.target.rect.left)
                self.follow(offset, self.direction)
                self.currsprite += 0.5
    
    
    def follow(self, offset: pg.math.Vector2, dir_: str = "r"):
        offset_pos = self.rect.topleft - offset
        if dir_ == 'r':
            self.screen.blit(self.right_sprites[int(self.currsprite)], offset_pos)
        else:
            self.screen.blit(self.left_sprites[int(self.currsprite)], offset_pos)