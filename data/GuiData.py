import pygame as pg
import thorpy as tp
import data.Constants as const

MM_BUTTON_STYLE_NORMAL = tp.styles.RoundStyle()
MM_BUTTON_STYLE_NORMAL.bck_color = (28,28,28)
MM_BUTTON_STYLE_NORMAL.font_color = (176, 55, 80)
MM_BUTTON_STYLE_NORMAL.margins = (250,30)
MM_BUTTON_STYLE_NORMAL.border_thickness = 4
MM_BUTTON_STYLE_NORMAL.font = pg.font.Font(const.PATHS['Fonts']['mainMenu']['Buttons_caps'], 50)
MM_BUTTON_STYLE_NORMAL.size = (500, 100)

MM_BUTTON_STYLE_HOVER = MM_BUTTON_STYLE_NORMAL.copy()
MM_BUTTON_STYLE_HOVER.nframes = 30
MM_BUTTON_STYLE_HOVER.font_color = (255,0,0)
MM_BUTTON_STYLE_HOVER.border_color = (230,230,230)
MM_BUTTON_STYLE_HOVER.thickness = 5

MM_BUTTON_STYLE_PRESSED = MM_BUTTON_STYLE_NORMAL.copy()

MM_BUTTON_STYLES = {
    'normal': MM_BUTTON_STYLE_NORMAL,
    'hover': MM_BUTTON_STYLE_HOVER,
    'pressed': MM_BUTTON_STYLE_PRESSED
}

SM_BUTTON_STYLE_NORMAL = MM_BUTTON_STYLE_NORMAL.copy()
SM_BUTTON_STYLE_NORMAL.font = pg.font.Font(const.PATHS['Fonts']['mainMenu']['Buttons_caps'], 30)
SM_BUTTON_STYLE_NORMAL.size = (300, 60)

SM_BUTTON_STYLE_HOVER = SM_BUTTON_STYLE_NORMAL.copy()
SM_BUTTON_STYLE_HOVER.nframes = 30
SM_BUTTON_STYLE_HOVER.font_color = (255,0,0)
SM_BUTTON_STYLE_HOVER.border_color = (230,230,230)
SM_BUTTON_STYLE_HOVER.thickness = 5

SM_BUTTON_STYLE_PRESSED = SM_BUTTON_STYLE_NORMAL.copy()
SM_BUTTON_STYLE_LOCKED = SM_BUTTON_STYLE_NORMAL.copy()
SM_BUTTON_STYLE_LOCKED.font_color = (255,255,255)

SM_BUTTON_STYLES = {
    'normal': SM_BUTTON_STYLE_NORMAL,
    'hover': SM_BUTTON_STYLE_HOVER,
    'pressed': SM_BUTTON_STYLE_PRESSED,
    'locked': SM_BUTTON_STYLE_LOCKED
}

IMG_BUTTON_TEXT_STYLE = tp.styles.TextStyle()
IMG_BUTTON_TEXT_STYLE.font = pg.font.Font(const.PATHS['Fonts']['mainMenu']['Buttons_regular'], 30)
IMG_BUTTON_TEXT_STYLE.font_color = (176, 55, 80)