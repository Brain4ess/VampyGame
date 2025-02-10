import pygame as pg
from classes.classCharacter import Character

class Camera:
    def __init__(self, screen: pg.Surface, width, height, bg):
        self.screen = screen
        self.width = width
        self.height = height
        self.bg = bg
        self.camera = pg.Rect(0, 0, width, height)
    
    
    # def apply(self, entity: pg.Surface):
    #     return entity.get_rect().move(self.camera.topleft)
    
    
    # def draw(self, surface: pg.Surface, group):
    #     for sprite in group:
    #         surface.blit(sprite.image, self.apply(sprite))
    
    
    def getoffset(self):
        return pg.math.Vector2(self.camera.topleft[0], self.camera.topleft[1])
    
    
    def update(self, target: Character):
        """
        Update the camera position to follow the target character.
        
        Args:
            target (Character): The character to follow.

        Returns:
            None
        """

        # Calculate the new x position of the camera to follow the target character
        # When the camera reaches the threshold value we stop moving in the direction the camera has reached the end of a background
        x = max(-self.bg.spawnpoint[0], min(self.bg.width - self.screen.get_width() - self.bg.spawnpoint[0], target.rect.centerx - (self.screen.get_width() / 2)))
        y = max(-self.bg.spawnpoint[1], min(self.bg.height - self.screen.get_height() - self.bg.spawnpoint[1], target.rect.centery - (self.screen.get_height() / 2)))

        # Update the camera position
        self.camera = pg.Rect(x, y, self.width, self.height)
