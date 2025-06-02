from random import choice as random_choice

import pygame as pg

from classes.Entities import Projectile
from data.Constants import FPS

from ..classAbility import Ability


# Fires a shuriken that flies into a random enemy position
class Shuriken(Ability):
    """
    A projectile-based ability that launches rotating shuriken towards enemies.
    
    This class manages a system of spinning shuriken projectiles that automatically
    target enemies. The shuriken rotate through pre-generated sprite frames and
    have a limited lifetime. The ability scales with level, increasing both the
    number of projectiles fired and reducing cooldown time.
    
    Core functionality:
    - Automatic enemy targeting with random selection
    - Rotating sprite animation for visual appeal
    - Level-based scaling for projectile count and cooldown
    - Automatic projectile lifecycle management
    - Cooldown-based firing system
    
    Constructor Parameters (inherited from Ability):
        - Inherits all parameters from the parent Ability class
        - Uses 'lifetime' from ability data to determine projectile duration
        - Generates rotating sprite frames based on FPS (typically 30 frames)
    
    Notes:
        - Requires enemies to be present in enemy_group to fire projectiles
        - Minimum cooldown is capped at 0.25 seconds regardless of level
        - Projectiles are automatically cleaned up after lifetime expires
        - Each firing cycle creates multiple projectiles equal to projectile_amount
    """
    def __post__init__(self):
        self.sprites = []
        self.lifetime = self.ability['lifetime']
        for i in range((FPS // 2)):
            self.sprites.append(pg.transform.rotate(self.sprite, i * (360 // (FPS // 2))))
        self.projectiles = []
        self.target = []


    def update(self, offset: pg.math.Vector2) -> None:
        """
        Update the projectile system, managing projectile lifecycle and firing logic.
        
        This method handles:
        - Calculating the number of projectiles based on current level
        - Removing expired projectiles that have exceeded their lifetime
        - Creating new projectiles when cooldown conditions are met
        - Updating all active projectiles with the given offset
        
        Args:
            offset (pg.math.Vector2): The offset vector to apply to all projectiles
                                    for position updates, typically used for camera
                                    movement or screen scrolling.
        
        Note:
            - Projectile amount increases with level: base amount + int((level / 2) + 1)
            - Projectiles are automatically removed after their lifetime expires
            - New projectiles are fired when cooldown period has passed and enemies exist
            - Cooldown decreases with level but has a minimum of 0.25 seconds
            - Each new projectile targets a randomly selected enemy from the enemy group
        """
        self.projectile_amount = self.projectile_addition + int((self.level / 2) + 1)

        if self.projectiles:
            for i in self.projectiles:
                if (self.timer.time - i.fired_at).seconds >= self.lifetime:
                    self.projectiles.remove(i)
                    self.group.remove(i)

        if (
            (self.timer.time - self.lastfired).seconds >= max(self.lifetime + self.cooldown - ((self.level - 1) / 1.45), 0.25)
            and self.enemy_group
        ):
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
                        random_choice(self.enemy_group.sprites()).rect.copy()
                    ) for _ in range(self.projectile_amount)
                ]
            )

        if self.projectiles:
            for i in self.projectiles:
                i.update(offset)
