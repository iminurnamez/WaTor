import pygame as pg
from .. import tools, prepare
from ..components.labels import Label, GroupLabel, Button

class Intro(tools._State):
    def __init__(self):
        self.font = prepare.FONTS["weblysleekuili"]
        super(Intro, self).__init__()
        self.next = "SETUPSCREEN"        
        screen_rect = pg.display.get_surface().get_rect()
        self.labels = []
        self.title = GroupLabel(self.labels, self.font, 64, "Wa-Tor", "blue",
                                         {"midtop": (screen_rect.centerx, 10)})
        

        control_title = GroupLabel(self.labels, self.font, 32, "Controls", "white", 
                                               {"midtop": (screen_rect.centerx, self.title.rect.bottom + 10)})
        instructs = [("UP", "Increase sim FPS"), ("DOWN", "Decrease sim FPS"),
                          ("U", "Toggle manual updating"), ("SPACE", "Manual update"),
                          ("F", "Toggle fullscreen"), ("G", "View graph"),
                          ("R",  "Write to JSON"), ("ESC", "Exit")]    
        top = control_title.rect.bottom + 10
        first_left = 500
        second_left = 650
        
        for instruct in instructs:
            label = GroupLabel(self.labels, self.font, 24, instruct[0], "white", {"topleft": (first_left, top)})
            label2 = GroupLabel(self.labels, self.font, 24, instruct[1], "white", {"topleft": (second_left, top)})
            top += label.rect.height + 5
            
        start = Label(self.font, 48, "Next", "blue", {"midbottom": (screen_rect.centerx, screen_rect.bottom - 20)})
        w, h = 120, 70
        self.start = Button(screen_rect.centerx - w/2, screen_rect.bottom - (h + 20), w, h, start, "Start", 0)
        
    def get_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.start.rect.collidepoint(event.pos):
                self.done = True
                
    def update(self, surface, keys):
        self.draw(surface)
        
    def draw(self, surface):
        for label in self.labels:
            label.draw(surface)
        self.start.draw(surface)