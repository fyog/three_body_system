import numpy as np
import math
from graphics import *

# constants
G = pow(10, 3) # gravitational constant
SCALE_FACTOR = 3.

class Mass:
   
    path_list_large = []
    path_list_med = []
    path_list_small = []

    # constructor
    def __init__(self, kg, pos, vel, colour, timestep):
        self.kg = kg
        self.pos = pos
        self.vel = vel
        self.radius = max(3., (math.log(kg)) * SCALE_FACTOR)
        self.colour = colour
        self.timestep = timestep

    # rightmost edge of a mass (w.r.t x-axis)
    def right(self):
        return self.pos[0] + self.radius
    
    # leftmost edge of a mass (w.r.t x-axis)
    def left(self):
        return self.pos[0] - self.radius
    
    # top edge of a mass (w.r.t y-axis)
    def top(self):
        return self.pos[1] - self.radius
    
    # bottom edge of a mass (w.r.t y-axis)
    def bot(self):
        return self.pos[1] + self.radius
    
    # front edge of a mass (w.r.t z-axis)
    def front(self):
        return self.pos[2] + self.radius
    
    # back edge of a mass (w.r.t z-axis)
    def back(self):
        return self.pos[2] - self.radius

    # adjust the timestep of individual masses
    def set_timestep(self, timestep):
        self.timestep = timestep

    # returns displacement vector between the given mass and the argument mass
    def displacement(self, mass):
        return np.array([mass.pos[0] - self.pos[0],
                         mass.pos[1] - self.pos[1],
                         mass.pos[2] - self.pos[2]])
    
    # set location and velocity
    def set_pos_vel(self, pos, vel):
        self.pos = pos
        self.vel = vel
    
    # determines force on the given mass as a result of another mass
    def force(self, mass):
        r = self.displacement(mass) 
        r_hat = r / np.linalg.norm(r) # unit vector
        r_mag = G * self.kg * mass.kg / pow(np.linalg.norm(r), 2) # magnitude of r
        return r_mag * r_hat
    
    # check for collisions
    def detect_collision(self, masses):  
        for mass in masses:
            if self != mass and self.right() - mass.left() > .0 and mass.right() - self.left() > .0 and self.top() - mass.bot() < 0 and mass.top() - self.bot() < 0 and self.front() - mass.back() > .0 and mass.front() - self.back() > .0:
                return True
        return False
                        
    # draws mass to the screen
    def draw(self, win):
        self.circle = Circle(Point(self.pos[0], self.pos[1]), self.radius)
        self.circle.setOutline(self.colour)
        self.circle.setFill(self.colour)
        self.circle.draw(win)

    # remove the mass from the screen
    def undraw(self):
        self.circle.undraw()

    # draws mass path trajectory
    def draw_path(self, win):
     
        # small pts
        path_pt_small = Point(self.pos[0], self.pos[1])
        path_pt_small.setOutline('white')
        self.path_list_small.append(path_pt_small)
        path_pt_small.draw(win)

        # medium pts
        path_pt_med = Circle(Point(self.pos[0], self.pos[1]), 1.3)
        path_pt_med.setOutline('lightblue')
        path_pt_med.setFill('purple')
        self.path_list_med.append(path_pt_med)
        path_pt_med.draw(win)

        # large pts
        path_pt_large = Circle(Point(self.pos[0], self.pos[1]), 2)
        path_pt_large.setOutline('blue')
        path_pt_large.setFill('blue')
        self.path_list_large.append(path_pt_large)
        path_pt_large.draw(win)

    # removes mass path trajectory from the screen
    def undraw_path(self):
        
        # small pts
        if len(self.path_list_small) > 75:
            self.path_list_small[0].undraw()
            self.path_list_small.pop(0)

        # med pts
        if len(self.path_list_med) > 50:
            self.path_list_med[0].undraw()
            self.path_list_med.pop(0)
        
        # large pts
        if len(self.path_list_large) > 25:
            self.path_list_large[0].undraw()
            self.path_list_large.pop(0)

    # updates the position and velocity of the given mass based on the current net force acting on it
    def update(self, masses):
        
        # calculate force on the given mass as a result of all other masses
        force = np.array([0., 0., 0.])
        for _ in masses:
            if _ != self:
                force += self.force(_)
        accel = force / self.kg

        # Newton's method
        self.vel = self.vel + accel * self.timestep
        self.pos = self.pos + self.vel * self.timestep
    

