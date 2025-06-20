'''This module contains the user interface management class for a game that handles various UI elements including health bars, level bars, and menu buttons.'''
import pygame as pg
import thorpy as tp

import data.constants as const
from classes.class_character import Character
from data.characters import CHARACTERS
from data.gui_data import IMG_BUTTON_TEXT_STYLE, MM_BUTTON_STYLES


class InitUI:
    '''
    A user interface management class for a game that handles various UI elements including health bars, level bars, and menu buttons.
    
    This class initializes and manages the game's user interface components such as:
    - Health bar display with visual styling
    - Level progression bar with text labels
    - Pause menu buttons (Resume, Exit to menu, Quit game)
    - Upgrade selection buttons with images and text
    
    The class sets up all UI elements with appropriate positioning, styling, and updaters for smooth animation.
    All UI elements are configured to work with a specified frame rate and are positioned relative to the screen dimensions.
    
    Args:
        screen (pg.Surface): The pygame Surface object representing the game screen.
                           Used for positioning UI elements and determining screen dimensions.
    
    Note:
        - Requires pygame and thorpy (tp) libraries to be properly imported
        - Depends on external constants (const.FPS, MM_BUTTON_STYLES, etc.)
        - All UI elements are locked by default to prevent user interaction during initialization
    '''
    def __init__(self, screen: pg.Surface):
        self.screen = screen

        self.health_bar = tp.Lifebar(
            "",
            length=self.screen.get_width() / 10 * 2,
            height=30,
            bck_color=(37, 190, 106),
            initial_value=100 / 100,
            auto_adapt_length=False
        )
        self.health_bar.set_locked(True)
        self.health_bar.e_frame.set_bck_color(pg.color.Color(32, 32, 32))
        self.health_bar.e_frame.set_style_attr("border_color", pg.color.Color(32, 32, 32))
        self.health_bar.move(self.screen.get_width() / 2, self.screen.get_height() - 35)
        self.health_bar_upd = self.health_bar.get_updater(const.FPS)

        self.lvl_bar = tp.Lifebar(
            "Lv. 0",
            length=self.screen.get_width() - 20,
            height=30,
            bck_color=(37, 150, 190),
            initial_value=0,
            auto_adapt_length=False,
            font_color="White"
        )
        self.lvl_bar.set_locked(True)
        self.lvl_bar.e_frame.set_bck_color(pg.color.Color(32, 32, 32))
        self.lvl_bar.e_frame.set_style_attr("border_color", pg.color.Color(32, 32, 32))
        self.lvl_bar.move(self.screen.get_width() / 2, 10)
        self.lvl_bar.life_text.move((self.screen.get_width() / 2) - 40, 0)
        self.lvl_bar_upd = self.lvl_bar.get_updater(const.FPS)

        self.resume = tp.Button("Resume", MM_BUTTON_STYLES['normal'], MM_BUTTON_STYLES['hover'], MM_BUTTON_STYLES['pressed'])
        self.exit_to_menu = tp.Button("Exit to menu", MM_BUTTON_STYLES['normal'], MM_BUTTON_STYLES['hover'], MM_BUTTON_STYLES['pressed'])
        self.quit = tp.Button("Quit game", MM_BUTTON_STYLES['normal'], MM_BUTTON_STYLES['hover'], MM_BUTTON_STYLES['pressed'])

        self.upgrade_btns = tp.Group([], gap = 10)
        for _ in range(6):
            self.upgrade_btns.add_child(
                tp.TextAndImageButton(
                    "Shuriken",
                    pg.transform.scale(pg.image.load(CHARACTERS["Protagonist"]["characterPreview"]), (64, 64)),
                    reverse=True,
                    styleNormal=MM_BUTTON_STYLES['normal'],
                    styleHover=MM_BUTTON_STYLES['hover'],
                    stylePressed=MM_BUTTON_STYLES['pressed'],
                    text_style=IMG_BUTTON_TEXT_STYLE
                    )
                )

        self.upgrade_btns_upd = self.upgrade_btns.get_updater(const.FPS)
        self.pause_menu_btns_upd = tp.Group([self.resume, self.exit_to_menu, self.quit], gap=10).get_updater(const.FPS)


class UI:
    """
    Manages the user interface elements for a game, including player status displays and interactive buttons.
    
    This class handles the main UI components such as health and level bars, pause menu functionality,
    and upgrade system buttons. It provides methods to update visual elements based on player state
    and manage button interactions with proper state changes and cursor management.
    
    Core functionality includes:
    - Health and level bar updates with dynamic visual feedback
    - Pause menu button management (resume, exit to menu, quit)
    - Upgrade button system with state handling
    - Mouse cursor state management for button interactions
    
    Args:
        screen (pg.Surface): The pygame surface to render UI elements on
        player (Character): The player character object containing stats like HP, level, experience
        ui (InitUI): Configuration object containing pre-initialized UI elements and updaters
    
    Note:
        - Button click handlers automatically manage cursor state changes
        - Health bar color dynamically interpolates from red (low) to green (full health)
        - All button elements must support the 'state' attribute for proper functionality
    """
    def __init__(self, screen: pg.Surface, player: Character, ui: InitUI):
        self.screen = screen
        self.player = player

        self.exit_to_menu = ui.exit_to_menu
        self.quit = ui.quit
        self.resume = ui.resume

        self.health_bar = ui.health_bar
        self.lvl_bar = ui.lvl_bar
        self.health_bar_upd = ui.health_bar_upd
        self.lvl_bar_upd = ui.lvl_bar_upd
        self.pause_menu_btns_upd = ui.pause_menu_btns_upd

        self.resume.at_unclick_params = {"button": self.resume}
        self.exit_to_menu.at_unclick = self.change_button_state
        self.exit_to_menu.at_unclick_params = {"button": self.exit_to_menu}
        self.quit.at_unclick = self.change_button_state
        self.quit.at_unclick_params = {"button": self.quit}

        self.upgrade_btns = ui.upgrade_btns
        for i in self.upgrade_btns.children:
            i.at_unclick = self.change_button_state
            i.at_unclick_params = {"button": i}
        self.upgrade_btns_upd = ui.upgrade_btns_upd

    def update(self) -> None:
        """
        Update the player's UI elements including health bar and level bar.
        
        This method updates the visual representation of the player's current status
        by refreshing the health bar value and color, level bar progress, and their
        associated updater components.
        
        The health bar color transitions from red (low health) to green (full health)
        based on the player's current HP ratio. The level bar shows experience
        progress towards the next level.
        """
        self.health_bar.set_value(self.player.hp / self.player.max_hp)
        self.health_bar.e_rect.set_bck_color(
            pg.color.Color.lerp(
                pg.color.Color(170, 35, 35),
                pg.color.Color(37, 190, 106),
                self.player.hp / self.player.max_hp
            )
        )

        self.lvl_bar.set_value(self.player.exp / self.player.exp_next)
        self.lvl_bar.life_text.set_text(f"Lv. {self.player.lvl}")

        self.health_bar_upd.update()
        self.lvl_bar_upd.update()

    def change_button_state(self, button: tp.elements.Element) -> None:
        """
        Change the button state to unclicked and reset the mouse cursor to default arrow.
        
        This method sets the provided button's state to "unclicked" and changes the
        mouse cursor back to the system default arrow cursor.
        
        Args:
            button (tp.elements.Element): The button element whose state needs to be changed.
                                        Must be a valid Element object with a 'state' attribute.
        """
        button.state = "unclicked"
        pg.mouse.set_cursor(pg.SYSTEM_CURSOR_ARROW)

    def update_pause_buttons(self) -> None:
        """
        Updates the pause menu buttons by calling the updater.
        
        This method triggers the update mechanism for all pause menu buttons,
        ensuring their visual state and functionality are refreshed according
        to the current game state.
        """
        self.pause_menu_btns_upd.update()

    def update_upgrade_btns(self) -> None:
        """
        Updates the upgrade buttons by calling the updater.
        
        This method triggers the update process for all upgrade buttons
        through the upgrade_btns_upd instance. It ensures that
        the upgrade buttons reflect the current state and availability
        of upgrades.
        """
        self.upgrade_btns_upd.update()
