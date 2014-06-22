from random import choice, randint
from collections import defaultdict
import pygame as pg
from .critters import Fish, Shark

class Cell(object):
    def __init__(self, index):
        self.index = index
        self.occupant = None

        
class World(object):
    def __init__(self, cells_wide, cells_high, cell_size, num_fish, num_sharks,
                        fish_fert_age, shark_fert_age, shark_belly_size):
        self.grid = {(x, y): Cell((x, y)) for x in range(cells_wide) for y in range(cells_high)}
        self.cells_wide = cells_wide
        self.cells_high = cells_high
        self.cell_size = cell_size
        self.fish_fert_age = fish_fert_age
        self.shark_fert_age = shark_fert_age
        self.shark_belly_size = shark_belly_size
        
        self.fishies = []
        self.tick_count = 0
        self.stats = {}
        
        for f in range(num_fish):
            open_indices = [x for x in self.grid.keys() if self.grid[x].occupant is None]
            new_fish = Fish(choice(open_indices), self)
            new_fish.age = randint(0, new_fish.fertility_age)
            self.fishies.append(new_fish)
            self.grid[new_fish.index].occupant = new_fish            
        self.sharks = []
        for s in range(num_sharks):
            open_indices = [x for x in self.grid if self.grid[x].occupant is None]
            new_shark = Shark(choice(open_indices), self)
            new_shark.age = randint(0, new_shark.fertility_age)
            self.sharks.append(new_shark)
            self.grid[new_shark.index].occupant = new_shark
            
    def report(self, dead_sharks):
        self.stats[self.tick_count] = {}
        avg_belly = sum([x.belly for x in self.sharks]) / max(1.0, float(len(self.sharks)))
        fish_age = sum([x.age for x in self.fishies]) / max(1.0, float(len(self.fishies)))
        shark_age = sum([x.age for x in self.sharks]) / max(1.0, float(len(self.sharks)))
        new_stats = [("Fish", len(self.fishies)),
                            ("Sharks", len(self.sharks) - len(dead_sharks)),
                            ("Avergae Shark Belly", avg_belly),
                            ("Average Shark Age", shark_age),
                            ("Average Fish Age", fish_age),
                            ("Fish Births", len(self.new_fishies)),
                            ("Shark Births", len(self.new_sharks)),
                            ("Shark Deaths", len(dead_sharks))]
        
        for stat in new_stats:
            self.stats[self.tick_count][stat[0]] = stat[1]
    
    def update(self):
        self.new_fishies = []
        self.new_sharks = []
       
        for fish in self.fishies:
            fish.update(self)
        for shark in self.sharks:
            shark.update(self)
        dead_sharks = [x for x in self.sharks if x.dead]
        self.report(dead_sharks)
        for dead in dead_sharks:
            self.grid[dead.index].occupant = None
            self.sharks.remove(dead)
        self.fishies = [x for x in self.fishies if not x.dead]          
        self.fishies.extend([x for x in self.new_fishies if not x.dead])
        self.sharks.extend(self.new_sharks)
        
        self.tick_count += 1

        
    def draw(self, surface):
        surface.fill(pg.Color("blue"))
        for fish in self.fishies:
            fish.draw(surface)
        for shark in self.sharks:
            shark.draw(surface)
        
        