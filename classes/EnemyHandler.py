import pygame as pg
from classes.classEnemy import Entity
from classes.classCharacter import Character
from classes.classCamera import Camera
import datetime as dt
import data.Constants as const
from classes.classTimer import Timer


class EnemyHandler:
    def __init__(self, screen: pg.Surface, camera: Camera, player: Character, timer: Timer):
        self.enemies = []
        self.obstacles = pg.sprite.Group()
        self.enemy_speed = 1
        self.screen = screen
        self.camera = camera
        self.player = player
        self.timer = timer
        self.lastwave = dt.datetime.now()

    def waveof(self, image: str, amount: int):
        for _ in range(amount):
            self.enemies.append(Entity(self.screen, image, self.player))
        self.lastwave = dt.datetime.now()

    def update(self):
        if len(self.enemies) > 0:
                for enemy in self.enemies:
                    enemy.update(self.camera.getoffset())
                    if enemy.hp <= 0:
                        del self.enemies[self.enemies.index(enemy)]
        
        if dt.datetime.now() - self.lastwave > dt.timedelta(seconds=3) and len(self.enemies) < 10 * ((self.timer.time.seconds // 60) + 1):
            self.waveof(const.PATHS["Characters"]["placeholder1"], 5 + (self.timer.time.seconds // 30))