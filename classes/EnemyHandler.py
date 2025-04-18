import pygame as pg
from classes.Entities import Enemy
from classes.classCharacter import Character
from classes.classCamera import Camera
import datetime as dt
from classes.classTimer import Timer
from data.Enemies import ENEMIES
import random


class EnemyHandler:
    def __init__(self, screen: pg.Surface, camera: Camera, player: Character, timer: Timer, group: pg.sprite.Group, enemy_group: pg.sprite.Group):
        self.enemies = []
        self.enemy_group = enemy_group
        self.enemy_speed = 1
        self.screen = screen
        self.camera = camera
        self.player = player
        self.timer = timer
        self.SprGroup = group
        self.lastwave = dt.datetime.now()

    def spawn_in(self, enemy: str):
        self.enemies.append(Enemy(self.screen, enemy, self.player, self.camera, self.SprGroup, self.enemy_group))
        self.lastwave = dt.datetime.now()

    def update(self):
        enemies_to_delete = []
        if len(self.enemies) > 0:
                for enemy in self.enemies:
                    enemy.update(self.camera.getoffset(), self.SprGroup)
                    if enemy.hp <= 0:
                        enemies_to_delete.append(enemy)
                        self.player.exp += (enemy.exp * ((self.timer.time.seconds // 60) + 1)) * self.player.exp_gain
                        
        for enemy in enemies_to_delete:
            del self.enemies[self.enemies.index(enemy)]
            self.SprGroup.remove(enemy)
            self.enemy_group.remove(enemy)
            del enemies_to_delete[enemies_to_delete.index(enemy)]
            
        if dt.datetime.now() - self.lastwave > dt.timedelta(milliseconds=100) and len(self.enemies) < 10 * ((self.timer.time.seconds // 60) + 1):
            self.spawn_in(ENEMIES[random.choices(list(ENEMIES.keys()), weights=[ENEMIES[enemy]['weight'] for enemy in list(ENEMIES.keys())])[0]])
