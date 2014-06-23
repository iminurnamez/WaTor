import os
import pygame as pg
from . import tools
#from .components import players

SCREEN_SIZE = (1280, 640)
CELL_SIZE = 16
ORIGINAL_CAPTION = "Wa-Tor"

pg.init()
os.environ['SDL_VIDEO_CENTERED'] = "TRUE"
pg.display.set_caption(ORIGINAL_CAPTION)
SCREEN = pg.display.set_mode(SCREEN_SIZE)
SCREEN_RECT = SCREEN.get_rect()


FONTS = tools.load_all_fonts(os.path.join("resources", "fonts"))
MUSIC = tools.load_all_music(os.path.join("resources", "music"))
#SFX   = tools.load_all_sfx(os.path.join("resources", "sound"))
#GFX   = tools.load_all_gfx(os.path.join("resources", "graphics"))

for direct in [("up", 90), ("left", 180), ("down", 270)]:
    GFX["fish" + direct[0]] = pg.transform.rotate(GFX["fishright"], direct[1])
    GFX["shark" + direct[0]] = pg.transform.rotate(GFX["sharkright"], direct[1])