from dataclasses import dataclass

import pygame as pg
from pygame.display import set_caption, set_icon, set_mode
from pygame.image import load


@dataclass
class GameScreen(pg.Surface):
    """A pygame-based game screen manager for creating and managing display windows.
    
    This class provides a convenient interface for creating and configuring pygame display windows
    with support for fullscreen mode, window captions, and custom icons. It extends pygame.Surface
    to provide additional display management functionality.
    
    Key Features:
    - Automatic display window initialization
    - Fullscreen and windowed mode support
    - Window caption and icon configuration
    - Screen surface access and management
    
    Attributes:
        size (tuple): Window dimensions as (width, height). Default: (1280, 720)
        caption (str): Window title/caption text. Default: ""
        icon (str): Path to icon image file. Default: ""
        fullscreen (bool): Whether to create window in fullscreen mode. Default: False
    
    Note:
        This class requires pygame to be properly initialized before use. The __post_init__
        method automatically sets up the display window, so manual initialization is not required
        after setting the desired attributes.
    """
    size: tuple = (1280, 720)
    caption: str = ""
    icon: str = ""
    fullscreen: bool = False

    def __post_init__(self):
        if self.fullscreen:
            self.win = set_mode(self.size, pg.FULLSCREEN)
        else:
            self.win = set_mode(self.size)

        set_caption(self.caption)

        if self.icon:
            set_icon(load(self.icon))

    def get_screen(self) -> pg.Surface:
        """
        Get the current screen surface.
        
        Returns:
            pg.Surface: The pygame surface representing the current window/screen.
        """
        return self.win

    def set_caption(self, caption: str) -> None:
        """
        Set the caption for the window or display.
        
        Args:
            caption (str): The caption text to be set as the window title.
        """
        set_caption(caption)
