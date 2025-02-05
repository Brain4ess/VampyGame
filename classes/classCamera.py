import pygame as pg
from classes.classCharacter import Character

class Camera:
    def __init__(self, screen: pg.Surface, width, height):
        self.screen = screen
        self.width = width
        self.height = height
        self.camera = pg.Rect(0, 0, width, height)
        
    # def apply(self, entity: pg.Surface):
    #     return entity.get_rect().move(self.camera.topleft)
    
    def draw(self, surface: pg.Surface, group):
        for sprite in group:
            surface.blit(sprite.image, self.apply(sprite))
    
    def getoffset(self):
        return pg.math.Vector2(self.camera.topleft[0], self.camera.topleft[1])
    
    def update(self, target: Character):
        x = target.rect.centerx - self.screen.get_width() / 2 
        y = target.rect.centery - self.screen.get_height() / 2
        
        self.camera = pg.Rect(x, y, self.width, self.height)
        


