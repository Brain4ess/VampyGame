import pygame as pg

# pg.init()
# screen = pg.display.set_mode((800, 800))
# pg.display.set_caption("Button!")
#main_font = pg.font.SysFont("cambria", 50)
class Button():
    def __init__(self, screen: pg.Surface, image: pg.Surface, x_pos, y_pos, text_input, font: str = 'Arial', sysfont = True, text_color = 'white', hover_color = 'green'):
        
        self.image = image
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.font = font
        self.screen = screen
        if not sysfont:
            self.main_font = pg.font.Font(font, 60)
        else:
            self.main_font = pg.font.SysFont(font, 60)
        self.hoverColor = hover_color
        self.text_color = text_color
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_input = text_input
        self.text = self.main_font.render(self.text_input, True, text_color)
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))
    def update(self):
        self.screen.blit(self.image, self.rect)
        self.screen.blit(self.text, self.text_rect)
    
    def checkForInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False
    
    def changeColor(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.text = self.main_font.render(self.text_input, True, self.hoverColor)
        else:
            self.text = self.main_font.render(self.text_input, True, self.text_color)


# button_surface = pg.image.load("assets/images/placeholders/buttons/playButton.png")
# font = 'assets/fonts/Salina-Trial-Regular.otf'
# button_surface = pg.transform.scale(button_surface, (400, 150))

# button = Button(button_surface, 400, 300, "PLAY", 'Algerian', True, text_color=(176, 55, 80), hover_color=(215, 67, 97))


# while True:
# 	for event in pg.event.get():
# 		if event.type == pg.QUIT:
# 			pg.quit()
# 			exit()
# 		if event.type == pg.MOUSEBUTTONDOWN:
# 			button.checkForInput(pg.mouse.get_pos())

# 	screen.fill("white")

# 	button.update()
# 	button.changeColor(pg.mouse.get_pos())

# 	pg.display.update()
