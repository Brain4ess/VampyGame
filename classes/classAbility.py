import datetime as dt
import os
import random

import pygame as pg

from classes.Entities import Projectile
from data.Constants import FPS
from data.UsefulFuncs import get_config, load_images_from_dir


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


class Passive():
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
    
    def __post__init__(self):
        pass
    
    def onAbilityAdd(self, ability):
        pass
    
    def onPassiveAdd(self, passive):
        pass


##########################################
###############  Passives  ###############
##########################################


class Duplicator(Passive):
    def __post__init__(self):
        self.onlevelup()
    
    def onlevelup(self):
        self.level += 1
        for i in self.player.abilities:
            i.projectile_addition += 1
    
    def onAbilityAdd(self, ability):
        ability.projectile_addition += self.level


class Overclock(Passive):
    def __post__init__(self):
        self.onlevelup()

    def onlevelup(self):
        self.level +=1
        for i in self.player.abilities:
            i.cooldown -= 0.25
    
    def onAbilityAdd(self, ability):
        ability.cooldown -= self.level * 0.25


class Overlevel(Passive):
    def __post__init__(self):
        self.onlevelup()

    def onlevelup(self):
        self.level += 1
        for i in self.player.abilities:
            i.max_level += 1
        for i in self.player.passives:
            if not (i is self):
                i.max_level += 1
    
    def onAbilityAdd(self, ability):
        ability.max_level += self.level
    
    def onPassiveAdd(self, passive):
        passive.max_level += self.level


class Mirror(Passive): 
    def __post__init__(self):
        cloning = random.choice(self.player.abilities)
        import classes.classAbility as clab
        self.clone = getattr(clab, cloning.ability['class'])
        self.clone = self.clone(self.screen, cloning.ability, cloning.player, cloning.group, cloning.enemy_group, cloning.timer)
        self.clone.name += ' mirrored'
        self.player.abilities.append(self.clone)

    def onlevelup(self):
        self.level += 1
        self.clone.level += 1


class Cheese(Passive):
    def __post__init__(self):
        self.onlevelup()
    
    def onlevelup(self):
        self.level += 1
        self.player.lives += 1


class MoreExp(Passive):
    def __post__init__(self):
        self.onlevelup()

    def onlevelup(self):
        self.level += 1
        self.player.exp_gain *= 1.6


##########################################
###########  Active Abilities  ###########
##########################################


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
                                                random.choice(self.enemy_group.sprites()).rect.copy()) for _ in range(self.projectile_amount)])
            # self.sound.play()
        if self.projectiles:
            for i in self.projectiles:
                i.update(offset)


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
                                                    target=random.choice(self.enemy_group.sprites()).rect) for _ in range(self.projectile_amount + self.projectile_addition)])
                #self.sound.play()
            if self.projectiles:
                for i in self.projectiles:
                    i.update(offset)

class LightningStrike(Ability):
    def __post__init__(self):
        self.sprites = load_images_from_dir(self.ability['sprite'])
        self.times_fired = 0
        self.random_sounds_pool = [pg.mixer.Sound(f"{self.ability['random-sounds-dir']}/{sound}") for sound in os.listdir(self.ability['random-sounds-dir'])]
        for i in self.random_sounds_pool:
            i.set_volume(get_config().getint("Settings", "sfxvolume") / 100)
        self.currsprite = 0
        self.last_targeted = dt.timedelta(0)
        self.target = None
        self._random_sound_played = False
        self.damaged = False


    def update(self, offset: pg.math.Vector2):
        if self.enemy_group.sprites():
            if self.target == None:
                self.target = random.choice(self.enemy_group.sprites())

            if int(self.currsprite) == 1 and self.damaged == False:
                self.target.hp -= self.ability['damage'] * (self.level)
                self.sound.stop()
                self.sound.play()
                self.damaged = True

            if self.currsprite >= len(self.sprites):
                self.currsprite = 0
                self.times_fired += 1
                self.damaged = False
                self.target = random.choice(self.enemy_group.sprites())
                self.last_targeted = self.timer.time

            if (self.timer.time - self.lastfired).seconds >= (self.cooldown - ((self.level - 1) / 1.45)) - 1.3 and self.enemy_group and self._random_sound_played == False:
                random.choice(self.random_sounds_pool).play()
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
                self.target = random.choice(self.enemy_group.sprites())

            if int(self.currsprite) == 10 and self.damaged == False:
                self.target.hp -= self.ability['damage'] * (self.level)
                # self.sound.stop()
                # self.sound.play()
                self.damaged = True
                

            if (self.timer.time - self.lastfired).seconds >= self.cooldown - ((self.level - 1) / 1.45) and self.enemy_group and int(self.currsprite) >= len(self.right_sprites) - 1:
                    self.lastfired = self.timer.time
                    self.currsprite = 0
                    self.damaged = False
                    self.target = random.choice(self.enemy_group.sprites())
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


class Slash(Ability, pg.sprite.Sprite):
    def __post__init__(self):
        self.right_sprites = []
        self.left_sprites = []
        for value in self.ability['sprites'].values():
            right, left = load_images_from_dir(value, -90, True, True)
            self.right_sprites.append(right)
            self.left_sprites.append(left)

        self.currsprite = 0
        self.direction = 'right'
        self.current_color = 0
        self.times_fired = 0
        self.projectile_addition = 1
        self.damage = self.ability["damage"]
        self.damageable = False
        self.old_rect = self.right_sprites[0][0].get_rect(center=self.player.rect.center)
        pg.sprite.Sprite.__init__(self, self.group)

    def update(self, offset):
        self.damage = self.ability["damage"] * (self.level)
        if self.currsprite >= len(self.right_sprites[0]):
            self.old_rect = self.rect.copy()
            self.currsprite = 0
            self.times_fired += 1
            self.current_color += 1

        if self.current_color >= len(self.right_sprites):
            self.current_color = 0
            
        if self.times_fired == self.projectile_addition:
            self.kill()
        
        if (self.timer.time - self.lastfired).seconds >= self.cooldown - ((self.level - 1) / 1.45) and self.enemy_group:
            self.add(self.group)
            self.lastfired = self.timer.time
            self.direction = self.player.side
            self.times_fired = 0
            self.current_color = 0
            self.old_rect = self.right_sprites[0][0].get_rect(center=self.player.rect.center)

        if self.current_color < len(self.right_sprites) and self.times_fired < self.projectile_addition:
            self.old_rect.x += self.player.rect.x - self.player.old_rect.x
            
            if self.times_fired == self.projectile_addition // 2 and self.currsprite == 0:
                self.old_rect = self.right_sprites[0][0].get_rect(center=self.player.rect.center)
                if self.direction == 'right':
                    self.direction = 'left'
                else:
                    self.direction = 'right'
            
            if self.direction == 'right':
                self.rect = self.right_sprites[self.current_color][int(self.currsprite)].get_rect(center=self.player.rect.center, left=self.old_rect.right)
            else:
                self.rect = self.left_sprites[self.current_color][int(self.currsprite)].get_rect(center=self.player.rect.center, right=self.old_rect.left)
            
            self.follow(offset, self.direction)
            self.currsprite += 0.4 + (self.level / 10) - 0.1

    def follow(self, offset: pg.math.Vector2, dir_: str = "right"):
        offset_pos = self.rect.topleft - offset
        if dir_ == "right":
            if self.times_fired % 2 == 0:
                self.screen.blit(pg.transform.flip(self.right_sprites[self.current_color][int(self.currsprite)], False, True), offset_pos)
            else:
                self.screen.blit(self.right_sprites[self.current_color][int(self.currsprite)], offset_pos)
        else:
            if self.times_fired % 2 == 0:
                self.screen.blit(pg.transform.flip(self.left_sprites[self.current_color][int(self.currsprite)], False, True), offset_pos)
            else:
                self.screen.blit(self.left_sprites[self.current_color][int(self.currsprite)], offset_pos)
