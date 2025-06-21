'''This module contains the background class for the game. It handles the background image and its rendering.'''
import pygame as pg
from pygame.image import load
from pygame.locals import *
from pygame.transform import scale


class BG:
    """
    A background image handler for pygame applications that provides flexible rendering options.
    
    This class manages background images with support for scrolling, scaling, and positioning.
    It can handle both static backgrounds (centered on screen) and dynamic backgrounds that
    can be moved with camera offsets. The class automatically loads and processes images
    based on the specified parameters.
    
    Core functionality:
    - Load and optionally scale background images to fit screen dimensions
    - Render backgrounds with camera offset support for scrolling effects
    - Render static centered backgrounds
    - Manage background positioning relative to spawn points
    
    Args:
        map_image (str): Path to the background image file
        screen (pg.Surface): Pygame surface to render the background onto
        speed (int, optional): Movement speed parameter (currently unused). Defaults to 0.
        spawnpoint (pg.math.Vector2, optional): Reference point for background positioning,
            automatically adjusted relative to screen center. Defaults to (0, 0).
        fill (bool, optional): If True, scales the image to match screen dimensions.
            If False, uses original image size. Defaults to False.
    
    Note:
        The spawnpoint is automatically adjusted by subtracting half the screen dimensions,
        effectively making it relative to the screen center rather than top-left corner.
    """
    def __init__(self,
                 map_image: str,
                 screen: pg.Surface,
                 speed: int = 0,
                 spawnpoint: pg.math.Vector2 = pg.math.Vector2(0,0),
                 fill = False
    ):
        self.map_image = map_image
        self.screen = screen
        self.speed = speed
        self.fill = fill
        self.spawnpoint = (spawnpoint[0] - self.screen.get_width() / 2, spawnpoint[1] - self.screen.get_height() / 2)
        self.__post_init__()

    def __post_init__(self):
        """
        Post-initialization method called after object initialization.
        
        This method loads and processes the map image based on the fill attribute.
        If fill is True, the image is scaled to match the screen dimensions.
        Otherwise, the image is loaded at its original size. The method also
        sets the width and height attributes based on the processed background image.
        
        Attributes set:
            bg: The processed background image (pygame Surface)
            width: Width of the background image in pixels
            height: Height of the background image in pixels
        """
        if self.fill:
            self.bg = scale(load(self.map_image).convert(), (self.screen.get_width(), self.screen.get_height()))
        else:
            self.bg = load(self.map_image).convert()
        self.width = self.bg.get_width()
        self.height = self.bg.get_height()

    def blit_bg(self, offset: pg.math.Vector2 = pg.math.Vector2(0,0)) -> None:
        """
        Blit the background image to the screen with an optional offset.
        
        This method renders the background image to the screen surface, taking into account
        both the provided offset and the spawnpoint to determine the final position.
        
        Args:
            offset (pg.math.Vector2, optional): Additional offset vector to apply to the 
                background position. Defaults to pg.math.Vector2(0,0).
        
        Note:
            The final position is calculated as: bg.topleft - (offset + spawnpoint)
            This means both offset and spawnpoint are subtracted from the background's
            top-left corner position.
        """
        self.screen.blit(self.bg, self.bg.get_rect().topleft - (offset + self.spawnpoint))

    def blit_static(self) -> None:
        """
        Blit the background image to the center of the screen.
        
        This method centers the background image on the screen by calculating
        the appropriate position based on the difference between screen and
        background dimensions.
        
        The background is positioned so that its center aligns with the
        screen's center point.
        """
        self.screen.blit(
            self.bg,
            ((self.screen.get_width() // 2) - (self.bg.get_width() // 2), (self.screen.get_height() // 2) - (self.bg.get_height() // 2))
        )
