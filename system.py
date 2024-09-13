from mass import *
from graphics import *
from interface import *

class System:

    # constructor
    def __init__(self, win, interface, masses):
        self.win, self.interface, self.masses = win, interface, masses

    # render the system
    def render(self):
        for _ in self.masses:
            _.draw(self.win)
            _.draw_path(self.win)

    # add another mass to the system
    def add_mass(self, mass):
        self.masses.add(mass)

    # remove the given mass from the system
    def remove_mass(self, mass):
        for _ in self.masses:
            if _ == mass:
                self.masses.remove(mass)

    # updates all the masses in the system
    def update(self):
        for _ in self.masses:
            _.update(self.masses)

    # clear the system from the screen
    def clear(self):
        for _ in self.masses:
            _.undraw()
            _.undraw_path()

    # def reset(self):
