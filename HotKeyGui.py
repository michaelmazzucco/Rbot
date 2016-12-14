# -*- coding: utf-8 -*-
"""
Created on Sun Dec 11 23:29:54 2016

@author: Mikes
"""

try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk

from pilotControl import pltInput




DIRECT_DICT = {'Up'    : ( 0,-1),
               'Down'  : ( 0, 1),
               'Left'  : (-1, 0),
               'Right' : ( 1, 0)}


class Sprite(object):
    def __init__(self, location, size):
        self.start_x, self.start_y = location
        self.width, self.height = size
        self.speed = 5
        self.rect = None

    def update(self, canvas, keys):

        x, y   = (511, 511)
        for key in DIRECT_DICT:
            if keys.get(key, False):
                x +=  DIRECT_DICT[key][0]*511
                y += DIRECT_DICT[key][1]*511

               
                
        if not self.rect:
            rect = (self.start_x, self.start_y,
                    self.start_x+self.width, self.start_y+self.height)
            self.rect = canvas.create_rectangle(rect, outline="green",
                                                fill="purple", width=2)
        else:
            canvas.move(self.rect, x/511-1, y/511-1)
            print(x)
            
        print(x)
        print(y)
        pltInput.setJoysticks(0,0,y,x)

class Control(object):
    def __init__(self):
        self.root = tk.Tk()
        self.canvas = tk.Canvas(self.root, width=1000, height=1000,
                                bg='dark slate gray')
        self.canvas.focus_set()
        self.canvas.bind("<Key>", self.key_pressed)
        self.canvas.bind("<KeyRelease>", self.key_released)
        self.canvas.pack()
        self.fps = 60
        self.player = Sprite((250,250), (50,50))
        self.pressed = {}

    def key_pressed(self, event):
        self.pressed[event.keysym] = True

    def key_released(self, event):
        self.pressed[event.keysym] = False

    def update(self):
        self.player.update(self.canvas, self.pressed)
        self.root.after(1000//self.fps, self.update)
        

    def main(self):
        self.update()
        self.root.mainloop()


if __name__ == "__main__":
    run_it = Control()
    run_it.main()
