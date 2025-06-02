from random import choice

import pygame as pg

from data.UsefulFunctions import load_images_from_dir

from ..classAbility import Ability

# Starburst a specific enemy
class Starfall(Ability):
    """
    A special ability that creates a starfall attack targeting enemies.
    
    This class represents a ranged magical attack ability that automatically targets
    random enemies and deals damage through an animated sprite sequence. The starfall
    effect follows the target enemy and adjusts its direction based on enemy movement.
    
    Core Features:
    - Automatic enemy targeting with random selection
    - Animated sprite-based attack sequence
    - Direction-aware rendering (left/right facing sprites)
    - Cooldown-based attack timing with level scaling
    - Damage dealing at specific animation frames
    - Dynamic positioning relative to target enemies
    
    Constructor Parameters:
        Inherits from Ability class - refer to parent class for parameter details.
        The ability configuration should include 'sprite' path and 'damage' values.
    
    Special Notes:
        - Requires enemy_group to contain valid enemy sprites for targeting
        - Damage scales with ability level
        - Cooldown decreases as level increases
        - Sprite animation must have exactly 11 frames (0-10) for proper damage timing
        - Target selection changes on each attack cycle
    """
    
    def __post__init__(self):
        self.right_sprites, self.left_sprites = load_images_from_dir(
            self.ability['sprite'], with_flip=True
        )
        self.current_sprite = 0
        self.target = None
        self.damaged = False
        self.direction = 'r'

    def update(self, offset) -> None:
        """
        Update the character's state and perform actions based on enemy targets.
        
        This method handles target selection, damage dealing, attack timing, sprite animation,
        and positioning relative to the target enemy.
        
        Args:
            offset: The offset value used for following/positioning calculations.
            
        The method performs the following operations:
        1. Selects a random target from available enemies if none exists
        2. Deals damage when the attack sprite reaches frame 10
        3. Manages attack cooldown timing and resets attack cycle
        4. Updates character direction based on target movement
        5. Positions character sprites relative to target and animates
        """
        if self.enemy_group.sprites():
            if self.target is None:
                self.target = choice(self.enemy_group.sprites())

            if int(self.current_sprite) == 10 and self.damaged == False:
                self.target.hp -= self.ability['damage'] * (self.level)
                self.damaged = True

            if (
                (self.timer.time - self.lastfired).seconds >= self.cooldown - ((self.level - 1) / 1.45)
                and self.enemy_group
                and int(self.current_sprite) >= len(self.right_sprites) - 1
            ):
                self.lastfired = self.timer.time
                self.current_sprite = 0
                self.damaged = False
                self.target = choice(self.enemy_group.sprites())

                if self.target.old_rect.x > self.target.rect.x:
                    self.direction = 'r'
                else:
                    self.direction = 'l'

            if self.current_sprite <= len(self.right_sprites) - 1:
                if self.direction == 'r':
                    self.rect = self.right_sprites[int(self.current_sprite)].get_rect(center=self.target.rect.center, right=self.target.rect.right)
                else:
                    self.rect = self.left_sprites[int(self.current_sprite)].get_rect(center=self.target.rect.center, left=self.target.rect.left)
                self.follow(offset, self.direction)
                self.current_sprite += 0.5
    
    
    def follow(self, offset: pg.math.Vector2, dir_: str = "r") -> None:
        """
        Render the character sprite at a position adjusted by the given offset.
        
        This method draws the character sprite on the screen at a position calculated
        by subtracting the offset from the character's current rectangle position.
        The sprite direction (left or right) is determined by the dir_ parameter.
        
        Args:
            offset (pg.math.Vector2): The offset vector to subtract from the character's
                                    current position to determine the render position.
            dir_ (str, optional): The direction the character is facing. 
                                "r" for right (default), any other value for left.
        
        Note:
            - Uses self.current_sprite to determine which frame of animation to display
            - The sprite is rendered at (self.rect.topleft - offset) position
            - Assumes self.right_sprites and self.left_sprites contain the sprite images
        """
        offset_pos = self.rect.topleft - offset
        if dir_ == 'r':
            self.screen.blit(self.right_sprites[int(self.current_sprite)], offset_pos)
        else:
            self.screen.blit(self.left_sprites[int(self.current_sprite)], offset_pos)
