import pygame as pg
from ..import tools, prepare
from ..components.labels import Label, GroupLabel

class Line(object):
    def __init__(self, name, color, points, label_topleft):
        self.active = True
        self.name = name
        self.points = points
        self.color = color
        self.label = Label(prepare.FONTS["weblysleekuili"], 24,
                                  self.name, self.color, {"topleft": label_topleft})
        


    def draw(self, surface):
        if self.active:
            pg.draw.lines(surface, pg.Color(self.color), False, self.points)

class StatsGraph(tools._State):
    def __init__(self):
        super(StatsGraph, self).__init__()
        self.next = "SIMULATION"
        self.height = pg.display.get_surface().get_height()
        self.base = self.height - 200
        self.width = pg.display.get_surface().get_width()

    def get_points(self, stats, key, x_scale, y_scale, base):
        return [(int(k * x_scale),
                    base - int(stats[k][key] * y_scale)) for k in stats]

    def startup(self, persistent):
        
        
        left1 = 100
        left2 = 350
        self.stats = persistent["stats"]
        x_scale = self.width / float(max(self.stats.keys()))
        y_scale =.1
        _lines = [("Fish", "gray80", y_scale, (left1, self.base + 20)),
                      ("Average Fish Age", "blue", y_scale, (left1, self.base + 50)),
                      ("Fish Births", "cyan", y_scale, (left1, self.base + 80)),
                      ("Sharks", "purple", y_scale, (left2, self.base + 20)),
                      ("Average Shark Age", "orange", y_scale, (left2, self.base + 50)),
                      ("Avergae Shark Belly", "yellow", y_scale, (left2, self.base + 80)),
                      ("Shark Births", "deeppink", y_scale, (left2, self.base + 110)),
                      ("Shark Deaths", "red", y_scale, (left2, self.base + 140))]
        self.lines = [Line(x[0], x[1],
                                 self.get_points(self.stats, x[0], x_scale, x[2], self.base),
                                 x[3])
                                 for x in _lines]
        
        self.labels = []
        _instruct  =["Click on a category to toggle that line on the graph",
                           "Press G to return to simulation"]
        centx = 900
        centy = self.base + 40
        f = prepare.FONTS["weblysleekuili"]
        for instruct in _instruct:
            label = GroupLabel(self.labels, f, 24, instruct, "white",
                                        {"center": (centx, centy)}, "black")
            centy += label.rect.height + 15
    def update(self, surface, keys):
        self.draw(surface)

    def draw(self, surface):
        surface.fill(pg.Color("black"))
        for line in self.lines:
            line.draw(surface)
            line.label.draw(surface)
        for label in self.labels:
            label.draw(surface)

    def get_event(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_g:
                self.done = True
                self.persist["initial"] = False
        elif event.type == pg.MOUSEBUTTONDOWN:
            for line in self.lines:
                if line.label.rect.collidepoint(event.pos):
                    line.active = not line.active