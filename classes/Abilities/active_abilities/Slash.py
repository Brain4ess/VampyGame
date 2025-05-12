import pygame as pg

from data.UsefulFunctions import load_images_from_dir

from ..classAbility import Ability


# Slash attack that pushes enemies around, also increases the number of slashes depending on the passive ability 'Duplicator' pumping
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
