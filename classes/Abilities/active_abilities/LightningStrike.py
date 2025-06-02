from datetime import timedelta
from os import listdir
from random import choice

import pygame as pg

from data.UsefulFunctions import get_config, load_images_from_dir

from ..classAbility import Ability


# Unleashes a lightning strike that attacks multiple targets with a slight delay
class LightningStrike(Ability):
    """
    A lightning strike ability that targets random enemies with animated lightning attacks.
    
    This class implements a lightning-based attack ability that automatically targets
    random enemies within range, dealing damage with visual and audio effects. The
    ability features animated lightning sprites, sound effects, and level-based
    scaling for damage, attack speed, and number of targets.
    
    Core Features:
    - Automatic random enemy targeting
    - Animated lightning strike effects
    - Sound effects with random pre-attack sounds
    - Level-based damage scaling and cooldown reduction
    - Multiple strikes per cooldown cycle
    - Camera offset support for scrolling games
    
    Constructor Parameters:
    - Inherits from Ability class, so constructor parameters depend on parent class
    - Requires ability configuration dict with keys: 'sprite', 'random-sounds-dir', 
      'damage', 'max_enemies'
    - Needs enemy_group, timer, and screen objects to be set via parent class
    
    Notes:
    - Requires sprite images in specified directory
    - Requires sound files in random-sounds-dir
    - Attack frequency increases with level
    - Number of strikes per cycle scales with level and max_enemies setting
    - Sound volume is controlled by global SFX volume setting
    """
    
    def __post__init__(self):
        self.sprites = load_images_from_dir(self.ability['sprite'])
        self.times_fired = 0
        self.random_sounds_pool = [
            pg.mixer.Sound(f"{self.ability['random-sounds-dir']}/{sound}") for sound in listdir(self.ability['random-sounds-dir'])
        ]
        for i in self.random_sounds_pool:
            i.set_volume(get_config().getint("Settings", "sfxvolume") / 100)
        self.curr_spr = 0
        self.last_targeted = timedelta(0)
        self.target = None
        self._random_sound_played = False
        self.damaged = False

    def update(self, offset: pg.math.Vector2) -> None:
        """
        Update the lightning attack behavior and animation.
        
        This method handles the lightning attack's targeting system, damage dealing,
        animation progression, sound effects, and cooldown management. The lightning
        will target random enemies from the enemy group and deal damage based on
        the current level.
        
        Args:
            offset (pg.math.Vector2): The camera offset for positioning adjustments.
            
        Behavior:
            - Selects random targets from available enemies
            - Deals damage when animation reaches frame 1
            - Plays sound effects during attack and random pre-attack sounds
            - Manages attack cooldown based on level (faster attacks at higher levels)
            - Limits number of attacks per cooldown cycle based on max_enemies ability
            - Animates lightning sprite with level-dependent speed
        """
        if self.enemy_group.sprites():
            if self.target == None:
                self.target = choice(self.enemy_group.sprites())

            if int(self.curr_spr) == 1 and self.damaged == False:
                self.target.hp -= self.ability['damage'] * (self.level)
                self.sound.stop()
                self.sound.play()
                self.damaged = True

            if self.curr_spr >= len(self.sprites):
                self.curr_spr = 0
                self.times_fired += 1
                self.damaged = False
                self.target = choice(self.enemy_group.sprites())
                self.last_targeted = self.timer.time

            if ((self.timer.time - self.lastfired).seconds >= (self.cooldown - ((self.level - 1) / 1.45)) - 1.3
                and self.enemy_group
                and self._random_sound_played is False
            ):
                choice(self.random_sounds_pool).play()
                self._random_sound_played = True

            if ((self.timer.time - self.lastfired).seconds >= self.cooldown - ((self.level - 1) / 1.45)
                and self.enemy_group
            ):
                    self.lastfired = self.timer.time
                    self.times_fired = 0
                    self._random_sound_played = False

            if self.times_fired <= (self.ability["max_enemies"] * self.level) + self.projectile_addition:
                self.rect = self.sprites[int(self.curr_spr)].get_rect(center=self.target.rect.center, bottom=self.target.rect.bottom)
                self.follow(offset)
                self.curr_spr += 0.2 + (self.level / 10) - 0.1

    def follow(self, offset: pg.math.Vector2) -> None:
        """
        Render the sprite at a position adjusted by the given offset.
        
        This method is typically used for camera following or scrolling effects,
        where the sprite needs to be drawn relative to a camera or viewport offset.
        
        Args:
            offset (pg.math.Vector2): The offset vector to adjust the sprite's 
                                    position. The sprite will be drawn at 
                                    (rect.topleft - offset).
        
        Note:
            - Uses the current sprite frame (int(self.curr_spr)) from self.sprites
            - Blits the sprite to self.screen at the calculated offset position
        """
        offset_pos = self.rect.topleft - offset
        self.screen.blit(self.sprites[int(self.curr_spr)], offset_pos)
