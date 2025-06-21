'''This module contains the camera class for the game. It handles the camera position and movement based on the target character.'''
import pygame as pg

from classes.class_character import Character


class Camera:
    """
    A 2D camera system for pygame applications that follows a target character.
    
    This class manages the viewport position and provides smooth camera following
    functionality with boundary constraints. The camera automatically tracks a
    target character while respecting the boundaries defined by the background.
    
    Core functionality:
    - Follow target characters with centered positioning
    - Enforce camera boundaries based on background dimensions
    - Provide camera offset calculations for rendering
    - Maintain viewport dimensions and position
    
    Args:
        screen (pg.Surface): The pygame surface to render to
        width (int): Width of the camera viewport
        height (int): Height of the camera viewport  
        bg: Background object that defines camera movement boundaries and spawn point
    
    Note:
        The background object must have 'width', 'height', and 'spawnpoint' attributes
        for proper camera boundary calculations.
    """
    def __init__(self, screen: pg.Surface, width, height, bg):
        self.screen = screen
        self.width = width
        self.height = height
        self.bg = bg
        self.camera = pg.Rect(0, 0, width, height)

    def getoffset(self) -> pg.math.Vector2:
        """
        Get the current camera offset as a Vector2.
        
        Returns the top-left position of the camera as a pygame Vector2 object,
        which represents the camera's offset from the origin (0, 0).
        
        Returns:
            pg.math.Vector2: A Vector2 containing the camera's x and y offset values
                           from the camera's top-left corner position.
        """
        return pg.math.Vector2(self.camera.topleft[0], self.camera.topleft[1])

    def update(self, target: Character) -> None:
        """
        Update the camera position to follow the target character.

        Args:
            target (Character): The character to follow.
        """
        # Calculate the new x position of the camera to follow the target character
        # When the camera reaches the threshold value we stop moving in the direction the camera has reached the end of a background
        x = max(-self.bg.spawnpoint[0], min(self.bg.width - self.screen.get_width() - self.bg.spawnpoint[0], target.rect.centerx - (self.screen.get_width() / 2)))
        y = max(-self.bg.spawnpoint[1], min(self.bg.height - self.screen.get_height() - self.bg.spawnpoint[1], target.rect.centery - (self.screen.get_height() / 2)))

        # Update the camera position
        self.camera = pg.Rect(x, y, self.width, self.height)