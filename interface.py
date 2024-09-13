import keyboard
from graphics import *
import tkinter as tk

LENGTH = 1600
WIDTH = 800

class Interface():

    # constructor
    def __init__(self, win):
        self.win = win
        self.start, self.running, self.pause, self.restart, self.collision_detected, self.begin_game, self.slow_mo, self.zoom_in, self.zoom_out = False, True, False, False, False, False, False, False, False
        self.thrust_dir = ''
    
    # reset the state of the keyboard/mouse interface
    def reset_state(self):
        self.start, self.running, self.pause, self.restart, self.collision_detected, self.begin_game, self.slow_mo, self.zoom_in, self.zoom_out = False, True, False, False, False, False, False, False, False
        self.thrust_dir = ''

    # check the current state of the keyboard/mouse interface
    def check(self):
        
        # keyboard vars
        if keyboard.is_pressed('p'): self.pause = True 
        if keyboard.is_pressed('u'): self.pause = False
        if keyboard.is_pressed('r'): self.restart = True
        if keyboard.is_pressed('esc'): self.running, self.pause, self.restart, self.collision_detected = False, False, False, False
        if keyboard.is_pressed('left'): self.thrust_dir = 'left'
        if keyboard.is_pressed('right'): self.thrust_dir = 'right'
        if keyboard.is_pressed('up'): self.thrust_dir = 'up'
        if keyboard.is_pressed('down'): self.thrust_dir = 'down'
        if keyboard.is_pressed('b'): self.begin_game = True
        if keyboard.is_pressed('space'): self.slow_mo = True

        # mouse vars
        #self.win._root.bind
        if self.on_scroll == 'in': self.zoom_in = True
        if self.on_scroll == 'out': self.zoom_out = True

    # defines how mouse scrollwheel actions are interpreted by this interface
    def on_scroll(self,event):
        if event.delta > 0:
            print(text="Scrolled Up")
            return 'in'
        else:
            print(text="Scrolled Down")
            return 'out'
