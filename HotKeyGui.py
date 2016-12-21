# -*- coding: utf-8 -*-
"""
Created on Sun Dec 11 23:29:54 2016

@author: Mikes
"""

import win32gui 

try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk

from pilotControl import pltInput
MAXINPUT = 1023



DIRECT_DICT = {'A'    : ( 0,-1),
               'D'  : ( 0, 1),
               'W'  : (-1, 0),
               'S' : ( 1, 0)}


class Sprite(object):
    def __init__(self, location, size):
        self.start_x, self.start_y = location
        self.width, self.height = size
        self.speed = 5
        self.rect = None

    def update(self, canvas, keys):

        x, y   = (1, 1)
        
        #flags, hcursor, (x,y) = win32gui.GetCursorInfo()        
       
             
        if (keys.get('W') == True or keys.get('w') == True):  
            pltInput.MoveFwd(MAXINPUT)
            y +=  -1
        elif (keys.get('S') == True or keys.get('s')  == True):        
            pltInput.MoveBack(0)
            y += 1
        else:
            pltInput.MoveFwd(511)
            
        if (keys.get('Up') == True):  
            print("Turret Up")
            pltInput.setTurretUp()      
        elif (keys.get('Down') == True):  
            pltInput.setTurretDown() 
        else:
            pltInput.unsetTurretUp() 
            pltInput.unsetTurretDown()
        
            
            
        if (keys.get('Left') == True):  
            print("Turret Up")
            pltInput.setTurretLeft()      
        elif (keys.get('Right') == True):  
            pltInput.setTurretRight() 
        else:
            pltInput.unsetTurretLeft() 
            pltInput.unsetTurretRight()
            
            
            
        if (keys.get('Q') == True  or keys.get('q') == True ):
            pltInput.MoveTurnLeft(MAXINPUT)
        elif (keys.get('E') == True  or keys.get('e') == True ):
            pltInput.MoveTurnRight(0) 
        elif (keys.get('A') == True  or keys.get('a') == True ):            
            pltInput.MoveStrafeLeft(MAXINPUT)
            x += -1          
        elif (keys.get('D') == True  or keys.get('d') == True ):
            pltInput.MoveStrafeRight(0)
            x += 1
        else:
            pltInput.MoveTurnRight(511)

            
            
            
            
            
        if (keys.get(1) == True ):
            pltInput.set_Fire()
        else:
            pltInput.unset_Fire()
                

            
            
        if (keys.get('F1') == True ):
            pltInput.set_Arm()
        else:
            pltInput.unset_Arm()    
            
            
        if not self.rect:
            rect = (self.start_x, self.start_y,
                    self.start_x+self.width, self.start_y+self.height)
            self.rect = canvas.create_rectangle(rect, outline="green",
                                                fill="purple", width=2)
        else:
            canvas.move(self.rect, x-1, y-1)
            print(x)
 

class Control(object):
    def __init__(self):
        self.root = tk.Tk()
        self.canvas = tk.Canvas(self.root, width=1000, height=1000,
                                bg='dark slate gray')
        self.canvas.focus_set()
        self.canvas.bind("<Key>", self.key_pressed)
        self.canvas.bind("<KeyRelease>", self.key_released)
        self.canvas.bind("<Button-1>", self.Mouse1_pressed)
        self.canvas.bind("<ButtonRelease-1>", self.Mouse1_released)
        self.canvas.pack()
        self.fps = 60
        self.player = Sprite((250,250), (50,50))
        self.pressed = {}
        self.mouseclick = {}

    def Mouse1_pressed(self, event):
        self.pressed[event.num] = True

    def Mouse1_released(self, event):
        self.pressed[event.num] = False
        
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
