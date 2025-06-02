import configparser as cfgp

import pygame as pg

import UI.classMainMenu as mm
from classes.classGame import Game
from data.Constants import PATHS
from UI.classGameScreen import GameScreen
from UI.GameUI import InitUI

cfg = cfgp.ConfigParser()
cfg.read('data/config.ini')

class GameHandler:
    """
    Main game handler that manages the overall game flow and menu system.
    
    This class serves as the central controller for the VampyGame application, handling
    the main game loop, menu navigation, and transitions between different game states.
    It coordinates interactions between the game screen, UI components, and various menus
    including the main menu, character selector, map selector, and settings.
    
    Core Functionality:
    - Main game loop execution and state management
    - Menu system navigation (main menu, character/map selection, settings)
    - Game initialization and cleanup
    - Music and audio management
    - Window caption and cursor management
    - Transition handling between menus and gameplay
    
    Args:
        screen (GameScreen): The game screen object for rendering
        ui (InitUI): The UI initialization object for interface management
    
    Note:
        - Requires pygame to be initialized before instantiation
        - Automatically loads and plays menu music on initialization
        - The main loop will continue until user quits or an error occurs
        - Music volume is controlled by configuration settings
    """
    def __init__(self, screen: GameScreen, ui: InitUI):
        self.screen = screen
        self.ui = ui
        self.main_menu = mm.MainMenu(self.screen)
        self.running = True
        self.screen.set_caption("VampyGame: Main Menu")
        pg.mixer.music.load(PATHS['Music']['Menu'])
        pg.mixer.music.set_volume(cfg.getint("Settings", "musicvolume") / 100)
        pg.mixer.music.play(-1)

    def mainloop(self) -> None:
        """
        Main game loop that handles menu navigation and game state management.
        
        This method runs the primary game loop, managing transitions between different menus
        (main menu, character selector, map selector) and handling game initialization and cleanup.
        The loop continues until the user quits the application or an exit condition is met.
        
        Menu Flow:
        - Main Menu -> Character Selector -> Map Selector -> Game
        - Settings Menu (accessible from Main Menu)
        - Proper cleanup and state management between transitions
        
        Game States Handled:
        - Menu navigation and selection
        - Character and map selection
        - Game initialization and execution
        - Settings configuration
        - Application exit conditions
        
        Side Effects:
            - Modifies self.running to control loop execution
            - Changes mouse cursor appearance
            - Manages menu state transitions
            - Handles music playback and volume
            - Creates and destroys game instances
            - Updates window caption
        """
        while self.running:
            returned = self.main_menu.run_current()
            if not returned[1]:
                self.running = False
                break

            if returned[0] == "Play":
                pg.mouse.set_cursor(pg.SYSTEM_CURSOR_ARROW)
                self.main_menu.change_menu(self.main_menu.char_selector_menu)

                while True:
                    char_selector_option = self.main_menu.run_current()

                    if char_selector_option[0] == "Back":
                        self.main_menu.change_menu(self.main_menu.menu)
                        break

                    if char_selector_option[0] not in ("QUIT", "Back"):
                        self.main_menu.change_menu(self.main_menu.map_selector_menu)
                        map_selector_option = self.main_menu.run_current()

                        if map_selector_option[0] == "Back":
                            self.main_menu.change_menu(self.main_menu.char_selector_menu)
                            continue

                        if map_selector_option[0] not in ("QUIT", "Back"):
                            pg.mouse.set_cursor(pg.SYSTEM_CURSOR_WAIT)
                            self.main_menu.change_menu(None)
                            self.screen.set_caption("VampyGame")
                            pg.mixer.music.stop()

                            self.game = Game(
                                self.screen.get_screen(),
                                PATHS['Maps'][map_selector_option[0]],
                                char_selector_option[0],
                                self.ui
                            )

                            pg.mouse.set_cursor(pg.SYSTEM_CURSOR_ARROW)
                            game_returned = self.game.run_game()

                            if game_returned == "QUIT":
                                break

                            if game_returned == "ToMenu":
                                del self.game
                                break

                if char_selector_option[0] == "Back":
                    continue

                if game_returned == "QUIT":
                    break

                if game_returned == "ToMenu":
                    self.main_menu.change_menu(self.main_menu.menu)
                    pg.mixer.music.load(PATHS['Music']['Menu'])
                    pg.mixer.music.set_volume(cfg.getint("Settings", "musicvolume") / 100)
                    pg.mixer.music.play(-1)
                    continue

            elif returned[0] == "Quit":
                self.running = False
                break

            elif returned[0] == "Settings":
                self.main_menu.change_menu(self.main_menu.settings_menu)
                settings_menu_returned = self.main_menu.run_current()

                if settings_menu_returned[0] == "Back":
                    self.main_menu.change_menu(self.main_menu.menu)
                    continue

                if not settings_menu_returned[1]:
                    self.running = False
                    break
