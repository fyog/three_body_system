import graphics as gr

class Screen:

    # constructor
    def __init__(self, colour, interface):
        self.colour = colour
        self.interface = interface
        self.interface.win.setBackground(colour)
        
    # draws the menu screen, with the menu text at the given location
    def draw_menu_screen(self, x, y):
        self.start_menu = gr.Text(gr.Point(x, y), 'Press the b key to start the game.')
        self.start_menu.setTextColor ('white')
        self.start_menu.draw(self.interface.win)


    # removes the current screen
    def undraw(self):
        self.start_menu.undraw()