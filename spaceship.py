import mass

class Spaceship(mass.Mass):

    # constructor (add interface to the constructor)
    def _init_(self, kg, pos, vel, colour, timestep):
        mass.Mass.__init__(self, kg, pos, vel, colour, timestep)

    # applies thrust to the spaceship based on keyboard presses
    def apply_thrust(self, interface):
        if (interface.thrust_dir == 'left'):
            self.vel += (-10. * self.timestep, .0, .0)
        if (interface.thrust_dir == 'right'):
            self.vel += (10. * self.timestep, .0, .0)
        if (interface.thrust_dir == 'up'):
            self.vel += (.0, -10. * self.timestep, .0)
        if (interface.thrust_dir == 'down'):
            self.vel += (.0, 10. * self.timestep, .0)
