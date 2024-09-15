from graphics import *

class Screen:

    # constructor
    def __init__(self, colour, interface):
        self.colour = colour
        self.interface = interface
        self.interface.win.setBackground(colour)
        
    # draws the menu screen, with the menu text at the given location
    def draw_menu_screen(self, x, y):
        self.start_screen = Text(Point(x, y), 'Press the b key to start the game.')
        self.start_screen.setTextColor ('white')
        self.start_screen.draw(self.interface.win)

    # undraw the menu screen
    def undraw_menu_screen(self):
        self.start_screen.undraw()

    # removes the current screen
    def undraw(self):
        self.start_screen.undraw()