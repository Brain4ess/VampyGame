import pygame as pg
from math import sqrt
from classes.classCharacter import Character
import random

class Entity():
    def __init__(self, screen: pg.Surface, image: str, player: Character, damage: float = 0.3):
        self.screen = screen
        self.sprright = [pg.transform.scale(pg.image.load(image), (64, 64))]
        self.sprleft = [pg.transform.flip(self.sprright[0], True, False)]
        self.rect = self.sprright[0].get_rect()
        self.speed = 3
        self.hp = 100
        self.damage = damage
        self.player_position = player.rect
        self.player = player
        self.rect.colliderect(self.player.rect)
        self.spawnListX = [self.player_position.x + (self.screen.get_width() / 2) + 64, self.player_position.x - (self.screen.get_width() / 2) + 64]
        self.spawnListY = [self.player_position.y + (self.screen.get_height() / 2) + 64, self.player_position.y - (self.screen.get_height() / 2) + 64]
        self.rect.x = random.choice(self.spawnListX) + random.randint(-64, 64)
        self.rect.y = random.choice(self.spawnListY) + random.randint(-64, 64)
    
    def follow(self, offset: pg.math.Vector2):
        offset_pos = self.rect.topleft - offset
        self.screen.blit(self.sprright[0], offset_pos)
    
    def update(self, offset: pg.math.Vector2):
        dx = self.player_position.x - self.rect.x
        dy = self.player_position.y - self.rect.y
        distance = sqrt(dx ** 2 + dy ** 2)
        if distance > 69:
            dx = dx / distance * self.speed
            dy = dy / distance * self.speed
            self.rect.x += dx
            self.rect.y += dy
        if self.rect.colliderect(self.player.rect) and self.player.hp >= self.damage:
            self.player.hp -= self.damage
        if self.rect.colliderect(self.player.rect) and self.player.hp < self.damage and self.player.hp > 0:
            self.player.hp = 0
        if self.rect.colliderect(self.player.rect):
            self.hp -= self.player.damage
        self.follow(offset)
