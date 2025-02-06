import pygame as pg
from pygame.locals import MOUSEMOTION, MOUSEBUTTONDOWN, MOUSEBUTTONUP
from pygame.font import Font, SysFont
from pygame.image import load

class Button:
    def __init__(self, x, y, width, height, text, font, color, hover_color, click_color, image=None, image_hover=None, image_click=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.font = font
        self.color = color
        self.hover_color = hover_color
        self.click_color = click_color
        
        self.image = image
        self.image_hover = image_hover
        self.image_click = image_click

        self.rect = pg.Rect(self.x, self.y, self.width, self.height)
        self.text_surface = self.font.render(self.text, True, self.color)
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)

        self.hovered = False
        self.clicked = False

    def draw(self, screen):
        if self.image:
            if self.hovered and self.image_hover:
                screen.blit(self.image_hover, self.rect)
            elif self.clicked and self.image_click:
                screen.blit(self.image_click, self.rect)
            else:
                screen.blit(self.image, self.rect)
        else:
            if self.hovered:
                pg.draw.rect(screen, self.hover_color, self.rect)
            elif self.clicked:
                pg.draw.rect(screen, self.click_color, self.rect)
            else:
                pg.draw.rect(screen, self.color, self.rect)

        screen.blit(self.text_surface, self.text_rect)

    def update(self, event):
        if event.type == MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        elif event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                self.clicked = self.rect.collidepoint(event.pos)
        elif event.type == MOUSEBUTTONUP:
            if event.button == 1:
                self.clicked = False

    def is_clicked(self):
        return self.clicked

# Example usage
# button = Button(100, 100, 200, 50, "Click Me", font, (255, 255, 255), (200, 200, 200), (150, 150, 150))
# button.draw(screen)
# button.update(event)
# if button.is_clicked():
#     print("Button clicked!")
#     # Do something when the button is clicked
#     button.clicked = False
#     # Reset the clicked state after handling the click
#     # This is important to prevent the button from triggering multiple times
#     # when the mouse button is held down
#     # You can also add a delay or cooldown to prevent rapid clicking