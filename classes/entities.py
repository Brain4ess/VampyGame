'''This module contains the Enemy class for the game. It handles the enemy's movement, collision detection, and damage dealing.'''
import configparser as cfgp
import datetime as dt
from math import sqrt
from os import listdir
from random import choice as random_choice
from random import randint as random_randint

import pygame as pg


class Enemy(pg.sprite.Sprite):
    """
    A game enemy sprite that automatically follows and attacks the player.
    
    This class represents an enemy character in a 2D game that spawns at the screen edges,
    moves towards the player, handles collisions, and deals damage on contact. The enemy
    features animated sprites with directional facing, sound effects, and health management.
    
    Core Features:
    - Automatic pathfinding and movement towards player
    - Animated sprite rendering with left/right directional facing
    - Collision detection and damage dealing system
    - Health management with damage cooldown periods
    - Sound effect playback with volume control
    - Random spawn positioning at screen edges
    
    Args:
        screen (pg.Surface): The game screen surface for rendering
        enemy (dict): Enemy configuration dictionary containing:
            - 'sprites' (str): Path to sprite image directory
            - 'image_multiplier' (float): Scale factor for sprite images
            - 'speed' (float): Movement speed in pixels per frame
            - 'health' (int): Initial health points
            - 'exp' (int): Experience points awarded when defeated
            - 'damage' (int): Damage dealt to player on contact
            - 'sound' (str, optional): Path to damage sound effect file
        player: Player object with rect and hp attributes
        camera: Camera object with camera attribute containing x,y coordinates
        group (pg.sprite.Group): Main sprite group for collision detection
        enemy_group (pg.sprite.Group): Specific enemy sprite group
    
    Note:
        - Requires sprite images numbered sequentially (1.png, 2.png, etc.)
        - Sound volume is controlled by 'sfxvolume' setting in data/config.ini
        - Enemies spawn just outside the visible screen area
        - Damage has a 200ms cooldown period to prevent rapid health loss
    """
    def __init__(self,
                 screen: pg.Surface,
                 enemy: dict,
                 player,
                 camera,
                 group: pg.sprite.Group,
                 enemy_group: pg.sprite.Group
    ) -> None:
        super().__init__(group, enemy_group)
        self.screen = screen
        self.spr_right = []
        self.spr_left = []
        self.spr_create(enemy)
        self.curr_spr = 0
        self.rect = self.spr_right[0].get_rect()
        self.speed = enemy['speed']
        self.hp = enemy['health']
        self.exp = enemy['exp']
        self.damage = enemy['damage']
        self.sound = enemy['sound']
        if self.sound is not None:
            cfg = cfgp.ConfigParser()
            cfg.read('data/config.ini')
            self.sound_player = pg.mixer.Sound(self.sound)
            self.sound_player.set_volume(cfg.getint('Settings', 'sfxvolume') / 100)

        self.player_position = player.rect
        self.player = player

        self.old_rect = self.rect.copy()
        self.last_damaged = dt.datetime.now()

        self.spawn_list_x = [camera.camera.x + (self.screen.get_width()) + (64 * 2), camera.camera.x - (64 * 2)]
        self.spawn_list_y = [camera.camera.y + (self.screen.get_height()) + (64 * 2), camera.camera.y - (64 * 2)]

        temp_choice = random_choice(["h", "v"])
        
        if temp_choice == "h":
            self.rect.x = random_randint(self.spawn_list_x[1], self.spawn_list_x[0])
            self.rect.y = random_choice(self.spawn_list_y)
        
        elif temp_choice == "v":
            self.rect.x = random_choice(self.spawn_list_x)
            self.rect.y = random_randint(self.spawn_list_y[1], self.spawn_list_y[0])

    def follow(self, offset: pg.math.Vector2, dist_x) -> None:
        """
        Render the character sprite following the camera offset and handle sprite animation.
        
        This method blits the appropriate sprite (left or right facing) to the screen
        based on the movement direction and updates the current sprite frame for animation.
        
        Args:
            offset (pg.math.Vector2): Camera offset vector used to adjust the sprite position
                                     relative to the screen coordinates.
            dist_x: Direction of movement. If negative, character faces left; otherwise faces right.
            
        Note:
            - Uses self.spr_left for leftward movement (dist_x < 0)
            - Uses self.spr_right for rightward movement (dist_x >= 0)
            - Automatically cycles through sprite frames at 0.2 increment per call
            - Resets to frame 0 when reaching the end of the sprite sequence
        """
        if dist_x < 0:
            self.screen.blit(self.spr_left[int(self.curr_spr)], self.rect.topleft - offset)
        else:
            self.screen.blit(self.spr_right[int(self.curr_spr)], self.rect.topleft - offset)

        if self.curr_spr >= len(self.spr_right) - 1:
            self.curr_spr = 0
        else:
            self.curr_spr += 0.2

    def spr_create(self, enemy: dict) -> None:
        """
        Create and load sprite images for an enemy character.
        
        This method loads all sprite images from the enemy's sprite directory,
        scales them according to the specified multiplier, and creates both
        right-facing and left-facing versions of each sprite.
        
        Args:
            enemy (dict): A dictionary containing enemy configuration with the following keys:
                - 'sprites' (str): Path to the directory containing sprite images
                - 'image_multiplier' (float): Scale factor for resizing the sprites
        
        Note:
            - Sprite files should be named sequentially (1.png, 2.png, etc.)
            - Right-facing sprites are stored in self.spr_right list
            - Left-facing sprites (horizontally flipped) are stored in self.spr_left list
        """
        for i in range(len(listdir(enemy['sprites']))):
            self.spr_right.append(
                pg.transform.scale_by(
                    pg.image.load(f'{enemy['sprites']}/{i+1}.png'), enemy["image_multiplier"]
                )
            )

            self.spr_left.append(
                pg.transform.flip(
                    self.spr_right[i], True, False
                )
            )

    def collision(self, direction, group: pg.sprite.Group) -> None:
        """
        Handle collision detection and response for the sprite.
        
        This method detects collisions with sprites in the given group and handles
        both damage calculation and position correction based on collision direction.
        
        Args:
            direction (str): The direction of movement being checked.
                           "h" for horizontal movement, "v" for vertical movement.
            group (pg.sprite.Group): The sprite group to check collisions against.
        
        Returns:
            None
        
        Note:
            - For horizontal collisions, damage is applied between compatible sprite types
            - Position correction prevents sprites from overlapping
            - Damage has a cooldown period of 200 milliseconds
            - Sound effects are played when damage is taken (if sound is available)
        """
        collisions = pg.sprite.spritecollide(self, group, False)
        if collisions:
            if direction == "h":
                for sprite in collisions:
                    if sprite.__class__.__name__ not in ("Enemy", "Character"):
                        if (self.last_damaged + dt.timedelta(milliseconds=200)) < dt.datetime.now():
                            self.hp -= sprite.damage
                            self.last_damaged = dt.datetime.now()

                            if self.sound is not None:
                                self.sound_player.stop()
                                self.sound_player.play()

                            if sprite.damageable:
                                sprite.hp -= self.damage

                    if self.rect.right >= sprite.rect.left and self.old_rect.right <= sprite.old_rect.left:
                        self.rect.right = sprite.rect.left

                    elif self.rect.left <= sprite.rect.right and self.old_rect.left >= sprite.old_rect.right:
                        self.rect.left = sprite.rect.right

            if direction == "v":
                for sprite in collisions:
                    if self.rect.bottom >= sprite.rect.top and self.old_rect.bottom <= sprite.old_rect.top:
                        self.rect.bottom = sprite.rect.top

                    elif self.rect.top <= sprite.rect.bottom and self.old_rect.top >= sprite.old_rect.bottom:
                        self.rect.top = sprite.rect.bottom

    def update(self, offset: pg.math.Vector2, group: pg.sprite.Group) -> None:
        """
        Update the enemy's position and handle collision detection with player.
        
        This method moves the enemy towards the player position, handles collisions
        with other sprites in the group, and manages damage dealing to the player.
        
        Args:
            offset (pg.math.Vector2): The camera offset for rendering adjustments
            group (pg.sprite.Group): The sprite group containing other game objects
                                   for collision detection
        
        The method performs the following operations:
        1. Creates a temporary copy of the sprite group excluding this enemy
        2. Calculates movement direction towards the player
        3. Moves the enemy if distance exceeds a threshold
        4. Handles horizontal and vertical collision detection
        5. Applies damage to player on collision
        6. Updates enemy's visual following behavior
        """
        temp_group = group.copy()
        temp_group.remove(self)
        
        self.old_rect = self.rect.copy()
        dist_x = self.player_position.x - self.rect.x
        dist_y = self.player_position.y - self.rect.y
        distance = sqrt(dist_x ** 2 + dist_y ** 2)
        
        if distance > self.spr_right[0].get_size()[0] / 1.5:
            dist_x = dist_x / distance * self.speed
            dist_y = dist_y / distance * self.speed
            self.rect.x += dist_x
            self.collision("h", temp_group)
            self.rect.y += dist_y
            self.collision("v", temp_group)
        
        temp_group.empty()
        del temp_group

        if self.rect.colliderect(self.player.rect) and self.player.hp >= self.damage:
            self.player.hp -= self.damage
        
        if self.rect.colliderect(self.player.rect) and self.player.hp < self.damage and self.player.hp > 0:
            self.player.hp = 0

        self.follow(offset, dist_x)

class Projectile(pg.sprite.Sprite):
    """
    A game projectile sprite that moves toward a target with animation and damage capabilities.
    
    This class represents a projectile fired by a player that can move toward a specific target,
    display animated sprites, and optionally deal damage or be destroyed. The projectile supports
    both direct targeting and enemy-following behavior.
    
    Key Features:
    - Animated sprite rendering with automatic cycling
    - Movement toward target with configurable speed
    - Optional damage and health system for destructible projectiles
    - Camera offset support for scrolling game worlds
    - Flexible targeting system (fixed position or enemy following)
    
    Args:
        screen (pg.Surface): The game screen surface to render the projectile on
        ability (dict): Dictionary containing projectile stats like 'speed', 'damage', and optionally 'hp'
        sprites (list[pg.Surface]): List of sprite surfaces for animation frames
        player: The player object that fired this projectile (used for initial positioning)
        group (pg.sprite.Group): Sprite group to add this projectile to
        fired_at: Timestamp or frame when the projectile was fired
        target (pg.Rect, optional): Target rectangle to move toward. Defaults to None
        damagable (bool, optional): Whether this projectile can take damage. Defaults to False
        follow_enemy (bool, optional): If False, adjusts target position for extended range. Defaults to False
    
    Note:
        - When follow_enemy=False, the target position is extended beyond the actual target
          for increased range
        - The projectile starts at the player's center position
        - Animation cycles through all provided sprites automatically
    """
    def __init__(self,
                 screen: pg.Surface,
                 ability: dict,
                 sprites: list[pg.Surface],
                 player,
                 group: pg.sprite.Group,
                 fired_at,
                 target: pg.Rect = None,
                 damagable: bool = False,
                 follow_enemy: bool = False
    ) -> None:
        super().__init__(group)
        self.screen = screen
        self.player = player
        self.ability = ability
        self.speed = ability["speed"]
        self.damage = ability["damage"]
        self.sprites = sprites
        self.fired_at = fired_at
        self.target = target
        self.damageable = damagable
        if self.damageable:
            self.hp = ability["hp"]
        self.is_alive = True
        self.rect = self.sprites[0].get_rect(center=self.player.rect.center)
        self.old_rect = self.rect.copy()
        self.curr_spr = 0
        self.distance = 0
        if not follow_enemy:
            target.x -= (self.player.rect.x - target.x) * 10
            target.y -= (self.player.rect.y - target.y) * 10

    def follow(self, offset: pg.math.Vector2) -> None:
        """
        Render the sprite at a position adjusted by the given offset.
        
        This method calculates the sprite's position relative to the camera offset
        and blits the current sprite to the screen at that adjusted position.
        
        Args:
            offset (pg.math.Vector2): The camera offset vector used to adjust
                                    the sprite's rendering position. This is
                                    typically the camera's position in world space.
        
        Note:
            - Uses the current sprite from self.sprites[self.curr_spr]
            - The offset is subtracted from the sprite's topleft position to
              create the screen-relative position
        """
        offset_pos = self.rect.topleft - offset
        self.screen.blit(self.sprites[self.curr_spr], offset_pos)

    def update(self, offset: pg.math.Vector2) -> None:
        """
        Update the entity's position and sprite animation.
        
        This method handles the entity's movement towards a target, updates the current
        sprite for animation, and applies camera offset following. The entity moves at
        a constant speed towards the target position using normalized direction vectors.
        
        Args:
            offset (pg.math.Vector2): Camera offset vector used for screen positioning
            
        Note:
            - Cycles through available sprites for animation
            - Calculates distance and direction to target
            - Moves entity towards target at specified speed
            - Updates sprite rectangle positioning
        """
        self.old_rect = self.rect.copy()
        if self.curr_spr >= len(self.sprites):
            self.curr_spr = 0

        self.rect = self.sprites[self.curr_spr].get_rect(center=self.rect.center)

        dist_x = self.target.x - self.rect.x
        dist_y = self.target.y - self.rect.y
        self.distance = sqrt(dist_x ** 2 + dist_y ** 2)
        if self.distance > 0:
            dist_x = dist_x / self.distance * self.speed
            dist_y = dist_y / self.distance * self.speed
            self.rect.x += dist_x
            self.rect.y += dist_y
        self.follow(offset)
        self.curr_spr += 1
