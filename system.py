# represents the universe
class System:

    # constructor
    def __init__(self, win, interface, masses):
        self.win, self.interface, self.masses = win, interface, masses

    # render the system
    def render(self):
        for _ in self.masses:
            _.draw(self.win)
            #_.draw_path(self.win)

    # add another mass to the system
    def add_mass(self, mass):
        self.masses.add(mass)

    # remove the given mass from the system
    def remove_mass(self, mass):
        for _ in self.masses:
            if _ == mass:
                self.masses.remove(mass)

    # updates all the masses in the system
    def update(self, time):
        for _ in self.masses:
            _.update(self.masses, time)

    # clear the system from the screen
    def clear(self):
        for _ in self.masses:
            _.undraw()
            #_.undraw_path()

    # reset the system to its initial state
    def reset(self):
        for _ in self.masses:
            print('implement')