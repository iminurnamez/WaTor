from random import choice
import pygame as pg
from .. import prepare

class Critter(object):
    directs = {(-1, 0): "left",
                    (1, 0): "right",
                    (0, -1): "up",
                    (0, 1): "down"}
    def __init__(self, name, index, world):
        self.dead = False
        self.age = 0
        self.name = name
        self.index = index
        self.cell_size = world.cell_size
        self.direction = "up"


    def get_neighbors(self, world):
        offsets = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        return [world.grid[((self.index[0] + x[0]) % world.cells_wide,
                                    (self.index[1] + x[1]) % world.cells_high)]
                                    for x in offsets]

    def get_direction(self, cell):
        horiz = cell.index[0] - self.index[0]
        if horiz > 0:
            horiz = 1
        elif horiz < 0:
            horiz = -1
        vert = cell.index[1] - self.index[1]
        if vert > 0:
            vert = 1
        elif vert < 0:
            vert = -1
        self.direction = self.directs[(horiz, vert)]

    def draw(self, surface):
        surface.blit(prepare.GFX[self.name + self.direction],
                         ((self.index[0] * self.cell_size,
                            self.index[1] * self.cell_size)))


class Fish(Critter):
    def __init__(self, index, world):
        super(Fish, self).__init__("fish", index, world)
        self.fertility_age = world.fish_fert_age
        self.pregnant = False

    def get_open_neighbors(self, world):
        neighbors = self.get_neighbors(world)
        return [x for x in neighbors if x.occupant is None]

    def enter_cell(self, cell, world):
        self.get_direction(cell)
        if self.pregnant:
            new_fish = Fish(self.index, world)
            world.grid[self.index].occupant = new_fish
            self.age = 0
            self.pregnant = False
            world.new_fishies.append(new_fish)
        else:
            world.grid[self.index].occupant = None
        world.grid[cell.index].occupant = self
        self.index = cell.index

    def update(self, world):
        if not self.dead:
            self.age += 1
            if self.age >= self.fertility_age:
                self.pregnant = True
            moves = self.get_open_neighbors(world)
            if moves:
                self.enter_cell(choice(moves), world)




class Shark(Critter):
    def __init__(self, index, world):
        super(Shark, self).__init__("shark", index, world)
        self.fertility_age = world.shark_fert_age
        self.pregnant = False
        self.max_belly = world.shark_belly_size
        self.belly = self.max_belly


    def get_open_neighbors(self, world):
        neighbors = self.get_neighbors(world)
        return [x for x in neighbors if x.occupant is None or x.occupant.name == "fish"]

    def update(self, world):
        self.age += 1
        if self.age >= self.fertility_age:
            self.pregnant = True
        self.belly -= 1
        if self.belly <= 0:
            self.dead = True


        neighbors = self.get_open_neighbors(world)
        food = [x for x in neighbors if not x.occupant is None]

        if food:
            moves = food
        elif neighbors:
            moves = neighbors
        else:
            moves = None
        if moves is not None:
            self.enter_cell(world, choice(moves))

    def enter_cell(self, world, cell):
        self.get_direction(cell)
        if (cell.occupant is not None
             and not cell.occupant.dead):
            self.belly = self.max_belly
            cell.occupant.dead = True
        if self.pregnant:
            new_shark = Shark(self.index, world)
            world.new_sharks.append(new_shark)
            world.grid[self.index].occupant = new_shark
            self.age = 0
            self.pregnant = False
        else:
            world.grid[self.index].occupant = None
        cell.occupant = self
        self.index = cell.index

