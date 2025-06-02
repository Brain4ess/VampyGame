import configparser as cfgp
from random import choice

import pygame as pg
from pygame.locals import *

import data.constants as const
from classes.class_background import BG
from classes.class_camera import Camera
from classes.class_character import Character
from classes.class_timer import Timer
from classes.enemy_handler import EnemyHandler
from data.active_abilities import ACTIVE_ABILITIES
from data.passive_abilities import PASSIVE_ABILITIES
from UI.game_screen import GameScreen
from UI.game_ui import UI, InitUI

cfg = cfgp.ConfigParser()
cfg.read('data/config.ini')

class Game:
    """
    Main game controller class that orchestrates all game components and mechanics.
    
    This class manages the complete game loop including player character, enemies, UI, 
    camera system, background rendering, and game state transitions. It handles core
    gameplay mechanics such as combat, level progression, pause functionality, death
    and revival system, and upgrade selection.
    
    Key Features:
    - Real-time gameplay with sprite-based character and enemy systems
    - Dynamic camera that follows the player
    - Level-up system with ability and passive upgrades
    - Pause/resume functionality with UI overlay
    - Death and revival mechanics with lives system
    - Timer-based gameplay progression
    - Music and sound management
    
    Args:
        screen (GameScreen): The main game screen/display surface
        map_image (str): Path to the background map image file
        character (str): Character type identifier for player initialization
        init_ui (InitUI): Initial UI configuration object
    
    Note:
        The game requires pygame to be initialized before instantiation.
        Proper cleanup is handled automatically through the destructor,
        but manual cleanup via attempt_suicide() may be needed in some cases.
    """
    def __init__(self, screen: GameScreen, map_image: str, character: str, init_ui: InitUI):
        self.map_image = map_image
        self.spr_group = pg.sprite.Group()
        self.enemy_group = pg.sprite.Group()
        self.fps = const.FPS
        self.screen = screen
        self.bg = BG(self.map_image, self.screen, spawnpoint=(500, 500))
        self.run = True
        self.timer = Timer(self.screen, const.PATHS["Fonts"]["Timer"], 'White', 30)
        self.camera = Camera(self.screen, self.bg.width, self.bg.height, self.bg)
        self.player = Character(
            self.bg,
            character,
            self.screen,
            5,
            self.spr_group,
            self.enemy_group,
            self.timer
        )
        self.__prev_plr_lvl = self.player.lvl
        self.clock = pg.time.Clock()
        self.timer.start()
        self.enemy_handler = EnemyHandler(
            self.screen,
            self.camera,
            self.player,
            self.timer,
            self.spr_group,
            self.enemy_group
        )
        self.ui = UI(self.screen, self.player, init_ui)
        self.ui.resume.at_unclick = self.toggle_pause
        self.paused = False
        self.chosen = True
        self.__escprev = 0

    def event_game(self) -> None:
        """
        Handle game events and key input processing.
        
        This method processes pygame events and handles key inputs for the game.
        It checks for quit events and escape key presses to toggle pause functionality.
        The escape key press is tracked to prevent continuous triggering while held down.
        
        Events handled:
        - QUIT: Sets self.run to False to exit the game
        - K_ESCAPE: Toggles pause state when pressed (not held)
        
        Side effects:
        - May modify self.run attribute
        - May call self.toggle_pause() method
        - Updates self.__escprev to track escape key state
        """
        for event in pg.event.get():
            if event.type == QUIT:
                self.run = False

        keys = pg.key.get_pressed()

        if keys[K_ESCAPE] and keys[K_ESCAPE] != self.__escprev:
            self.toggle_pause()

        self.__escprev = keys[K_ESCAPE]

    def toggle_pause(self, button = None) -> None:
        """
        Toggle the pause state of the game.
        
        This method handles pausing and unpausing the game, including managing
        the game state, music playback, and timer functionality. The game can
        only be paused/unpaused if a player is chosen and still alive.
        
        Args:
            button (optional): The button object that triggered this action.
                             If provided, its state will be reset to "unclicked".
                             Defaults to None.

        Side Effects:
            - Resets button state to "unclicked" if button is provided
            - Toggles self.paused flag between True and False
            - Pauses/unpauses pygame mixer music
            - Pauses/unpauses the game timer
            - Updates UI resume button text when pausing
        
        Note:
            The toggle operation only occurs if self.chosen is True and 
            self.player.hp > 0 (player is alive).
        """
        if button is not None:
            button.state = "unclicked"

        if self.paused and self.chosen and self.player.hp > 0:
            self.paused = False
            pg.mixer.music.unpause()
            self.timer.pause(self.paused)

        elif not self.paused and self.chosen and self.player.hp > 0:
            self.paused = True
            self.ui.resume.set_text("Resume")
            pg.mixer.music.pause()
            self.timer.pause(self.paused)

    def run_game(self):
        """
        Main game loop that handles the core gameplay mechanics.
        
        This method manages the primary game execution including music playback,
        event handling, entity updates, screen rendering, and game state transitions.
        The loop continues until the game is terminated or a state change occurs.
        
        Returns:
            str: Game state indicator such as "QUIT" when the game should terminate,
                 or other state strings returned from sub-loops (death screen, 
                 level up screen, pause screen).
        """
        pg.mixer.music.load(const.PATHS["Music"]["Game"])
        pg.mixer.music.set_volume(cfg.getint('Settings', 'musicvolume') / 100)
        pg.mixer.music.play(-1)
        while self.run:
            self.event_game()
            if not self.run:
                return "QUIT"
            self.bg.blit_bg(self.camera.getoffset())
            self.enemy_handler.update()
            self.player.update(self.camera.getoffset())

            # Death mechanic
            death_screen = self.death_screen_loop()
            if death_screen is not True:
                return death_screen

            lvl_up_loop = self.lvl_up_loop()
            if lvl_up_loop is not True:
                return lvl_up_loop

            self.ui.update()
            self.camera.update(self.player)
            self.timer.update()

            pg.display.update()
            self.clock.tick(self.fps)

            while self.paused:
                pause_loop = self.pause_loop()
                if pause_loop is not True:
                    return pause_loop

    def make_upgrades(self):
        """
        Generate upgrade options for the player by selecting from available abilities and passives.
        
        This method creates upgrade choices by:
        1. Collecting upgradeable active abilities (excluding mirrored ones)
        2. Adding random new abilities if player has less than 5 abilities
        3. Collecting upgradeable passive abilities
        4. Adding random new passives if player has less than 5 passives
        5. Randomly selecting up to 3 final upgrade options
        6. Updating the UI upgrade buttons with the selected options
        
        The method ensures that:
        - Mirrored abilities are excluded from upgrades
        - Players can upgrade existing abilities/passives or acquire new ones
        - A maximum of 3 upgrade options are presented
        - UI buttons are properly configured with icons and display names
        - Unused upgrade buttons are hidden
        
        Side Effects:
            - Modifies self.abilities_final list
            - Updates UI upgrade button visibility and content
            - Refreshes UI surfaces for proper display
        """
        # Active abilities
        upg_abilities = []
        for ability in self.player.abilities:
            if ability.level < ability.max_level and not 'mirrored' in ability.name:
                upg_abilities.append(ability.name)

        if len(self.player.abilities) < 5:
            all_abilities = list(ACTIVE_ABILITIES.keys()).copy()

            for ability in self.player.abilities:
                if not 'mirrored' in ability.name:
                    all_abilities.remove(ability.name)
            abilities_random = []

            for i in range(3):
                if len(all_abilities) > 0:
                    temp = choice(all_abilities)
                    all_abilities.remove(temp)
                    abilities_random.append(temp)
            abilities_final = upg_abilities + abilities_random

        else:
            abilities_final = upg_abilities

        # Passive abilities
        upg_passives = []
        for passive in self.player.passives:
            if passive.level < passive.max_level:
                upg_passives.append(passive.name)

        if len(self.player.passives) < 5:
            all_passives = list(PASSIVE_ABILITIES.keys()).copy()

            for passive in self.player.passives:
                all_passives.remove(passive.name)
            passives_random = []

            for i in range(3):
                if len(all_passives) > 0:
                    temp = choice(all_passives)
                    all_passives.remove(temp)
                    passives_random.append(temp)
            passives_final = upg_passives + passives_random

        else:
            passives_final = upg_passives

        final_choices = abilities_final + passives_final
        self.abilities_final = []
        for i in range(3):
            if len(final_choices) > 0:
                temp = choice(final_choices)
                final_choices.remove(temp)
                self.abilities_final.append(temp)

        if len(self.abilities_final) > 0:
            for i, ability in enumerate(self.abilities_final):
                self.ui.upgrade_btns.children[i].set_invisible(False, True)

                if ability in list(ACTIVE_ABILITIES.keys()):
                    self.ui.upgrade_btns.children[i].children[1].set_text(ACTIVE_ABILITIES[ability]['display_name'])
                    self.ui.upgrade_btns.children[i].children[0].img = pg.transform.scale(
                        pg.image.load(ACTIVE_ABILITIES[ability]['icon']), (64, 64)
                    )
                else:
                    self.ui.upgrade_btns.children[i].children[1].set_text(PASSIVE_ABILITIES[ability]['display_name'])
                    self.ui.upgrade_btns.children[i].children[0].img = pg.transform.scale(
                        pg.image.load(PASSIVE_ABILITIES[ability]['icon']), (64, 64)
                    )

                self.ui.upgrade_btns.children[i].children[1].refresh_surfaces_build()
                self.ui.upgrade_btns.children[i].children[0].refresh_surfaces_build()
                self.ui.upgrade_btns.children[i].refresh_surfaces_build()

            if len(self.abilities_final) < len(self.ui.upgrade_btns.children):
                for i in range(len(self.abilities_final), len(self.ui.upgrade_btns.children)):
                    self.ui.upgrade_btns.children[i].set_invisible(True, True)

    def pause_loop(self) :
        """
        Handle the pause loop functionality during game pause state.
        
        This method manages the game's pause state by handling events, updating UI elements,
        and processing user interactions with pause menu buttons. It continues to run while
        the game is paused and returns different values based on user actions.
        
        Returns:
            str or bool: Returns one of the following:
                - "ToMenu": If the exit to menu button is clicked
                - "QUIT": If the quit button is clicked or the game should stop running
                - True: If the pause loop should continue running
        
        Side Effects:
            - Calls self.event_game() to handle game events
            - Updates pause button states via self.ui.update_pause_buttons()
            - May call self.attempt_suicide() when exiting to menu
            - Updates the display and maintains frame rate
        """
        self.event_game()
        self.ui.update_pause_buttons()

        if self.ui.exit_to_menu.state == "unclicked":
            self.ui.resume.at_unclick = None
            self.attempt_suicide()
            return "ToMenu"

        if self.ui.quit.state == "unclicked":
            return "QUIT"

        if not self.run:
            return "QUIT"

        pg.display.update()
        self.clock.tick(self.fps)
        return True

    def death_screen_loop(self):
        """
        Handle the death screen loop when player's HP reaches zero.
        
        This method manages the game state when the player dies, displaying revival options
        and handling user interactions on the death screen. It pauses the game timer and
        enters a loop that continues until the player makes a decision (revive, exit to menu,
        or quit the game).
        
        Returns:
            str or bool: Returns "ToMenu" if player chooses to exit to menu,
                        "QUIT" if player chooses to quit the game or closes the window,
                        True if player successfully revives and continues playing.
        
        Behavior:
            - Only activates when player's HP is <= 0
            - Updates the resume button text to show remaining lives
            - Pauses the game timer during the death screen
            - Allows player to revive if they have lives remaining
            - Restores player to full HP and decreases lives count upon revival
            - Handles exit to menu and quit game options
            - Maintains game loop with event handling and display updates
        """
        if self.player.hp <= 0:
            self.ui.resume.set_text(f'Revive (left: {self.player.lives})')
            self.timer.pause(True)
            while True:
                self.event_game()
                self.ui.update_pause_buttons()
                if self.ui.resume.state == "unclicked":
                    if self.player.lives > 0:
                        self.player.hp = self.player.max_hp
                        self.player.lives -= 1
                        self.timer.pause(False)
                        break
                if self.ui.exit_to_menu.state == "unclicked":
                    self.ui.resume.at_unclick = None
                    self.attempt_suicide()
                    return "ToMenu"
                if self.ui.quit.state == "unclicked":
                    return "QUIT"
                if not self.run:
                    return "QUIT"
                pg.display.update()
                self.clock.tick(self.fps)
        return True

    def lvl_up_loop(self):
        """
        Handle the level up process for the player character.
        
        This method manages the entire level up sequence including:
        - Detecting when the player has leveled up
        - Generating available upgrades
        - Pausing the game timer during upgrade selection
        - Processing the player's upgrade choice (abilities or passives)
        - Managing interactions between passives and abilities
        
        The method runs a loop that continues until an upgrade is chosen or the game is quit.
        When an upgrade is selected, it either:
        - Levels up an existing ability/passive or adds a new one
        - Triggers appropriate callbacks for passive interactions
        
        Returns:
            str: "QUIT" if the game run loop should be terminated
            bool: True if the level up process completed successfully
        """
        if self.player.lvl > self.__prev_plr_lvl:
            self.__prev_plr_lvl = self.player.lvl
            self.make_upgrades()
            if len(self.abilities_final) > 0:
                self.chosen = False
                self.timer.pause(not self.chosen)
                while not self.chosen:
                    self.event_game()
                    self.ui.update_upgrade_btns()
                    for i, btn in enumerate(self.ui.upgrade_btns.children):
                        if btn.state == "unclicked":
                            if '[•]' in btn.children[1].text:
                                if self.player.get_passive(self.abilities_final[i]) is not None:
                                    self.player.get_passive(self.abilities_final[i]).on_level_up()

                                else:
                                    self.player.add_passive(self.abilities_final[i])
                                    if len(self.player.passives) > 1:
                                        for i in range(len(self.player.passives) - 1):
                                            self.player.passives[i].on_passive_add(self.player.passives[-1])

                            else:
                                if self.player.get_ability(self.abilities_final[i]) is not None:
                                    self.player.get_ability(self.abilities_final[i]).level += 1

                                else:
                                    self.player.add_ability(self.abilities_final[i])
                                    if len(self.player.passives) > 0:
                                        for i, passive in enumerate(self.player.passives):
                                            passive.on_ability_add(self.player.abilities[-1])

                            self.timer.pause(self.chosen)
                            self.chosen = True
                            break

                    if not self.run:
                        return "QUIT"

                    pg.display.update()
                    self.clock.tick(self.fps)
        return True

    def attempt_suicide(self) -> None:
        """
        Performs cleanup operations to terminate the current game instance.
        
        This method removes all game objects and clears references to prevent
        memory leaks when the game instance needs to be destroyed. It deletes
        background resources, removes UI event handlers, and empties sprite groups.
        
        Operations performed:
        - Deletes background image and map resources
        - Removes UI button click event handlers (resume, exit_to_menu, quit)
        - Empties all sprite groups (spr_group, enemy_group)

        Note:
            This is a cleanup method that should be called when terminating
            the game to ensure proper resource deallocation.
        """
        del self.bg.bg
        del self.bg.map_image
        self.ui.resume.at_unclick = None
        self.ui.exit_to_menu.at_unclick = None
        self.ui.quit.at_unclick = None
        self.spr_group.empty()
        self.enemy_group.empty()

    def __del__(self) -> None:
        """
        Destructor method for cleaning up game resources.
        
        This method is called when the object is being garbage collected.
        It systematically deletes all game components and their associated
        resources to prevent memory leaks and ensure proper cleanup.
        
        The cleanup process includes:
        - Camera and player background resources
        - Player and enemy handler timers
        - Player abilities and their associated timers and player references
        - Game background and map images
        - Core game objects (player, timer, camera, enemy handler)
        - UI components (level bar, health bar, buttons, and their update handlers)
        
        Note:
            This method should be called automatically by Python's garbage collector.
            Manual calls are generally not recommended unless explicitly needed
            for immediate resource cleanup.
        """
        del self.camera.bg
        del self.player.bg
        del self.player.timer
        del self.enemy_handler.timer
        for i in self.player.abilities:
            del i.timer
            del i.player
        del self.enemy_handler.camera
        del self.bg
        del self.map_image
        del self.player
        del self.timer
        del self.camera
        del self.enemy_handler
        del self.ui.lvl_bar
        del self.ui.health_bar
        del self.ui.health_bar_upd
        del self.ui.lvl_bar_upd
        del self.ui.resume
        del self.ui.exit_to_menu
        del self.ui.quit
        del self.ui
