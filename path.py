import mass as m
import graphics as gr

class Path:
    
    # constructor
    def __init__(self, mass):
        self.mass = mass
        
    # draws path trajectory
    def draw_path(self, win):
        
        # small pts
        path_pt_small = gr.Point(self.pos[0], self.pos[1], 0.02)
        path_pt_small.setOutline('blue')
        path_pt_small.setFill('blue')
        self.path_list_small.append(path_pt_small)
        path_pt_small.draw(win)

        # medium pts
        path_pt_med = gr.Circle(gr.Point(self.pos[0], self.pos[1]), 0.02)
        path_pt_med.setOutline('blue')
        path_pt_med.setFill('blue')
        self.path_list_med.append(path_pt_med)
        path_pt_med.draw(win)

        # large pts
        path_pt_large = gr.Circle(gr.Point(self.pos[0], self.pos[1]), .02)
        path_pt_large.setOutline('blue')
        path_pt_large.setFill('blue')
        self.path_list_large.append(path_pt_large)
        path_pt_large.draw(win)
        
    # remove path trajectory from the screen
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
            
            
