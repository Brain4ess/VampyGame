from random import choice

import pygame as pg

from classes.entities import Projectile
from functions.load_images_from_dir import load_images_from_dir

from ..class_active_ability import ActiveAbility


# Launches a homing shot that flies until it reaches its target (if the target is gone, it flies to the point where it died and then disappears)
class HomingShot(ActiveAbility):
    """
    A homing projectile weapon system that fires tracking missiles at enemies.
    
    This class implements an ability that launches projectiles which automatically
    track and follow enemy targets. The weapon fires multiple homing projectiles
    simultaneously, with firing rate increasing as the weapon levels up.
    
    Core Features:
    - Fires homing projectiles that track random enemy targets
    - Automatic projectile lifecycle management (creation and cleanup)
    - Level-based cooldown reduction for increased firing rate
    - Multi-projectile support with configurable projectile count
    
    Constructor Parameters:
        Inherits from Ability base class. See Ability class documentation for
        constructor parameters including screen, ability configuration, sprites,
        player reference, sprite groups, and timer.
    
    Notes:
        - Requires enemies to be present in enemy_group to fire projectiles
        - Projectiles are automatically removed when they expire or reach targets
        - Minimum cooldown is capped at 0.1 seconds regardless of level
    """
    
    def __post__init__(self):
        self.sprites = load_images_from_dir(self.ability['sprite'])
        self.projectiles = []
        self.target = []
    
    def update(self, offset: pg.math.Vector2) -> None:
        """
        Update the weapon system and its projectiles.
        
        This method handles projectile lifecycle management, firing logic based on cooldown
        and level, and updates all active projectiles.
        
        Args:
            offset (pg.math.Vector2): The offset vector used for updating projectile positions.
        
        Returns:
            None
        
        Behavior:
            - Removes projectiles that have expired (hp <= 0 or distance <= 4)
            - Fires new projectiles when cooldown has elapsed and enemies are present
            - Updates all active projectiles with the given offset
            - Cooldown decreases with weapon level, with a minimum of 0.1 seconds
            - New projectiles target random enemies and follow them
        """
        if self.projectiles:
            for i in self.projectiles:
                if i.hp <= 0 or i.distance <= 4:
                    self.projectiles.remove(i)
                    self.group.remove(i)

        if (self.timer.time - self.lastfired).seconds >= max(self.cooldown - ((self.level - 1) / 1.45), 0.1) and self.enemy_group:
            self.lastfired = self.timer.time
            self.projectiles.extend(
                [
                    Projectile(
                        self.screen,
                        self.ability,
                        self.sprites,
                        self.player,
                        self.group,
                        self.timer.time,
                        damagable=True,
                        follow_enemy=True,
                        target=choice(self.enemy_group.sprites()).rect
                    ) for _ in range(self.projectile_amount + self.projectile_addition)
                ]
            )

        if self.projectiles:
            for i in self.projectiles:
                i.update(offset)
