import keyboard as key
 
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
        if key.is_pressed('p'): self.pause = True 
        if key.is_pressed('u'): self.pause = False
        if key.is_pressed('r'): self.restart = True
        if key.is_pressed('esc'): self.running, self.pause, self.restart, self.collision_detected = False, False, False, False
        if key.is_pressed('left'): self.thrust_dir = 'left'
        if key.is_pressed('right'): self.thrust_dir = 'right'
        if key.is_pressed('up'): self.thrust_dir = 'up'
        if key.is_pressed('down'): self.thrust_dir = 'down'
        if key.is_pressed('b'): self.begin_game = True
        if key.is_pressed('space'): self.slow_mo = True

        # mouse vars
        if self.on_scroll == 'in': self.zoom_in = True
        if self.on_scroll == 'out': self.zoom_out = True

    # defines how mouse scrollwheel actions are interpreted by this interface
    def on_scroll(self, event):
        if event.delta > 0:
            print(text = 'scrolled up')
            return 'in'
        else:
            print(text = 'scrolled down')
            return 'out'
