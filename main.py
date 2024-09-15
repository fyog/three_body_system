import numpy as np
from interface import *
from system import *
from mass import *
from spaceship import *
from screen import *

COLLISIONS = False
SHOW_PATH = True
SHOW_MASSES = True
SHOW_UI = False
SHOW_CONTROLS = True
TIME_STEP = 0.1

def main():
    
    # window and interface creation
    win = GraphWin('Three-Body System', LENGTH, WIDTH)
    interface = Interface(win)
    screen = Screen('black',  interface)
    world_origin = win.toWorld(200, 400)
       
    # menu screen
    while not interface.begin_game:
        x, y = world_origin
        print (f'{x},{y}')
        screen.draw_menu_screen(x, y)
        interface.check()
        screen.undraw_menu_screen()

    # game instructions
    if SHOW_CONTROLS:
        controls = Text(Point(1425, 720), 'To restart the sim press r.\nTo pause press p.\nTo unpause press u.\nTo close the window press esc.')
        controls.setTextColor('white')
        controls.draw(win)
    
    # generate system
    spaceship = Spaceship(1., np.array([-20, 100, 0]), np.array([15, 5, 0]), 'darkblue', TIME_STEP)
    mass = Mass(350., np.array([800, 550, 0]), np.array([0, 0, 0]), 'yellow', TIME_STEP)
    system = System(win, interface, [spaceship, mass])

    # simulation loop
    while interface.running:
              
        # detect collisions
        if COLLISIONS:
            interface.collision_detected = spaceship.detect_collision(system)
                              
        # render masses
        if SHOW_MASSES:
            system.render()
           
        # render ui
        if SHOW_UI:
            position = Text(Point(120, 34), 'pos x: ' + str(spaceship.pos[0]) + '\npos y: ' + str(spaceship.pos[1]))
            position.setTextColor('white')
            position.draw(win)
            speed = Text(Point(121, 78), 'speed x: ' + str(spaceship.vel[0]) + '\nspeed y: ' + str(spaceship.vel[1]))
            speed.setTextColor('white')
            speed.draw(win)
            position.undraw()
            speed.undraw() 
                   
        # register player input
        interface.check()

        # apply movement
        spaceship.apply_thrust(interface) # thrust is tied to timestep

        # apply zoom
        if interface.zoom_in:
            print('zooming in')
        elif interface.zoom_out:
            print('zooming out')

        # slow motion
        if interface.slow_mo:
            spaceship.set_timestep(TIME_STEP / 10.)
        else:
            spaceship.set_timestep(TIME_STEP)

        # pause loop
        while interface.pause:
            interface.check() # update interface state

        # restart simulation
        if interface.restart:
            system = System(win, interface, [spaceship, mass])
            interface.restart = False
              
        # update masses
        if not interface.collision_detected:
            system.update()
        else:
            print('You crashed.')
            interface.pause = True

        # clear the screen and reset the interface toggles
        system.clear()
        interface.reset_state()

main()
