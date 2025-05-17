import numpy as np
import interface as intr
import system as sys
import mass as m
import spaceship as s
import graphics as gr
import screen as scr

COLLISIONS = False
SHOW_PATH = True
SHOW_MASSES = True
SHOW_UI = False
SHOW_CONTROLS = True
TIME_STEP = 0.1

def main():
    
    # window and interface creation
    win = gr.GraphWin('Three-Body System', 1600, 800)
    interface = intr.Interface(win)
    screen = scr.Screen('black',  interface)
    
    origin_screen = win.toScreen(800, 400) # find the world origin in screen coordinates
    x, y = origin_screen
    #print("x: " + str(x) + ",y: " + str(y))

    # menu screen
    while not interface.begin_game:
        screen.draw_menu_screen(x, y)
        interface.check()
       
    print("triggered")
    #6screen.undraw() # is not undrawing the menu screen

    # game instructions
    if SHOW_CONTROLS:
        controls = gr.Text(gr.Point(800, 300), 'To restart the sim press r.\nTo pause press p.\nTo unpause press u.\nTo close the window press esc.')
        controls.setTextColor('white')
    
    # generate system
    coords = win.toScreen(-20., -20.)
    x, y = coords
    spaceship = s.Spaceship(1., np.array([x , y,  0]), np.array([15, 5, 0]), 'darkblue', TIME_STEP)
    mass = m.Mass(350., np.array([800, 550, 0]), np.array([0, 0, 0]), 'yellow', TIME_STEP)
    system = sys.System(win, interface, [spaceship, mass])

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
            position = gr.Text(gr.Point(120, 34), 'pos x: ' + str(spaceship.pos[0]) + '\npos y: ' + str(spaceship.pos[1]))
            position.setTextColor('white')
            position.draw(win)
            speed = gr.Text(gr.Point(121, 78), 'speed x: ' + str(spaceship.vel[0]) + '\nspeed y: ' + str(spaceship.vel[1]))
            speed.setTextColor('white')
            speed.draw(win)
            position.undraw()
            speed.undraw() 
                   
        # register player input
        interface.check()

        # apply zoom
        if interface.zoom_in:
            print('zooming in')
        elif interface.zoom_out:
            print('zooming out')

        # slow motion
        if interface.slow_mo:
            spaceship.set_timestep(TIME_STEP / 10.)
            interface.slow_mo = False
        else:
            spaceship.set_timestep(TIME_STEP)

        # pause loop
        while interface.pause:
            interface.check() # update interface state

        # restart simulation
        if interface.restart:
            spaceship = s.Spaceship(1., np.array([-20, 100, 0]), np.array([15, 5, 0]), 'darkblue', TIME_STEP)
            mass = m.Mass(350., np.array([800, 550, 0]), np.array([0, 0, 0]), 'yellow', TIME_STEP)
            system = sys.System(win, interface, [spaceship, mass])
            interface.restart = False
              
        # update masses
        if not interface.collision_detected:
            system.update()
        else:
            print('You crashed.')
            interface.pause = True

        # apply movement
        spaceship.apply_thrust(interface) # thrust is a function of timestep

        # clear the screen and reset the interface toggles
        #system.clear()
        #interface.reset_state()

main()
