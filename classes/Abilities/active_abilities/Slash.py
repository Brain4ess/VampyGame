import pygame as pg

from functions.load_images_from_dir import load_images_from_dir

from ..class_active_ability import ActiveAbility


# Slash attack that pushes enemies around, also increases the number of slashes depending on the passive ability 'Duplicator' pumping
class Slash(ActiveAbility, pg.sprite.Sprite):
    """
    A projectile ability that creates animated slash attacks around the player.
    
    The Slash ability fires animated projectile attacks in bursts that alternate between
    left and right directions. Each slash consists of multiple animated sprites with
    different colors that cycle through during the attack sequence. The slashes follow
    the player's movement and have damage scaling based on ability level.
    
    Core functionality:
    - Fires projectiles in timed bursts with cooldown periods
    - Alternates firing direction (left/right) halfway through each burst
    - Animated sprites with color cycling and vertical flipping effects
    - Damage scaling based on ability level
    - Position tracking that follows player movement
    
    Constructor Parameters:
        Inherits from Ability class, which typically requires:
        - player: The player character this ability belongs to
        - ability: Dictionary containing ability configuration (damage, sprites, etc.)
        - Various sprite groups for collision detection and rendering
        - Timer object for cooldown management
    
    Notes:
        - Requires sprite images organized in directories specified in ability['sprites']
        - Projectiles are automatically destroyed after completing their burst sequence
        - The ability respects cooldown periods and enemy group presence for activation
    """
    def __post__init__(self):
        self.right_sprites = []
        self.left_sprites = []
        for value in self.ability['sprites'].values():
            right, left = load_images_from_dir(value, -90, True, True)
            self.right_sprites.append(right)
            self.left_sprites.append(left)

        self.curr_spr = 0
        self.direction = 'right'
        self.curr_color = 0
        self.times_fired = 0
        self.projectile_addition = 1
        self.damage = self.ability["damage"]
        self.damageable = False
        self.old_rect = self.right_sprites[0][0].get_rect(center=self.player.rect.center)
        pg.sprite.Sprite.__init__(self, self.group)

    def update(self, offset) -> None:
        """
        Update the projectile's state, animation, and position.
        
        This method handles the projectile's lifecycle including damage calculation,
        sprite animation, firing timing, direction changes, and position updates.
        The projectile fires in bursts and alternates direction halfway through each burst.
        
        Args:
            offset: Position offset for rendering/positioning calculations
            
        Side Effects:
            - Updates damage based on current level
            - Manages sprite animation and color cycling
            - Controls firing timing and cooldown
            - Handles projectile lifecycle (creation/destruction)
            - Updates position and follows player movement
            - Alternates firing direction during burst sequence
        """
        self.damage = self.ability["damage"] * (self.level)
        if self.curr_spr >= len(self.right_sprites[0]):
            self.old_rect = self.rect.copy()
            self.curr_spr = 0
            self.times_fired += 1
            self.curr_color += 1

        if self.curr_color >= len(self.right_sprites):
            self.curr_color = 0
            
        if self.times_fired == self.projectile_addition:
            self.kill()
        
        if (self.timer.time - self.lastfired).seconds >= self.cooldown - ((self.level - 1) / 1.45) and self.enemy_group:
            self.add(self.group)
            self.lastfired = self.timer.time
            self.direction = self.player.side
            self.times_fired = 0
            self.curr_color = 0
            self.old_rect = self.right_sprites[0][0].get_rect(center=self.player.rect.center)

        if self.curr_color < len(self.right_sprites) and self.times_fired < self.projectile_addition:
            self.old_rect.x += self.player.rect.x - self.player.old_rect.x
            
            if self.times_fired == self.projectile_addition // 2 and self.curr_spr == 0:
                self.old_rect = self.right_sprites[0][0].get_rect(center=self.player.rect.center)
                if self.direction == 'right':
                    self.direction = 'left'
                else:
                    self.direction = 'right'
            
            if self.direction == 'right':
                self.rect = self.right_sprites[self.curr_color][int(self.curr_spr)].get_rect(center=self.player.rect.center, left=self.old_rect.right)
            else:
                self.rect = self.left_sprites[self.curr_color][int(self.curr_spr)].get_rect(center=self.player.rect.center, right=self.old_rect.left)
            
            self.follow(offset, self.direction)
            self.curr_spr += 0.4 + (self.level / 10) - 0.1

    def follow(self, offset: pg.math.Vector2, dir_: str = "right") -> None:
        """
        Render the sprite at a position offset from its current location.
        
        This method draws the sprite on the screen at a calculated position based on
        the provided offset. The sprite can be flipped vertically depending on the
        number of times it has been fired, and uses different sprite sets based on
        the specified direction.
        
        Args:
            offset (pg.math.Vector2): The offset vector to subtract from the sprite's
                                    current top-left position to determine the render position.
            dir_ (str, optional): The direction the sprite is facing. Can be "right" or
                                any other value for left direction. Defaults to "right".
        
        Note:
            - The sprite is vertically flipped when times_fired is even
            - Uses right_sprites when dir_ is "right", otherwise uses left_sprites
            - The current sprite frame is determined by curr_spr and curr_color
        """
        offset_pos = self.rect.topleft - offset

        if dir_ == "right":
            if self.times_fired % 2 == 0:
                self.screen.blit(pg.transform.flip(self.right_sprites[self.curr_color][int(self.curr_spr)], False, True), offset_pos)
            else:
                self.screen.blit(self.right_sprites[self.curr_color][int(self.curr_spr)], offset_pos)

        else:
            if self.times_fired % 2 == 0:
                self.screen.blit(pg.transform.flip(self.left_sprites[self.curr_color][int(self.curr_spr)], False, True), offset_pos)
            else:
                self.screen.blit(self.left_sprites[self.curr_color][int(self.curr_spr)], offset_pos)
