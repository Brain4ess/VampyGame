import pygame as pg
from pygame.locals import MOUSEMOTION, MOUSEBUTTONDOWN, MOUSEBUTTONUP
from pygame.font import Font, SysFont
from pygame.image import load
from dataclasses import dataclass, field, InitVar

@dataclass
class Button:
    """
    A class representing a button with customizable properties and behaviors.

    This class provides a way to create a button with various visual and functional properties.
    It supports text and image rendering, color changes on hover and click, and event handling
    for mouse interactions.

    Attributes:
        pos (tuple): Position of the button on the screen (x, y).
        size (tuple): Size of the button (width, height).
        image (str): Path to the image file to be displayed on the button.
        text (str): Text to be displayed on the button.
        font (InitVar[str]): Font name to be used for rendering the text.
        defaultSysFont (str): Default system font to be used if no font is specified.
        fontSize (int): Font size for rendering the text.
        bgColor (str | tuple[int, int, int]): Background color of the button.
        textColor (str | tuple[int, int, int]): Text color.
        hoverColor (str | tuple[int, int, int]): Color of the button when hovered.
        clickColor (str | tuple[int, int, int]): Color of the button when clicked.
        isHovered (bool): Flag indicating if the mouse is hovering over the button.
        isClicked (bool): Flag indicating if the button is clicked.
        onClickReferences (object): Reference to the function to be called on click.
        referenceArgs (tuple): Arguments to be passed to the onClickReferences function.
        referenceKwargs (dict): Keyword arguments to be passed to the onClickReferences function.

    Methods:
        __post_init__(font: str): Initializes the button's font.
        update(surface): Updates the button's appearance on the given surface.
        handleEvent(event): Handles mouse events to update the button's state.
    """
    
    
    pos: tuple = (0, 0)
    size: tuple = (20, 20)

    image: str = None

    text: str = None
    font: InitVar[str] = None
    defaultSysFont: str = 'Arial'
    fontSize: int = 26

    bgColor: str | tuple[int, int, int] = (0, 0, 0)
    textColor: str | tuple[int, int, int] = 'white'
    hoverColor: str | tuple[int, int, int] = (0, 0, 0)
    clickColor: str | tuple[int, int, int] = (0, 0, 0)

    isHovered: bool = False
    isClicked: bool = False

    onClickReferences: object = None
    referenceArgs: tuple = field(default_factory = tuple)
    referenceKwargs: dict = field(default_factory = dict)


    def __post_init__(self, font: str):
        """
        Initialize the rectangle and font attributes for the Text object.

        Args:
            font (str): The name of the font to use. If None, the system default font will be used.
        """
        self.rect = pg.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
        self.font = Font(font, self.fontSize) if font else SysFont(self.defaultSysFont, self.fontSize)


    def update(self, surface):
        if self.isClicked:
            self.color = self.clickColor
        elif self.isHovered:
            self.color = self.hoverColor
        else:
            self.color = self.bgColor

        pg.draw.rect(surface, self.color, self.rect, border_radius = 20)

        if self.text:
            textSurface = self.font.render(self.text, True, self.textColor)
            textRect = textSurface.get_rect(center = self.rect.center)
            surface.blit(textSurface, textRect)
        
        if self.image:
            image = load(self.image)
            imageRect = self.image.get_rect(center = self.rect.center)
            surface.blit(image, imageRect)


    def handleEvent(self, event):
        # Check if the event is a mouse motion event
        if event.type == MOUSEMOTION:
            # Check if the mouse is hovering over the rectangle
            self.isHovered = self.rect.collidepoint(event.pos)
        # Check if the event is a mouse button down event
        elif event.type == MOUSEBUTTONDOWN:
            # Check if the left mouse button is pressed and the mouse is over the rectangle
            if event.button == 1 and self.rect.collidepoint(event.pos):
                # Set the isClicked attribute to True
                self.isClicked = True
                # Check if there are any references to call when the button is clicked
                if self.onClickReferences:
                    # Call the references with the reference arguments and keyword arguments
                    self.onClickReferences(*self.referenceArgs, **self.referenceKwargs)
        # Check if the event is a mouse button up event
        elif event.type == MOUSEBUTTONUP:
            # Set the isClicked attribute to False
            self.isClicked = False
