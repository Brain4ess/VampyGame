import pygame as pg
from math import sqrt
import random
from os import listdir
import configparser as cfgp
import datetime as dt

class Enemy(pg.sprite.Sprite):
    def __init__(self, screen: pg.Surface, enemy: dict, player, camera, group: pg.sprite.Group, enemy_group:pg.sprite.Group):
        super().__init__(group, enemy_group)
        self.screen = screen
        self.sprright = []
        self.sprleft = []
        self.spriteCreate(enemy)
        self.currsprite = 0
        self.rect = self.sprright[0].get_rect()
        self.speed = enemy['speed']
        self.hp = enemy['health']
        self.exp = enemy['exp']
        self.damage = enemy['damage']
        self.sound = enemy['sound']
        if self.sound != None:
            cfg = cfgp.ConfigParser()
            cfg.read('data/config.ini')
            self.sound_player = pg.mixer.Sound(self.sound)
            self.sound_player.set_volume(cfg.getint('Settings', 'sfxvolume') / 100)
        self.player_position = player.rect
        self.player = player
        self.old_rect = self.rect.copy()
        self.lastdamaged = dt.datetime.now()
        self.spawnListX = [camera.camera.x + (self.screen.get_width()) + (64 * 2), camera.camera.x - (64 * 2)]
        self.spawnListY = [camera.camera.y + (self.screen.get_height()) + (64 * 2), camera.camera.y - (64 * 2)]
        tempchoice = random.choice(["h", "v"])
        if tempchoice == "h":
            self.rect.x = random.randint(self.spawnListX[1], self.spawnListX[0])
            self.rect.y = random.choice(self.spawnListY)
        elif tempchoice == "v":
            self.rect.x = random.choice(self.spawnListX)
            self.rect.y = random.randint(self.spawnListY[1], self.spawnListY[0])

    def follow(self, offset: pg.math.Vector2, dx):
        if dx < 0:
            self.screen.blit(self.sprleft[int(self.currsprite)], self.rect.topleft - offset)
        else:
            self.screen.blit(self.sprright[int(self.currsprite)], self.rect.topleft - offset)
        if self.currsprite >= len(self.sprright) - 1:
            self.currsprite = 0
        else:
            self.currsprite += 0.2

    def spriteCreate(self, enemy: dict):
        for i in range(len(listdir(enemy['sprites']))):
            self.sprright.append(pg.transform.scale_by(pg.image.load(f'{enemy['sprites']}/{i+1}.png'), enemy["image_multiplier"]))
            self.sprleft.append(pg.transform.flip(self.sprright[i], True, False))

    def collision(self, direction, group: pg.sprite.Group):
        collisions = pg.sprite.spritecollide(self, group, False)
        if collisions:
            if direction == "h":
                for sprite in collisions:
                    if sprite.__class__.__name__ != "Enemy" and sprite.__class__.__name__ != "Character":
                        if (self.lastdamaged + dt.timedelta(milliseconds=200)) < dt.datetime.now():
                            self.hp -= sprite.damage
                            self.lastdamaged = dt.datetime.now()
                            if self.sound != None:
                                self.sound_player.stop()
                                self.sound_player.play()
                            if sprite.damageable:
                                sprite.hp -= self.damage
                    if self.rect.right >= sprite.rect.left and self.old_rect.right <= sprite.old_rect.left:
                        self.rect.right = sprite.rect.left
                    elif self.rect.left <= sprite.rect.right and self.old_rect.left >= sprite.old_rect.right:
                        self.rect.left = sprite.rect.right
            if direction == "v":
                for sprite in collisions:
                    if self.rect.bottom >= sprite.rect.top and self.old_rect.bottom <= sprite.old_rect.top:
                        self.rect.bottom = sprite.rect.top
                    elif self.rect.top <= sprite.rect.bottom and self.old_rect.top >= sprite.old_rect.bottom:
                        self.rect.top = sprite.rect.bottom

    def update(self, offset: pg.math.Vector2, group: pg.sprite.Group):
        tg = group.copy()
        tg.remove(self)
        self.old_rect = self.rect.copy()
        dx = self.player_position.x - self.rect.x
        dy = self.player_position.y - self.rect.y
        distance = sqrt(dx ** 2 + dy ** 2)
        if distance > self.sprright[0].get_size()[0] / 1.5:
            dx = dx / distance * self.speed
            dy = dy / distance * self.speed
            self.rect.x += dx
            self.collision("h", tg)
            self.rect.y += dy
            self.collision("v", tg)
        tg.empty()
        del tg

        if self.rect.colliderect(self.player.rect) and self.player.hp >= self.damage:
            self.player.hp -= self.damage
        if self.rect.colliderect(self.player.rect) and self.player.hp < self.damage and self.player.hp > 0:
            self.player.hp = 0

        self.follow(offset, dx)

class Projectile(pg.sprite.Sprite):
    def __init__(self, screen: pg.Surface, ability: dict, sprites: list[pg.Surface], player, group: pg.sprite.Group, firedAt, target: pg.Rect = None, damagable: bool = False, followEnemy: bool = False):
        super().__init__(group)
        self.screen = screen
        self.player = player
        self.ability = ability
        self.speed = ability["speed"]
        self.damage = ability["damage"]
        self.sprites = sprites
        self.firedAt = firedAt
        self.target = target
        self.damageable = damagable
        if self.damageable:
            self.hp = ability["hp"]
        self.isalive = True
        self.rect = self.sprites[0].get_rect(center=self.player.rect.center)
        self.old_rect = self.rect.copy()
        self.currsprite = 0
        self.distance = 0
        if not followEnemy:
            target.x -= (self.player.rect.x - target.x) * 10
            target.y -= (self.player.rect.y - target.y) * 10

    def follow(self, offset: pg.math.Vector2):
        offset_pos = self.rect.topleft - offset
        self.screen.blit(self.sprites[self.currsprite], offset_pos)

    def update(self, offset: pg.math.Vector2):
        self.old_rect = self.rect.copy()
        if self.currsprite >= len(self.sprites):
            self.currsprite = 0

        self.rect = self.sprites[self.currsprite].get_rect(center=self.rect.center)

        dx = self.target.x - self.rect.x
        dy = self.target.y - self.rect.y
        self.distance = sqrt(dx ** 2 + dy ** 2)
        if self.distance > 0:
            dx = dx / self.distance * self.speed
            dy = dy / self.distance * self.speed
            self.rect.x += dx
            self.rect.y += dy
        self.follow(offset)
        self.currsprite += 1
