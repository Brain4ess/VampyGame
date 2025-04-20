import os

import pygame as pg
from pygame.image import load
from pygame.locals import *
from pygame.sprite import Sprite
from pygame.transform import flip, scale_by

import classes.classAbility as clab
import data.Abilities as ab
from data.Characters import CHARACTERS


class Character(Sprite):
    def __init__(self, bg, character: str, screen: pg.Surface = None, speed: int = 0, group: pg.sprite.Group = None, enemy_group: pg.sprite.Group = None, timer = None):
        super().__init__()
        self.screen = screen
        self.speed = speed
        self.curspeed = self.speed
        self.timer = timer
        self.size = CHARACTERS[character]['scale_by']
        self.side = 'right'
        self.bg = bg
        self.group = group
        self.enemy_group = enemy_group

        self.passives = []
        self.maxhp = 100
        self.hp = 100
        self.damage = 10
        self.exp = 0
        self.lives = 0
        self.exp_next = 100
        self.exp_gain = 1.0
        self.lvl = 0
        self.characterdir = CHARACTERS[character]['sprites']
        self.cursprite = 0
        self.__post_init__(character)

    def __post_init__(self, character):
        self.scrWidth = self.screen.get_width()
        self.scrHeight = self.screen.get_height()
        
        self.sprHeroLeft: list[pg.Surface] = list()
        self.sprHeroRight: list[pg.Surface] = list()
        self.sgroup = pg.sprite.Group()
        
        self.heroCreate()
        self.rect = self.sprHeroLeft[0].get_rect(center = (self.scrWidth / 2, self.scrHeight / 2))
        self.old_rect = self.rect.copy()
        self.size = (self.sprHeroLeft[int(self.cursprite)].get_width(), self.sprHeroLeft[int(self.cursprite)].get_height())
        ability_class = getattr(clab, ab.ABILITIES[CHARACTERS[character]['startAbility']]['class'])
        self.abilities = [ability_class(self.screen, ab.ABILITIES[CHARACTERS[character]['startAbility']], self, self.group, self.enemy_group, self.timer)]
    
    def heroCreate(self):
        for i in range(len(os.listdir(self.characterdir))):
            self.sprHeroRight.append(scale_by(load(self.characterdir + f'/{i+1}.png'), self.size))
            self.sprHeroLeft.append(flip(self.sprHeroRight[i], True, False))

    def eventKey(self):
        keys = pg.key.get_pressed()
        if keys[K_d] and keys[K_s] or keys[K_a] and keys[K_s] or keys[K_d] and keys[K_w] or keys[K_a] and keys[K_w]:
            self.curspeed = self.speed / 1.4
        else:
            self.curspeed = self.speed
        if keys[K_d] or keys[K_a] or keys[K_w] or keys[K_s]:
            if keys[K_d]:
                self.side = 'right'
                self.rect.x += self.curspeed
            if keys[K_a]:
                self.side = 'left'
                self.rect.x -= self.curspeed
            if keys[K_w]:
                self.rect.y -= self.curspeed
            if keys[K_s]:
                self.rect.y += self.curspeed
            if self.cursprite >= len(self.sprHeroLeft) - 1:
                self.cursprite = 0
            else:
                self.cursprite += self.speed / 25

    def direction(self, offset: pg.math.Vector2 = (0, 0)):
        offset_pos = self.rect.topleft - offset
        if self.side == 'right':
            offset_pos = self.rect.topleft - offset
            self.screen.blit(self.sprHeroRight[int(self.cursprite)], offset_pos)
        if self.side == 'left':
            offset_pos = self.sprHeroLeft[int(self.cursprite)].get_rect(center = self.rect.center).topleft - offset
            self.screen.blit(self.sprHeroLeft[int(self.cursprite)], offset_pos)

    def get_ability(self, name: str):
        for i in self.abilities:
            if i.name == name:
                return i
        return None

    def get_passive(self, name: str):
        for i in self.passives:
            if i.name == name:
                return i
        return None

    def add_ability(self, name: str):
        ability_class = getattr(clab, ab.ABILITIES[name]['class'])
        self.abilities.append(ability_class(self.screen, ab.ABILITIES[name], self, self.group, self.enemy_group, self.timer))

    def add_passive(self, name: str):
        ability_class = getattr(clab, ab.PASSIVES[name]['class'])
        self.passives.append(ability_class(self.screen, ab.PASSIVES[name], self, self.timer))

    def level_Up(self):
        self.lvl += 1
        self.exp = self.exp % self.exp_next
        self.exp_next += 100**((self.lvl/30) + 1) #testing  #int((self.exp_next/10) * ((self.lvl / 10) + 1))
        self.maxhp += self.lvl * 10
        self.hp = self.maxhp

    def update_abilities(self, offset):
        for i in self.abilities:
            i.update(offset)

    def update(self, offset: pg.math.Vector2 = (0, 0)):
        
        if self.exp >= self.exp_next:
            self.level_Up()
            
        # When the player reaches the threshold value we stop moving in the direction the player has reached the end of a background
        self.rect.x = max(-self.bg.spawnpoint[0], min(self.bg.width - self.size[0] - self.bg.spawnpoint[0], self.rect.centerx - (self.size[0] / 2)))
        self.rect.y = max(-self.bg.spawnpoint[1], min(self.bg.height - self.size[1] - self.bg.spawnpoint[1], self.rect.centery - (self.size[1] / 2)))
        
        self.update_abilities(offset)
        self.old_rect = self.rect.copy()
        self.eventKey()
        self.direction(offset)
