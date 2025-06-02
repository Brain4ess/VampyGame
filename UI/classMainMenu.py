import configparser as cfgp

import pygame as pg
import thorpy as tp
from pygame.image import load
from pygame.transform import scale

import data.Constants as const
from classes.classBackground import BG
from data.Characters import CHARACTERS
from data.GuiData import (IMG_BUTTON_TEXT_STYLE, MM_BUTTON_STYLES,
                          SM_BUTTON_STYLES)
from UI.classGameScreen import GameScreen

cfg = cfgp.ConfigParser()
cfg.read('data/config.ini')

class Menu:
    """
    A game menu interface that manages screen display, background, and interactive elements.
    
    This class provides a framework for creating game menus with customizable backgrounds,
    interactive elements, and update loops. It handles the basic menu lifecycle including
    initialization, element management, and screen rendering.
    
    Core functionality:
    - Background image management with automatic screen filling
    - Element collection management for UI components
    - Update loop system for dynamic elements
    - Screen and caption management
    - FPS control for smooth rendering
    
    Args:
        screen (GameScreen): The game screen object to render the menu on
        background_image (str): Path to the background image file
        elements_upd (list[tp.loops.Loop], optional): List of update loops for dynamic behavior
        elements (list[tp.elements.Element], optional): List of UI elements to display
        caption (str, optional): Menu title or caption text
    
    Note:
        - The background image will be automatically scaled to fill the entire screen
        - The menu starts in a running state by default
        - FPS is set from global constants and may affect performance
    """
    def __init__(self, screen: GameScreen, background_image: str,
                 elements_upd: list[tp.loops.Loop] = None,
                 elements: list[tp.elements.Element] = None, caption: str = ""):
        self.screen = screen
        self.elements_upd = elements_upd
        self.elements = elements
        self.caption = caption
        self.fps = const.FPS
        self.background_image = background_image
        self.bg = BG(self.background_image, self.screen.get_screen(), fill=True)
        self.running = True


class MainMenu:
    """
    A comprehensive menu system for managing the main game interface and user interactions.
    
    This class handles the complete menu navigation system including the main menu,
    settings menu, character selector, and map selector. It provides a unified interface
    for managing game configuration, user preferences, and game initialization options.
    
    Core Functionality:
    - Main menu with Play, Settings, and Quit options
    - Settings menu with audio controls, resolution selection, and fullscreen toggle
    - Character selection with visual previews
    - Map selection with thumbnail previews
    - Configuration persistence to file system
    - Button state management and event handling
    
    Args:
        screen (GameScreen): The game screen object used for rendering all menu elements.
                           Must be initialized before creating the MainMenu instance.
    
    Note:
        - Requires pygame to be initialized before instantiation
        - Depends on configuration files and asset paths defined in const module
        - Button click sounds are automatically configured based on user settings
        - All menu elements are positioned dynamically based on screen dimensions
    """
    def __init__(self, screen: GameScreen):
        self.screen = screen
        self.fps = const.FPS
        self.clock = pg.time.Clock()
        self.fonts = const.PATHS['Fonts']['mainMenu']
        self.btn_click_sound = pg.mixer.Sound(file=const.PATHS['SFX']['buttonClick1'])
        self.btn_click_sound.set_volume(cfg.getint('Settings', 'sfxvolume') / 100)
        tp.Button.default_at_unclick = self.btn_click_sound.play
        self.__prev_menu: Menu
        self.__post_init__()

    def __post_init__(self):
        self.play_button = tp.Button("Play", MM_BUTTON_STYLES['normal'], MM_BUTTON_STYLES['hover'], MM_BUTTON_STYLES['pressed'])
        self.settings_button = tp.Button("Settings", MM_BUTTON_STYLES['normal'], MM_BUTTON_STYLES['hover'], MM_BUTTON_STYLES['pressed'])
        self.quit_button = tp.Button("Quit", MM_BUTTON_STYLES['normal'], MM_BUTTON_STYLES['hover'], MM_BUTTON_STYLES['pressed'])

        self.play_button.at_unclick = self.change_button_state
        self.play_button.at_unclick_params = {"button": self.play_button}
        self.settings_button.at_unclick = self.change_button_state
        self.settings_button.at_unclick_params = {"button": self.settings_button}
        self.quit_button.at_unclick = self.change_button_state
        self.quit_button.at_unclick_params = {"button": self.quit_button}

        self.btn_group = tp.Group([self.play_button, self.settings_button, self.quit_button], gap=20)
        self.btn_group.move(0, 100)
        self.btn_group_upd = self.btn_group.get_updater(self.fps)

        self.menu = Menu(
            self.screen,
            const.PATHS['Backgrounds']['mainMenu'],
            [self.btn_group_upd],
            [self.btn_group],
            "Main Menu"
        )
        self.__prev_menu = self.menu

        self.apply_btn = tp.Button("Apply", SM_BUTTON_STYLES['normal'], SM_BUTTON_STYLES['hover'], SM_BUTTON_STYLES['pressed'])
        self.back_btn = tp.Button("Back", SM_BUTTON_STYLES['normal'], SM_BUTTON_STYLES['hover'], SM_BUTTON_STYLES['pressed'])

        self.master_slider = tp.SliderWithText("Master", 0, 100, cfg.getint('Settings', 'mastervolume'), 100)
        self.sfx_slider = tp.SliderWithText("SFX", 0, 100, cfg.getint('Settings', 'sfxvolume'), 100)
        self.music_slider = tp.SliderWithText("Music", 0, 100, cfg.getint('Settings', 'musicvolume'), 100)
        self.audio_group = tp.Group([self.master_slider, self.sfx_slider, self.music_slider], gap=20)

        self.res_list = pg.display.list_modes()
        self.res_list = [f"{self.res_list[i][0]}x{self.res_list[i][1]}" for i in range(len(self.res_list))]

        self.res_dropdown = tp.DropDownListButton(
            self.res_list,
            cfg.get('Settings', 'width') + "x" + cfg.get('Settings', 'height'),
            SM_BUTTON_STYLES['normal'],
            style_hover=SM_BUTTON_STYLES["hover"],
            style_pressed=SM_BUTTON_STYLES["pressed"],
            style_locked=SM_BUTTON_STYLES["locked"],
            generate_shadow=(True, True),
            size_limit=["auto", 250]
        )

        self.res_dropdown.move(
            self.screen.get_screen().get_width() - SM_BUTTON_STYLES['normal'].margins[0] + 75,
            self.screen.get_screen().get_height() / 2 - SM_BUTTON_STYLES['normal'].margins[1] - 30
        )

        self.res_text = tp.Text(
            "Resolution",
            font_size=30,
            font_color=SM_BUTTON_STYLES['normal'].font_color,
            style_normal=IMG_BUTTON_TEXT_STYLE
        )

        self.res_text.move(
            self.screen.get_screen().get_width() - (SM_BUTTON_STYLES['normal'].margins[0] + 75) - 100,
            self.screen.get_screen().get_height() / 2 - SM_BUTTON_STYLES['normal'].margins[1] - 30
        )

        self.res_text.default_at_unclick = self.do_nothing

        self.fullscreen_checkbox = tp.Checkbox(
            value=cfg.getboolean("Settings", "Fullscreen"),
            style_normal=SM_BUTTON_STYLES["normal"],
            style_hover=SM_BUTTON_STYLES["hover"],
            style_pressed=SM_BUTTON_STYLES["pressed"]
        )

        self.fullscreen_text = tp.Text(
            "Fullscreen",
            font_size=30,
            font_color=SM_BUTTON_STYLES['normal'].font_color,
            style_normal=IMG_BUTTON_TEXT_STYLE
        )
        self.fullscreen_text.default_at_unclick = self.do_nothing

        self.fullscreen_checkbox.move(
            self.screen.get_screen().get_width() / 2 - (SM_BUTTON_STYLES['normal'].margins[0] + 75) - 100,
            self.screen.get_screen().get_height() / 2 - SM_BUTTON_STYLES['normal'].margins[1] - 30
        )
        self.fullscreen_text.move(
            self.screen.get_screen().get_width() / 2 - (SM_BUTTON_STYLES['normal'].margins[0] + 75) - 180,
            self.screen.get_screen().get_height() / 2 - SM_BUTTON_STYLES['normal'].margins[1] - 33
        )
        self.apply_btn.move(
            self.screen.get_screen().get_width() - SM_BUTTON_STYLES['normal'].margins[0] + 75,
            self.screen.get_screen().get_height() - SM_BUTTON_STYLES['normal'].margins[1] - 30
        )
        self.back_btn.move(
            SM_BUTTON_STYLES['normal'].margins[0] - 75,
            self.screen.get_screen().get_height() - SM_BUTTON_STYLES['normal'].margins[1] - 30
        )

        self.apply_btn.at_unclick = self.apply_settings
        self.back_btn.at_unclick = self.change_button_state
        self.back_btn.at_unclick_params = {"button": self.back_btn}

        self.settings_elements = [
            self.apply_btn,
            self.back_btn,
            self.audio_group,
            self.fullscreen_checkbox,
            self.fullscreen_text,
            self.res_text,
            self.res_dropdown
        ]
        self.settings_elements_upd = [element.get_updater(self.fps) for element in self.settings_elements]
        self.settings_menu = Menu(
            self.screen,
            const.PATHS['Backgrounds']['settings_menu'],
            self.settings_elements_upd,
            self.settings_elements,
            "Settings"
        )

        self.char_selector_btns = []
        for keys, values in CHARACTERS.items():
            self.char_selector_btns.append(
                tp.TextAndImageButton(
                    text=keys,
                    img=scale(load(values['characterPreview']), (32, 32)),
                    mode="v", styleNormal=SM_BUTTON_STYLES['normal'],
                    styleHover=SM_BUTTON_STYLES['hover'],
                    stylePressed=SM_BUTTON_STYLES['pressed'],
                    text_style=IMG_BUTTON_TEXT_STYLE
                )
            )

        for i in self.char_selector_btns:
            i.at_unclick = self.change_button_state
            i.at_unclick_params = {"button": i}
            for j in i.children:
                j.default_at_unclick = self.do_nothing

        self.char_selector_btns_group = tp.Group(self.char_selector_btns, gap=20, mode="h")
        self.char_selector_btns_group_upd = self.char_selector_btns_group.get_updater(self.fps)
        self.back_btn_upd = self.back_btn.get_updater(self.fps)

        self.char_selector_menu = Menu(
            self.screen,const.PATHS['Backgrounds']['CharacterSelector'],
            [self.char_selector_btns_group_upd, self.back_btn_upd],
            [self.char_selector_btns_group, self.back_btn],
            "Character Selector"
        )

        self.map_selector_btns = []
        for keys, values in const.PATHS['Maps'].items():
            self.map_selector_btns.append(
                tp.TextAndImageButton(
                    text=keys,
                    img=scale(load(values), (128, 128)),
                    mode="h", margins=(10, 15), reverse=True,
                    styleNormal=SM_BUTTON_STYLES['normal'],
                    styleHover=SM_BUTTON_STYLES['hover'],
                    stylePressed=SM_BUTTON_STYLES['pressed'],
                    text_style=IMG_BUTTON_TEXT_STYLE
                )
            )

        for i in self.map_selector_btns:
            i.at_unclick = self.change_button_state
            i.at_unclick_params = {"button": i}
            for j in i.children:
                j.default_at_unclick = self.do_nothing

        self.map_selector_btns_group = tp.Group(self.map_selector_btns, gap=20, mode="v")
        self.map_selector_btns_group_upd = self.map_selector_btns_group.get_updater(self.fps)
        self.map_selector_menu = Menu(
            self.screen,
            const.PATHS['Backgrounds']['MapSelector'],
            [self.map_selector_btns_group_upd, self.back_btn_upd],
            [self.map_selector_btns_group, self.back_btn],
            "Map Selector"
        )

    def do_nothing(self) -> None:
        """Dummy function for button click events."""
        pass

    def run_current(self) -> list:
        """
        Run the current menu loop and handle user interactions.
        
        This method manages the main game loop for the current menu, handling:
        - Background rendering and element updates
        - Button state checking and user input processing
        - Menu navigation (Play, Settings, Quit, Back)
        - Character and map selection
        - Window close events
        
        The method continuously runs until the menu is closed or a menu action
        is triggered by the user.
        
        Returns:
            list: A list containing two elements:
                - str: The action name ("Play", "Settings", "Quit", "Back", or selected item text)
                - bool: Whether the menu should continue running (True) or exit (False)
                
        Menu Flow:
            - Main menu: Returns "Play", "Settings", or "Quit" when respective buttons are clicked
            - Settings/Character/Map menus: Returns "Back" when back button is clicked
            - Character selector: Returns the selected character's text
            - Map selector: Returns the selected map's text
            - Window close: Returns "Quit" with False flag to exit
        """
        self.__prev_menu.running = True
        while self.__prev_menu.running:
            self.__prev_menu.bg.blit_static()

            for i in self.__prev_menu.elements_upd:
                i.update()

            if self.__prev_menu == self.menu:
                if self.play_button.state == "unclicked":
                    return ["Play", True]

                if self.settings_button.state == "unclicked":
                    return ["Settings", True]

                if self.quit_button.state == "unclicked":
                    return ["Quit", True]

            if self.__prev_menu in {self.settings_menu, self.char_selector_menu, self.map_selector_menu}:
                if self.back_btn.state == "unclicked":
                    return ["Back", True]

            if self.__prev_menu == self.char_selector_menu:
                for i in self.char_selector_btns:
                    if i.state == "unclicked":
                        return [i.children[0].text, True]

            if self.__prev_menu == self.map_selector_menu:
                for i in self.map_selector_btns:
                    if i.state == "unclicked":
                        return [i.children[1].text, True]

            if pg.event.poll().type == pg.QUIT:
                self.__prev_menu.running = False
                return ["Quit", False]

            pg.display.update()
            self.clock.tick(self.fps)

    def change_menu(self, change_to: Menu) -> None:
        """
        Changes the current menu to a new menu, handling visibility transitions.
        
        This method hides all elements from the previous menu and shows all elements
        from the new menu. It also updates the screen caption and resets the mouse
        cursor to the default arrow.
        
        Args:
            change_to (Menu): The new menu to change to. Can be None to hide
                            the current menu without showing a new one.
        
        Side Effects:
            - Sets all elements in the previous menu to invisible
            - Sets all elements in the new menu to visible
            - Updates the screen caption with the new menu's caption
            - Resets the mouse cursor to system arrow cursor
        """
        if self.__prev_menu:
            for i in self.__prev_menu.elements:
                i.set_invisible(True, True)

        if change_to:
            self.__prev_menu = change_to
            for i in change_to.elements:
                i.set_invisible(False, True)

            self.screen.set_caption(f"VampyGame: {change_to.caption}")

        pg.mouse.set_cursor(pg.SYSTEM_CURSOR_ARROW)

    def change_button_state(self, button: tp.elements.Element) -> None:
        """
        Changes the state of a button element to 'unclicked'.
        
        This method sets the state attribute of the provided button element
        to 'unclicked', typically used to reset a button's visual or 
        behavioral state after it has been interacted with.
        
        Args:
            button (tp.elements.Element): The button element whose state 
                                        needs to be changed.
        """
        button.state = "unclicked"

    def apply_settings(self) -> None:
        """
        Apply the current settings from the UI controls to the configuration file.
        
        This method reads values from various UI elements (resolution dropdown, 
        checkboxes, and sliders) and saves them to the configuration object, 
        then writes the updated configuration to 'data/config.ini' file.
        
        Settings applied:
        - Resolution (width and height) from resolution dropdown
        - Fullscreen mode from fullscreen checkbox
        - Master volume from master volume slider
        - Music volume from music volume slider
        - SFX volume from SFX volume slider
        """
        if self.res_dropdown.get_value():
            res = self.res_dropdown.get_value().split("x")
            cfg.set('Settings', 'width', res[0])
            cfg.set('Settings', 'height', res[1])

        cfg.set('Settings', 'fullscreen', str(self.fullscreen_checkbox.get_value()))
        cfg.set('Settings', 'mastervolume', str(self.master_slider.get_value()))
        cfg.set('Settings', 'musicvolume', str(self.music_slider.get_value()))
        cfg.set('Settings', 'sfxvolume', str(self.sfx_slider.get_value()))

        with open('data/config.ini', 'w', encoding='utf-8') as config_file:
            cfg.write(config_file)
