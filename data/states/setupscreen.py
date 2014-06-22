import pygame as pg
from .. import tools, prepare
from ..components.labels import Label, GroupLabel, Button, GroupButton


FONT = prepare.FONTS["weblysleekuili"]
class SetupScreen(tools._State):
    def __init__(self):
        
        super(SetupScreen, self).__init__()
        self.next = "SIMULATION"
        
        
    def startup(self, persistent):    
        screen_rect = pg.display.get_surface().get_rect()
        self.persist = {"Number of Fish": 200,
                             "Fish Fertility Age": 2,
                             "Number of Sharks": 200,
                             "Shark Fertility Age": 3,
                             "Shark Belly Size": 2}                            
        self.labels = []
        self.buttons = []
        self.dynamics = []
        self.title = GroupLabel(self.labels, FONT, 48, "Wa-Tor Setup", "blue",
                                   {"midtop": (screen_rect.centerx, 10)})
        
        
        
        start = Label(FONT, 36, "Start", "blue", {"midbottom": (screen_rect.centerx, screen_rect.bottom - 20)})
        w, h = 120, 70
        self.start = Button(screen_rect.centerx - w/2, screen_rect.bottom - (h + 20), w, h, start, "Start", 0)
                                     
        
        
        left1 = 200
        self.left2 = 500
        left3 = 630
        left4 = 700
        left5 = 780
        left6 = 850
        left7 = 930
        left8 = 1000
        top = 150
        space = 30
        for stat_name, stat in self.persist.items():
            text = GroupLabel(self.labels, FONT, 24, stat_name, "white", {"topleft": (left1, top)})
            number = GroupLabel(self.dynamics, FONT, 24, "{}".format(stat), "white", {"topleft": (self.left2, top)})
            up = Label(FONT, 24, "+1", "gray10", {"center": (0, 0)})
            up_button = GroupButton(self.buttons, left3, top - 10, 60, 40, up, stat_name, 1)
            down = Label(FONT, 24, "-1", "gray10", {"center": (0, 0)})
            down_button  = GroupButton(self.buttons, left4, top - 10, 60, 40, down, stat_name, -1)
            up10 = Label(FONT, 24, "+10", "gray10", {"center": (0, 0)})
            up10_button = GroupButton(self.buttons, left5, top - 10, 60, 40, up10, stat_name, 10)
            down10 = Label(FONT, 24, "-10", "gray10", {"center": (0, 0)})
            down10_button = GroupButton(self.buttons, left6, top - 10, 60, 40, down10, stat_name, -10)
            up100 = Label(FONT, 24, "+100", "gray10", {"center": (0, 0)})
            up100_button = GroupButton(self.buttons, left7, top - 10, 60, 40, up100, stat_name, 100)
            down100 = Label(FONT, 24, "-100", "gray10", {"center": (0, 0)})
            down100_button = GroupButton(self.buttons, left8, top - 10, 60, 40, down100, stat_name, -100)
            top += text.rect.height + space

        
    def get_event(self, event):
        if event.type == pg.QUIT:
            self.done = True
            self.quit = True
        elif event.type == pg.KEYDOWN:
            pass
        elif event.type == pg.MOUSEBUTTONDOWN:
            if self.start.rect.collidepoint(event.pos):
                self.done = True
                self.persist["initial"] = True
            else:
                for button in self.buttons:
                    if button.rect.collidepoint(event.pos):
                        self.persist[button.payload] += button.amount
                        break        
        
    def update(self, surface, keys):        
        self.dynamics = []
        top = 150
        for stat_name, stat in self.persist.items():
            dynamic = GroupLabel(self.dynamics, FONT, 24, "{}".format(stat), "white", {"topleft": (self.left2, top)})
            top += dynamic.rect.height + 30            

        self.draw(surface)

    def draw(self, surface):
        surface.fill(pg.Color("black"))
        for label in self.labels:
            label.draw(surface)
        for dyno in self.dynamics:
            dyno.draw(surface)
        for button in self.buttons:
            button.draw(surface)  
        self.start.draw(surface)            