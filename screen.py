from graphics import *

class Screen:

    # constructor
    def __init__(self, win, colour, interface):
        self.win = win
        self.colour = colour
        self.interface = interface
    
    # draws the menu screen, with the menu text at the given location
    def draw_menu(self, x, y):
        #self.win.setBackground(self.colour)
        self.start_screen = Text(Point(x, y), 'Press the b key to start the game.')
        self.start_screen.draw(self.win)

    # removes the current screen
    def undraw(self):
        self.start_screen.undraw()

    # adjust background colour of the screen
    '''def change_background_colour(self, colour):
        self.win.setBackground(colour)'''