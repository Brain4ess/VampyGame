import os

import pygame as pg
from pygame.image import load
from pygame.locals import *
from pygame.sprite import Sprite
from pygame.transform import flip, scale_by

from classes import Abilities
import data.Abilities as ab
from data.Characters import CHARACTERS


class Character(Sprite):
    """
    A playable character class that extends Sprite functionality for game entities.
    
    This class represents a player-controlled character in a 2D game environment with 
    comprehensive features including movement, combat, leveling, and ability management.
    
    Core Features:
    - Player movement with keyboard input (WASD keys)
    - Sprite animation with directional facing (left/right)
    - Experience and leveling system with automatic stat progression
    - Ability and passive skill management
    - Health and damage system
    - Collision detection and boundary constraints
    - Timer-based updates and rendering
    
    Constructor Parameters:
        bg: Background object that defines the game world boundaries and spawn points
        character (str): Character type identifier that must exist in CHARACTERS config dictionary
        screen (pg.Surface, optional): Pygame surface for rendering. Defaults to None
        speed (int, optional): Base movement speed in pixels per frame. Defaults to 0
        group (pg.sprite.Group, optional): Sprite group for collision detection. Defaults to None
        enemy_group (pg.sprite.Group, optional): Enemy sprite group for combat interactions. Defaults to None
        timer (optional): Game timer object for time-based operations. Defaults to None
    
    Important Notes:
        - The 'character' parameter must correspond to a valid entry in the CHARACTERS configuration
        - Requires sprite images to be numbered sequentially (1.png, 2.png, etc.) in the character's sprite directory
        - Movement speed is automatically adjusted for diagonal movement to maintain consistent velocity
        - Position is automatically constrained to background boundaries during updates
        - Character starts at level 0 with 100 HP and gains stats through experience progression
    """
    def __init__(self,
                 bg,
                 character: str,
                 screen: pg.Surface = None,
                 speed: int = 0,
                 group: pg.sprite.Group = None,
                 enemy_group: pg.sprite.Group = None,
                 timer = None
    ) -> None:
        super().__init__()
        self.screen = screen
        self.speed = speed
        self.curspeed = self.speed
        self.timer = timer
        self.size = CHARACTERS[character]['scale_by']
        self.side = 'right'
        self.bg = bg
        self.group = group
        self.enemy_group = enemy_group
        self.passives = []
        self.max_hp = 100
        self.hp = 100
        self.damage = 10
        self.exp = 0
        self.lives = 0
        self.exp_next = 100
        self.exp_gain = 1.0
        self.lvl = 0
        self.plr_spr_dir = CHARACTERS[character]['sprites']
        self.curr_sprite = 0
        self.__post_init__(character)

    def __post_init__(self, character):
        self.screen_width = self.screen.get_width()
        self.screen_height = self.screen.get_height()

        self.plr_spr_left: list[pg.Surface] = list()
        self.plr_spr_right: list[pg.Surface] = list()

        self.plr_create()
        self.rect = self.plr_spr_left[0].get_rect(center = (self.screen_width / 2, self.screen_height / 2))
        self.old_rect = self.rect.copy()
        self.size = (self.plr_spr_left[int(self.curr_sprite)].get_width(), self.plr_spr_left[int(self.curr_sprite)].get_height())
        ability_class = getattr(Abilities, ab.ABILITIES[CHARACTERS[character]['startAbility']]['class'])
        self.abilities = [
            ability_class(
                self.screen,
                ab.ABILITIES[CHARACTERS[character]['startAbility']],
                self,
                self.group,
                self.enemy_group,
                self.timer
            )
        ]

    def plr_create(self) -> None:
        """
        Create and load player sprites for both left and right directions.
        
        This method loads all sprite images from the player sprite directory,
        scales them according to the specified size, and creates mirrored
        versions for left-facing movement.
        
        The method populates two lists:
        - plr_spr_right: Contains right-facing player sprites
        - plr_spr_left: Contains left-facing player sprites (horizontally flipped)
        
        The sprites are loaded from numbered files (1.png, 2.png, etc.) in
        the player sprite directory and scaled to match the player's size.
        """
        for i in range(len(os.listdir(self.plr_spr_dir))):
            self.plr_spr_right.append(scale_by(load(self.plr_spr_dir + f'/{i+1}.png'), self.size))
            self.plr_spr_left.append(flip(self.plr_spr_right[i], True, False))

    def event_key(self) -> None:
        """
        Handle keyboard input events for player movement.
        
        This method processes keyboard input to move the player character in four directions
        (up, down, left, right) and manages diagonal movement speed adjustment. It also
        handles sprite animation and direction tracking.
        
        Key mappings:
            - K_d: Move right
            - K_a: Move left  
            - K_w: Move up
            - K_s: Move down
            
        Movement behavior:
            - Diagonal movement (two keys pressed simultaneously) reduces speed by factor of 1.4
            - Single direction movement uses normal speed
            - Updates player's facing direction ('left' or 'right')
            - Advances sprite animation frame based on movement speed
            
        Attributes modified:
            - self.curspeed: Current movement speed (adjusted for diagonal movement)
            - self.side: Player's facing direction ('left' or 'right')
            - self.rect.x: Player's horizontal position
            - self.rect.y: Player's vertical position  
            - self.curr_sprite: Current sprite frame index for animation
        """
        keys = pg.key.get_pressed()
        if keys[K_d] and keys[K_s] or keys[K_a] and keys[K_s] or keys[K_d] and keys[K_w] or keys[K_a] and keys[K_w]:
            self.curspeed = self.speed / 1.4
        else:
            self.curspeed = self.speed
        if keys[K_d] or keys[K_a] or keys[K_w] or keys[K_s]:
            if keys[K_d]:
                self.side = 'right'
                self.rect.x += self.curspeed
            if keys[K_a]:
                self.side = 'left'
                self.rect.x -= self.curspeed
            if keys[K_w]:
                self.rect.y -= self.curspeed
            if keys[K_s]:
                self.rect.y += self.curspeed
            if self.curr_sprite >= len(self.plr_spr_left) - 1:
                self.curr_sprite = 0
            else:
                self.curr_sprite += self.speed / 25

    def direction(self, offset: pg.math.Vector2 = (0, 0)) -> None:
        """
        Render the player sprite in the correct direction based on the current side.
        
        This method handles the rendering of player sprites for both left and right
        facing directions. It calculates the proper position offset and blits the
        appropriate sprite to the screen.
        
        Args:
            offset (pg.math.Vector2, optional): The camera or screen offset to apply
                when rendering the sprite. Defaults to (0, 0).

        Note:
            - For 'right' side: Uses the current sprite from plr_spr_right list
            - For 'left' side: Uses the current sprite from plr_spr_left list and
              centers it properly before applying the offset
            - The curr_sprite attribute should be a float/int representing the
              current animation frame index
        """
        offset_pos = self.rect.topleft - offset

        if self.side == 'right':
            offset_pos = self.rect.topleft - offset
            self.screen.blit(self.plr_spr_right[int(self.curr_sprite)], offset_pos)

        if self.side == 'left':
            offset_pos = self.plr_spr_left[int(self.curr_sprite)].get_rect(center = self.rect.center).topleft - offset
            self.screen.blit(self.plr_spr_left[int(self.curr_sprite)], offset_pos)

    def get_ability(self, name: str):
        """
        Retrieve an ability by its name from the abilities collection.
        
        This method searches through the abilities list to find an ability
        with the specified name and returns it if found.
        
        Args:
            name (str): The name of the ability to search for.
            
        Returns:
            Ability or None: The ability object if found, None otherwise.
        """
        for i in self.abilities:
            if i.name == name:
                return i
        return None

    def get_passive(self, name: str):
        """
        Retrieve a passive by its name from the passives collection.
        
        Args:
            name (str): The name of the passive to search for.
            
        Returns:
            object or None: The passive object if found, None otherwise.
        """
        for i in self.passives:
            if i.name == name:
                return i
        return None

    def add_ability(self, name: str) -> None:
        """
        Add an ability to the entity by creating an instance of the specified ability class.
        
        This method retrieves the ability class from the Abilities module based on the provided
        ability name, then creates an instance of that class with the necessary parameters
        and adds it to the entity's abilities list.
        
        Args:
            name (str): The name of the ability to add. This name should correspond to a
                       key in the ab.ABILITIES dictionary that contains the ability
                       configuration including the class name.
        
        Raises:
            AttributeError: If the ability class is not found in the Abilities module.
            KeyError: If the ability name is not found in ab.ABILITIES dictionary.
        """
        ability_class = getattr(Abilities, ab.ABILITIES[name]['class'])
        self.abilities.append(ability_class(self.screen, ab.ABILITIES[name], self, self.group, self.enemy_group, self.timer))

    def add_passive(self, name: str) -> None:
        """
        Add a passive ability to the entity.
        
        This method creates an instance of a passive ability class based on the
        provided name and adds it to the entity's passives list.
        
        Args:
            name (str): The name of the passive ability to add. This name should
                       correspond to a key in the ab.PASSIVES dictionary.
        
        Raises:
            AttributeError: If the specified ability class doesn't exist in Abilities module.
            KeyError: If the name doesn't exist in ab.PASSIVES dictionary.
        """
        ability_class = getattr(Abilities, ab.PASSIVES[name]['class'])
        self.passives.append(ability_class(self.screen, ab.PASSIVES[name], self, self.timer))

    def level_up(self) -> None:
        """
        Levels up the character by increasing level and updating related attributes.
        
        This method performs the following operations:
        - Increments the character's level by 1
        - Calculates remaining experience after level up
        - Updates experience required for next level using exponential formula
        - Increases maximum HP based on new level
        - Restores HP to maximum
        
        The experience requirement for next level follows the formula:
        exp_next += 100 ** ((level/30) + 1)
        
        Maximum HP increases by 10 points per level gained.
        """
        self.lvl += 1
        self.exp = self.exp % self.exp_next
        self.exp_next += 100 ** ((self.lvl/30) + 1)
        self.max_hp += self.lvl * 10
        self.hp = self.max_hp

    def update_abilities(self, offset) -> None:
        """
        Update all abilities with the given offset.
        
        This method iterates through all abilities in the abilities collection
        and calls the update method on each ability with the provided offset.
        
        Args:
            offset: The offset value to be passed to each ability's update method.
                   This could be a time delta, position offset, or other update parameter
                   depending on the ability implementation.
        
        Note:
            This method assumes that all items in self.abilities have an update() method
            that accepts an offset parameter.
        """
        for i in self.abilities:
            i.update(offset)

    def update(self, offset: pg.math.Vector2 = (0, 0)) -> None:
        """
        Update the player's state including level progression, position constraints, and abilities.
        
        This method handles the main update cycle for the player object, including:
        - Level progression based on experience points
        - Position clamping to stay within background boundaries
        - Ability updates
        - Event handling and movement direction processing
        
        Args:
            offset (pg.math.Vector2, optional): Position offset vector for camera or world movement.
                                              Defaults to (0, 0).
        
        Note:
            The position is constrained to prevent the player from moving outside the
            background boundaries, taking into account the background spawn point and
            the player's size.
        """
        if self.exp >= self.exp_next:
            self.level_up()

        # When the player reaches the threshold value we stop moving in the direction the player has reached the end of a background
        self.rect.x = max(-self.bg.spawnpoint[0], min(self.bg.width - self.size[0] - self.bg.spawnpoint[0], self.rect.centerx - (self.size[0] / 2)))
        self.rect.y = max(-self.bg.spawnpoint[1], min(self.bg.height - self.size[1] - self.bg.spawnpoint[1], self.rect.centery - (self.size[1] / 2)))

        self.update_abilities(offset)
        self.old_rect = self.rect.copy()
        self.event_key()
        self.direction(offset)
