import datetime as dt
import random

import pygame as pg

from classes.classCamera import Camera
from classes.classCharacter import Character
from classes.classTimer import Timer
from classes.Entities import Enemy
from data.Enemies import ENEMIES


class EnemyHandler:
    """
    Manages enemy spawning, updating, and lifecycle in the game.
    
    This class handles all aspects of enemy management including spawning new enemies
    based on time intervals, updating enemy states, processing enemy deaths with
    experience rewards, and maintaining enemy groups for collision detection and rendering.
    
    Core functionality:
    - Automatic enemy spawning with weighted random selection
    - Enemy lifecycle management (spawn, update, death)
    - Experience point calculation and distribution to player
    - Time-based enemy count scaling and spawn rate control
    - Integration with camera system and sprite groups
    
    Args:
        screen (pg.Surface): The pygame surface for rendering enemies
        camera (Camera): Camera object for handling viewport offsets
        player (Character): Player character for targeting and experience distribution
        timer (Timer): Game timer for time-based mechanics and scaling
        group (pg.sprite.Group): Main sprite group for rendering all game objects
        enemy_group (pg.sprite.Group): Dedicated sprite group for enemy collision detection
    
    Note:
        - Enemy spawn rate is limited to one every 100ms
        - Enemy count scales with game time (10 * (minutes + 1))
        - Requires ENEMIES dictionary with enemy configurations and weights
        - Experience gain scales with time and player's exp_gain modifier
    """
    def __init__(self,
                 screen: pg.Surface,
                 camera: Camera,
                 player: Character,
                 timer: Timer,
                 spr_group: pg.sprite.Group,
                 enemy_group: pg.sprite.Group
    ):
        self.enemies = []
        self.enemy_group = enemy_group
        self.enemy_speed = 1
        self.screen = screen
        self.camera = camera
        self.player = player
        self.timer = timer
        self.spr_group = spr_group
        self.lastwave = dt.datetime.now()

    def spawn_in(self, enemy: str) -> None:
        """
        Spawn an enemy into the game world.
        
        Creates a new Enemy instance and adds it to the enemies list, then updates
        the timestamp of the last wave spawn.
        
        Args:
            enemy (str): The type or identifier of the enemy to spawn.
        
        Side Effects:
            - Adds a new Enemy object to self.enemies list
            - Updates self.lastwave with current datetime
        """
        self.enemies.append(
            Enemy(self.screen, enemy, self.player, self.camera, self.spr_group, self.enemy_group)
        )
        self.lastwave = dt.datetime.now()

    def update(self) -> None:
        """
        Update the enemy management system.
        
        This method handles the core enemy lifecycle including:
        - Updating all active enemies with camera offset and sprite group
        - Processing enemy death and experience gain calculation
        - Removing defeated enemies from all relevant groups
        - Spawning new enemies based on time intervals and current enemy count
        
        The method performs the following operations:
        1. Updates each enemy's state and checks for defeated enemies (hp <= 0)
        2. Awards experience points to the player based on enemy exp value,
           current time multiplier, and player's exp gain modifier
        3. Removes defeated enemies from enemies list, sprite group, and enemy group
        4. Spawns new enemies if conditions are met:
           - At least 100ms have passed since last wave
           - Current enemy count is below the time-based limit (10 * (minutes + 1))
        
        Experience calculation formula:
        player_exp += enemy_exp * time_multiplier * player_exp_gain_modifier
        where time_multiplier = (seconds // 60) + 1
        
        Enemy spawning uses weighted random selection from the ENEMIES dictionary.
        """
        enemies_to_delete = []
        if len(self.enemies) > 0:
            for enemy in self.enemies:
                enemy.update(self.camera.getoffset(), self.spr_group)
                if enemy.hp <= 0:
                    enemies_to_delete.append(enemy)
                    self.player.exp += (enemy.exp * ((self.timer.time.seconds // 60) + 1)) * self.player.exp_gain

        for enemy in enemies_to_delete:
            del self.enemies[self.enemies.index(enemy)]
            self.spr_group.remove(enemy)
            self.enemy_group.remove(enemy)
            del enemies_to_delete[enemies_to_delete.index(enemy)]

        if (dt.datetime.now() - self.lastwave > dt.timedelta(milliseconds=100)
            and len(self.enemies) < 10 * ((self.timer.time.seconds // 60) + 1)
        ):
            self.spawn_in(
                ENEMIES[
                    random.choices(list(ENEMIES.keys()), weights=[ENEMIES[enemy]['weight'] for enemy in list(ENEMIES.keys())])[0]
                ]
            )
