import os
import json
import pygame as pg


class Control(object):
    def __init__(self, caption):
        self.screen = pg.display.get_surface()
        self.caption = caption
        self.done = False
        self.clock = pg.time.Clock()
        self.show_fps = True
        self.keys = pg.key.get_pressed()
        self.state_dict = {}
        self.state_name = None
        self.state = None
        self.fullscreen = False

    def setup_states(self, state_dict, start_state):
        self.state_dict = state_dict
        self.state_name = start_state
        self.state = self.state_dict[self.state_name]

    def update(self):
        if self.state.quit:
            self.done = True
        elif self.state.done:
            self.flip_state()
        self.state.update(self.screen, self.keys)


    def flip_state(self):
        previous,self.state_name = self.state_name, self.state.next
        persist = self.state.cleanup()
        self.state = self.state_dict[self.state_name]
        self.state.startup(persist)
        self.state.previous = previous

    def event_loop(self):
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                self.keys = pg.key.get_pressed()
                self.toggle_show_fps(event.key)
                self.toggle_fullscreen(event.key)
            elif event.type == pg.KEYUP:
                self.keys = pg.key.get_pressed()
            self.state.get_event(event)

    def toggle_show_fps(self, key):
        if key == pg.K_F5:
            self.show_fps = not self.show_fps
            if not self.show_fps:
                pg.display.set_caption(self.caption)
    
    def toggle_fullscreen(self, key):
        if key == pg.K_f:
            self.fullscreen = not self.fullscreen
            if self.fullscreen:
                pg.display.set_mode(self.screen.get_rect().size, pg.FULLSCREEN)
            else:
                pg.display.set_mode(self.screen.get_rect().size)
    
    
    def main(self):
        while not self.done:
            self.state.dt += self.clock.tick(self.state.fps)
            self.event_loop()
            
            
            self.update()
            pg.display.update()
            if self.show_fps:
                fps = self.clock.get_fps()
                with_fps = "{} - {:.2f} FPS".format(self.caption, fps)
                if hasattr(self.state, "run_speed"):
                    with_fps = "{}  Run FPS: {}".format(with_fps, self.state.run_speed) 

                pg.display.set_caption(with_fps)
            

class _State(object):
    def __init__(self):
        self.fps = 60
        self.done = False
        self.quit = False
        self.next = None
        self.previous = None
        self.persist = {}
        self.dt = 0.0

    def get_event(self, event):
        pass

    def startup(self, persistent):
        self.persist = persistent

    def cleanup(self):
        self.done = False
        return self.persist

    def update(self, surface, keys):
        pass




def load_all_gfx(directory,colorkey=(0,0,0),accept=(".png",".jpg",".bmp")):
    graphics = {}
    for pic in os.listdir(directory):
        name,ext = os.path.splitext(pic)
        if ext.lower() in accept:
            img = pg.image.load(os.path.join(directory, pic))
            if img.get_alpha():
                img = img.convert_alpha()
            else:
                img = img.convert()
                img.set_colorkey(colorkey)
            graphics[name]=img
    return graphics


def load_all_music(directory, accept=(".wav", ".mp3", ".ogg", ".mdi")):
    songs = {}
    for song in os.listdir(directory):
        name,ext = os.path.splitext(song)
        if ext.lower() in accept:
            songs[name] = os.path.join(directory, song)
    return songs

def load_words(directory, accept=(".txt")):
    words = {}
    for word in os.listdir(directory):
        name, ext = os.path.splitext(word)
        if ext.lower() in accept:
            with open(os.path.join(directory, word), "r") as f:
                words[name] = [str(x).strip() for x in f.readlines()]
    return words
            
def load_all_sfx(directory, accept=(".wav", ".mp3", ".ogg", ".mdi")):
    effects = {}
    for fx in os.listdir(directory):
        name,ext = os.path.splitext(fx)
        if ext.lower() in accept:
            effects[name] = pg.mixer.Sound(os.path.join(directory, fx))
    return effects

def load_all_fonts(directory, accept=(".ttf")):
    return load_all_music(directory, accept)