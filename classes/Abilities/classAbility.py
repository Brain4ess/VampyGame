import datetime as dt
from abc import ABC, abstractmethod

import pygame as pg

from data.UsefulFunctions import get_config


class Ability(ABC):
    """
    Abstract base class for player abilities in a game system.
    
    This class provides the foundation for implementing various player abilities such as weapons,
    spells, or special powers. It manages ability properties like cooldowns, levels, projectiles,
    and handles the basic setup including sprite loading, sound effects, and timing mechanics.
    
    Core functionality includes:
    - Ability level progression and upgrade system
    - Cooldown management and timing control
    - Sprite and sound resource handling
    - Integration with game groups and enemy targeting
    - Projectile amount scaling
    
    Args:
        screen (pg.Surface): The main game screen surface for rendering
        ability (dict): Configuration dictionary containing ability properties like
                       'icon', 'name', 'sound', 'max_level', 'cooldown'
        player: Reference to the player object that owns this ability
        group (pg.sprite.Group): Sprite group for managing ability projectiles
        enemy_group (pg.sprite.Group): Group containing enemy sprites for targeting
        timer: Game timer object for managing timing and cooldowns
    
    Note:
        - Subclasses must implement the __post__init__ method
        - Sound effects require proper audio configuration in game settings
        - Ability icons are automatically scaled to 64x64 pixels
    """
    def __init__(self,
                 screen: pg.Surface,
                 ability: dict,
                 player,
                 group: pg.sprite.Group,
                 enemy_group: pg.sprite.Group,
                 timer
    ):
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

    @abstractmethod
    def __post__init__(self):
        pass
