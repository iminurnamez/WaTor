import json
import pygame as pg
from .. import tools
from ..components.world import World


class Sim(tools._State):
    def __init__(self):
        super(Sim, self).__init__()
        self.world = World(80, 40, 16, 200, 1, 100, 200, 150)
        self.fps = 30
        self.run_speed = 1
        self.mode = "MANUAL"

    def startup(self, persistent):
        if persistent["initial"]:
            nfish = persistent["Number of Fish"]
            nsharks = persistent["Number of Sharks"]
            fish_fert = persistent["Fish Fertility Age"]
            shark_fert = persistent["Shark Fertility Age"]
            shark_belly = persistent["Shark Belly Size"]
            self.world = World(80, 40, 16, nfish, nsharks, fish_fert,
                                        shark_fert, shark_belly)

    def write_report(self):
        with open("wator_report.json", "w") as f:
                report = json.dumps(self.world.stats)
                f.write(report)

    def get_event(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.done = True
                self.quit = True
            elif event.key == pg.K_g:
                self.done = True
                self.persist["stats"] = self.world.stats
                self.next = "GRAPH"
            elif event.key == pg.K_r:
                self.write_report()
            elif event.key == pg.K_SPACE and self.mode == "MANUAL":
                self.world.update()
            elif event.key == pg.K_u:
                if self.mode == "MANUAL":
                    self.dt = 0.0
                    self.mode = "AUTOMATIC"
                else:
                    self.mode = "MANUAL"
            elif event.key == pg.K_DOWN:
                self.run_speed = max(1, self.run_speed - 1)

            elif event.key == pg.K_UP:
                self.run_speed = min(self.run_speed + 1, 30)

    def update(self, surface, keys):
        if self.mode == "AUTOMATIC":
            if self.dt >= 1000.0 / self.run_speed:
                self.dt -= 1000.0 / self.run_speed
                self.world.update()
        self.world.draw(surface)



