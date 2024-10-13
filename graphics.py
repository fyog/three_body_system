import time, os, sys
import tkinter as tk

# constants
WIDTH = 1600
HEIGHT = 800

# open up root tkinter window
root = tk.Tk()
root.withdraw()

#_update_lasttime = time.time()

'''
def update(rate=None):
    global _update_lasttime
    if rate:
        now = time.time()
        pauseLength = 1/rate-(now-_update_lasttime)
        if pauseLength > 0:
            time.sleep(pauseLength)
            _update_lasttime = now + pauseLength
        else:
            _update_lasttime = now

    root.update()
'''

# GraphWin ------------------------------------------------------------------------------------------------------------
class GraphWin(tk.Canvas):

    # constructor
    def __init__(self, title="Graphics Window",
                 width=200, height=200, autoflush=True):
        #assert type(title) == type(""), "Title must be a string"
        master = tk.Toplevel(root)
        master.protocol("WM_DELETE_WINDOW", self.close)
        tk.Canvas.__init__(self, master, width=width, height=height,
                           highlightthickness=0, bd=0)
        self.master.title(title)
        self.pack()
        master.resizable(0,0)
        self.foreground = "black"
        self.items = []
        self.mouseX = None
        self.mouseY = None
        self.bind("<Button-1>", self._onClick)
        self.bind_all("<Key>", self._onKey)
        self.height = int(height)
        self.width = int(width)
        self.autoflush = autoflush
        self._mouseCallback = None
        self.trans = None
        self.closed = False
        master.lift()
        self.lastKey = ""
        if autoflush: root.update()
    
    # unambiguous representation of the object state
    def __repr__(self):
        if self.isClosed():
            return "<Closed GraphWin>"
        else:
            return "GraphWin('{}', {}, {})".format(self.master.title(),
                                             self.getWidth(),
                                             self.getHeight())

    # readable representation of the object currently
    def __str__(self):
        return repr(self)
     
    '''def __checkOpen(self):
        if self.closed:
            raise GraphicsError("window is closed")'''
    
    def _onKey(self, evnt):
        self.lastKey = evnt.keysym

    # set background color
    def setBackground(self, color):
        #self.__checkOpen()
        self.config(bg=color)
        self.__autoflush()

    # set coordinates of window to run from (x1,y1) in the lower-left corner to (x2,y2) in the upper-right corner.
    def setCoords(self, x1, y1, x2, y2):
        self.trans = Transform(self.width, self.height, x1, y1, x2, y2)
        self.redraw()

    # close the window
    def close(self):
        if self.closed: return
        self.closed = True
        self.master.destroy()
        self.__autoflush()

    # checks if window is currently closed
    def isClosed(self):
        return self.closed

    # checks if window is currently open
    def isOpen(self):
        return not self.closed

    # ?
    def __autoflush(self):
        if self.autoflush:
            root.update()
    
    # plots a single pixel with the given color
    def plot(self, x, y, color="black"):
        self.__checkOpen()
        xs,ys = self.toScreen(x,y)
        self.create_line(xs,ys,xs+1,ys, fill=color)
        self.__autoflush()
    
    # plots a single pixel with the given color (raw, independent of window coordinates)
    def plotPixel(self, x, y, color="black"):
        self.__checkOpen()
        self.create_line(x,y,x+1,y, fill=color)
        self.__autoflush()
    
    # update drawing to the window
    def flush(self):
        self.__checkOpen()
        self.update_idletasks()
    
    # wait for mouse click and return 0-d Point object representing the click location
    def getMouse(self):
        self.update()      # flush any prior clicks
        self.mouseX = None
        self.mouseY = None
        while self.mouseX == None or self.mouseY == None:
            self.update()
            #if self.isClosed(): raise GraphicsError("getMouse in closed window")
            time.sleep(.1) # give up thread
        x,y = self.toWorld(self.mouseX, self.mouseY)
        self.mouseX = None
        self.mouseY = None
        return Point(x,y)

    # returns the last mouse click position, as 0-d Point, or None if no mouse click has occured since the last call
    def checkMouse(self):
        if self.isClosed():
            self.update()
        if self.mouseX != None and self.mouseY != None:
            x,y = self.toWorld(self.mouseX, self.mouseY)
            self.mouseX = None
            self.mouseY = None
            return Point(x,y)
        else:
            return None

    # wait for key press and return appropriate string
    def getKey(self):
        self.lastKey = ""
        while self.lastKey == "":
            self.update()
            #if self.isClosed(): raise GraphicsError("getKey in closed window")
            time.sleep(.1) # give up thread

        key = self.lastKey
        self.lastKey = ""
        return key

    # checks and returns the last key that was pressed or None is nothing was pressed since the last function call
    def checkKey(self):
        if self.isClosed():
            #raise GraphicsError("checkKey in closed window")
            self.update()
        key = self.lastKey
        self.lastKey = ""
        return key

    # returns window height     
    def getHeight(self):
        return self.height
    
    # returns window width
    def getWidth(self):
        return self.width
    
    # converts 2-d world coords to screen coords
    def toScreen(self, x, y):
        return x + (WIDTH / 2.), -(y - (HEIGHT / 2.))
        
        # original method below
        '''trans = self.trans
        if trans:
            return self.trans.screen(x,y)
        else:
            return x,y'''

    # converts 2-d screen coords to world coords
    def toWorld(self, x, y):
        return x - (WIDTH / 2.), -(y - (HEIGHT / 2.))

        # original method below
        '''trans = self.trans
        if trans:
            return self.trans.world(x,y)
        else:
            return x,u'''
    
    # sets a specific function as the func that will be executed by the mouse handler event
    def setMouseHandler(self, func):
        self._mouseCallback = func
    
    # ?
    def _onClick(self, e):
        self.mouseX = e.x
        self.mouseY = e.y
        if self._mouseCallback:
            self._mouseCallback(Point(e.x, e.y))

    # append to the list of items in the window
    def addItem(self, item):
        self.items.append(item)


    # delete an itemm from the list of items in the window
    def delItem(self, item):
        self.items.remove(item)

    # redraw the entire window
    def redraw(self):
        for item in self.items[:]:
            item.undraw()
            item.draw(self)
        self.update()
        
# Transform -----------------------------------------------------------------------------------------------------------     
class Transform:
   
    def __init__(self, w, h, xlow, ylow, xhigh, yhigh):
        # w, h are width and height of window
        # (xlow,ylow) coordinates of lower-left [raw (0,h-1)]
        # (xhigh,yhigh) coordinates of upper-right [raw (w-1,0)]
        xspan = (xhigh-xlow)
        yspan = (yhigh-ylow)
        self.xbase = xlow
        self.ybase = yhigh
        self.xscale = xspan/float(w-1)
        self.yscale = yspan/float(h-1)
        
    def screen(self,x,y):
        # returns x,y in screen (actually window) coordinates
        xs = (x-self.xbase) / self.xscale
        ys = (self.ybase-y) / self.yscale
        return int(xs+0.5),int(ys+0.5)
        
    def world(self,xs,ys):
        # returns xs,ys in world coordinates
        x = xs*self.xscale + self.xbase
        y = ys*self.yscale - self.ybase
        return x,y


# Default values for various item configuration options. Only a subset of
# keys may be present in the configuration dictionary for a given item
DEFAULT_CONFIG = {"fill":"",
      "outline":"black",
      "width":"1",
      "arrow":"none",
      "text":"",
      "justify":"center",
                  "font": ("helvetica", 12, "normal")}

# GraphicsObject ------------------------------------------------------------------------------------------------------
class GraphicsObject:

    # all subclasses of GraphicsObject should override draw and
    # and move methods.
    
    # constructor
    def __init__(self, options):
        # options is a list of strings indicating which options are
        # legal for this object.
        
        # When an object is drawn, canvas is set to the GraphWin(canvas)
        # object where it is drawn and id is the TK identifier of the
        # drawn shape.
        self.canvas = None
        self.id = None

        # config is the dictionary of configuration options for the widget.
        config = {}
        for option in options:
            config[option] = DEFAULT_CONFIG[option]
        self.config = config
    
    # set interior color to given color
    def setFill(self, color):
        
        self._reconfig("fill", color)
    
    # set outline color to given color
    def setOutline(self, color):
        self._reconfig("outline", color)
    
    # set line weight to width
    def setWidth(self, width):
        self._reconfig("width", width)

    # draw the object in graphwin, which should be a GraphWin object. A GraphicsObject may only be drawn into one
    # window. Raises an error if attempt made to draw an object that
    # is already visible.
    def draw(self, graphwin):
        #if self.canvas and not self.canvas.isClosed(): raise GraphicsError(OBJ_ALREADY_DRAWN)
        #if graphwin.isClosed(): raise GraphicsError("Can't draw to closed window")
        self.canvas = graphwin
        self.id = self._draw(graphwin, self.config)
        graphwin.addItem(self)
        if graphwin.autoflush:
            root.update()
        return self

    # undraw the object (i.e. hide it). Returns silently if the object is not currently drawn.    
    def undraw(self):
        if not self.canvas: return
        if not self.canvas.isClosed():
            self.canvas.delete(self.id)
            self.canvas.delItem(self)
            if self.canvas.autoflush:
                root.update()
        self.canvas = None
        self.id = None

    # move object by dx, dy
    def move(self, dx, dy):       
        self._move(dx,dy)
        canvas = self.canvas
        if canvas and not canvas.isClosed():
            trans = canvas.trans
            if trans:
                x = dx / trans.xscale 
                y = -dy / trans.yscale
            else:
                x = dx
                y = dy
            self.canvas.move(self.id, x, y)
            if canvas.autoflush:
                root.update()

    # Internal method for changing configuration of the object. Will
    # raise an error if the option does not exist in the config dictionary for this object
    # ?     
    def _reconfig(self, option, setting):
     
        #if option not in self.config:
            #raise GraphicsError(UNSUPPORTED_METHOD)
        options = self.config
        options[option] = setting
        if self.canvas and not self.canvas.isClosed():
            self.canvas.itemconfig(self.id, options)
            if self.canvas.autoflush:
                root.update()

    # draws appropriate figure on canvas with options provided and returns Tk id of item drawn
    def _draw(self, canvas, options):
        pass # must override in subclass
  
    # overwritten method - updates internal state of object to move it dx, dy units
    def _move(self, dx, dy):
        pass # must override in subclass

# Point ---------------------------------------------------------------------------------------------------------------
class Point(GraphicsObject):
    def __init__(self, x, y):
        GraphicsObject.__init__(self, ["outline", "fill"])
        self.setFill = self.setOutline
        self.x = float(x)
        self.y = float(y)

    # unambiguous representation of the object state
    def __repr__(self):
        return "Point({}, {})".format(self.x, self.y)
    
    # readable representation of the object state
    def _draw(self, canvas, options):
        x,y = canvas.toScreen(self.x,self.y)
        return canvas.create_rectangle(x, y , x+1, y+1, options)

    # move the Point by dx, dy
    def _move(self, dx, dy):
        self.x = self.x + dx
        self.y = self.y + dy
    
    # clones the curent Point object
    def clone(self):
        other = Point(self.x, self.y)
        other.config = self.config.copy()
        return other

    # returns x-coord of the given point  
    def getX(self): return self.x

    # returns y-coord of the given point
    def getY(self): return self.y

# Bounding box class (box defined by opposite corners)
class _BBox(GraphicsObject):
  
    # constructor
    def __init__(self, p1, p2, options=["outline","width","fill"]):
        GraphicsObject.__init__(self, options)
        self.p1 = p1.clone()
        self.p2 = p2.clone()

    # moves the BBox by dx, dy
    def _move(self, dx, dy):
        self.p1.x = self.p1.x + dx
        self.p1.y = self.p1.y + dy
        self.p2.x = self.p2.x + dx
        self.p2.y = self.p2.y  + dy

    # returns a 0-d point at the top right corner of the bounding box object     
    def getP1(self): return self.p1.clone()

    # returns a 0-d point at the bottom left corner of the bounding box object
    def getP2(self): return self.p2.clone()
    
    # returns a 0-d point at the center of the bounding box object
    def getCenter(self):
        p1 = self.p1
        p2 = self.p2
        return Point((p1.x+p2.x)/2.0, (p1.y+p2.y)/2.0)

# Rectangle ----------------------------------------------------------------------------------------------------------- 
class Rectangle(_BBox):
    
    # constructor
    def __init__(self, p1, p2):
        _BBox.__init__(self, p1, p2)

    # unambiguous representation of the object state
    def __repr__(self):
        return "Rectangle({}, {})".format(str(self.p1), str(self.p2))
    
    # draw the given Rectangle object 
    def _draw(self, canvas, options):
        p1 = self.p1
        p2 = self.p2
        x1,y1 = canvas.toScreen(p1.x,p1.y)
        x2,y2 = canvas.toScreen(p2.x,p2.y)
        return canvas.create_rectangle(x1,y1,x2,y2,options)

    # clones the curent Rectangle object
    def clone(self):
        other = Rectangle(self.p1, self.p2)
        other.config = self.config.copy()
        return other

# Oval ----------------------------------------------------------------------------------------------------------------
class Oval(_BBox):
    
    # constructor, using BBox class
    def __init__(self, p1, p2):
        _BBox.__init__(self, p1, p2)

    # unambiguous representation of the object state
    def __repr__(self):
        return "Oval({}, {})".format(str(self.p1), str(self.p2))

    # clones the curent Oval object
    def clone(self):
        other = Oval(self.p1, self.p2)
        other.config = self.config.copy()
        return other
    
    # draw the given Oval object
    def _draw(self, canvas, options):
        p1 = self.p1
        p2 = self.p2
        x1,y1 = canvas.toScreen(p1.x,p1.y)
        x2,y2 = canvas.toScreen(p2.x,p2.y)
        return canvas.create_oval(x1,y1,x2,y2,options)

# Circle --------------------------------------------------------------------------------------------------------------
class Circle(Oval):
    
    # constructor
    def __init__(self, center, radius):
        p1 = Point(center.x-radius, center.y-radius)
        p2 = Point(center.x+radius, center.y+radius)
        Oval.__init__(self, p1, p2)
        self.radius = radius

    # unambiguous representation of the object state
    def __repr__(self):
        return "Circle({}, {})".format(str(self.getCenter()), str(self.radius))
    
    # clones the curent Point object
    def clone(self):
        other = Circle(self.getCenter(), self.radius)
        other.config = self.config.copy()
        return other
    
    # returns the radius of the given Circle object
    def getRadius(self):
        return self.radius


# Line ----------------------------------------------------------------------------------------------------------------   
class Line(_BBox):
    
    # constructor
    def __init__(self, p1, p2):
        _BBox.__init__(self, p1, p2, ["arrow","fill","width"])
        self.setFill(DEFAULT_CONFIG['outline'])
        self.setOutline = self.setFill

    # unambiguous representation of the object state
    def __repr__(self):
        return "Line({}, {})".format(str(self.p1), str(self.p2))

    # clones them current Line object
    def clone(self):
        other = Line(self.p1, self.p2)
        other.config = self.config.copy()
        return other
  
    # draw the given Line object
    def _draw(self, canvas, options):
        p1 = self.p1
        p2 = self.p2
        x1,y1 = canvas.toScreen(p1.x,p1.y)
        x2,y2 = canvas.toScreen(p2.x,p2.y)
        return canvas.create_line(x1,y1,x2,y2,options)

    # ?   
    def setArrow(self, option):
        #if not option in ["first","last","both","none"]:
           #raise GraphicsError(BAD_OPTION)
        self._reconfig("arrow", option)
        
# Polygon -------------------------------------------------------------------------------------------------------------
class Polygon(GraphicsObject):
    
    def __init__(self, *points):
        # if points passed as a list, extract it
        if len(points) == 1 and type(points[0]) == type([]):
            points = points[0]
        self.points = list(map(Point.clone, points))
        GraphicsObject.__init__(self, ["outline", "width", "fill"])

    # unambiguous representation of the object state
    def __repr__(self):
        return "Polygon" + str(tuple(p for p in self.points))
    
    # clones them current Line object
    def clone(self):
        other = Polygon(*self.points)
        other.config = self.config.copy()
        return other

    # returns a list of points outlining the Polygon object
    def getPoints(self):
        return list(map(Point.clone, self.points))

    # move the given Polygon by dx, dy
    def _move(self, dx, dy):
        for p in self.points:
            p.move(dx,dy)
   
    # draw the Polygon object
    def _draw(self, canvas, options):
        args = [canvas]
        for p in self.points:
            x,y = canvas.toScreen(p.x,p.y)
            args.append(x)
            args.append(y)
        args.append(options)
        return GraphWin.create_polygon(*args) 

# Text ----------------------------------------------------------------------------------------------------------------
class Text(GraphicsObject):
    
    # constructor
    def __init__(self, p, text):
        GraphicsObject.__init__(self, ["justify", "fill", "text", "font"])
        self.setText(text)
        self.anchor = p.clone()
        self.setFill(DEFAULT_CONFIG['outline'])
        self.setOutline = self.setFill

    def __repr__(self):
        return "Text({}, '{}')".format(self.anchor, self.getText())
    
    # draws the current text box, with the given options - ?
    def _draw(self, canvas, options):
        p = self.anchor
        x,y = canvas.toScreen(p.x,p.y)
        return canvas.create_text(x,y,options)
    
    # moves the given TextBox object  by dx, dy
    def _move(self, dx, dy):
        self.anchor.move(dx,dy)
   
    # clones the current TextBox object
    def clone(self):
        other = Text(self.anchor, self.config['text'])
        other.config = self.config.copy()
        return other
    
    # change the text inside of a TextBox object
    def setText(self,text):
        self._reconfig("text", text)
    
    # returns the text inside of a TextBox object
    def getText(self):
        return self.config["text"]

    # ? 
    def getAnchor(self):
        return self.anchor.clone()

    # set the typeface of the TextBox object
    def setFace(self, face):
        if face in ['helvetica','arial','courier','times roman']:
            f,s,b = self.config['font']
            self._reconfig("font",(face,s,b))
        '''else:
            raise GraphicsError(BAD_OPTION)'''
    
    # set font size of the TextBox object
    def setSize(self, size):
        if 5 <= size <= 36:
            f,s,b = self.config['font']
            self._reconfig("font", (f,size,b))
        '''else:
            raise GraphicsError(BAD_OPTION)'''

    # set font-style of the TextBox object
    def setStyle(self, style):
        if style in ['bold','normal','italic', 'bold italic']:
            f,s,b = self.config['font']
            self._reconfig("font", (f,s,style))
        '''else:
            raise GraphicsError(BAD_OPTION)'''

    # set text color
    def setTextColor(self, color):
        self.setFill(color)

# Entry ---------------------------------------------------------------------------------------------------------------
class Entry(GraphicsObject):

    # constructor
    def __init__(self, p, width):
        GraphicsObject.__init__(self, [])
        self.anchor = p.clone()
        #print self.anchor
        self.width = width
        self.text = tk.StringVar(root)
        self.text.set("")
        self.fill = "gray"
        self.color = "black"
        self.font = DEFAULT_CONFIG['font']
        self.entry = None
    
    # unambiguous representation of object state 
    def __repr__(self):
        return "Entry({}, {})".format(self.anchor, self.width)

    # draw the Entry object, with the given options
    def _draw(self, canvas, options):
        p = self.anchor
        x,y = canvas.toScreen(p.x,p.y)
        frm = tk.Frame(canvas.master)
        self.entry = tk.Entry(frm,
                              width=self.width,
                              textvariable=self.text,
                              bg = self.fill,
                              fg = self.color,
                              font=self.font)
        self.entry.pack()
        #self.setFill(self.fill)
        self.entry.focus_set()
        return canvas.create_window(x,y,window=frm)

    # returns the text of the Entry object
    def getText(self):
        return self.text.get()

    # move the Entry object by dx, dy
    def _move(self, dx, dy):
        self.anchor.move(dx,dy)

    # ?
    def getAnchor(self):
        return self.anchor.clone()

    # clones the current Entry object
    def clone(self):
        other = Entry(self.anchor, self.width)
        other.config = self.config.copy()
        other.text = tk.StringVar()
        other.text.set(self.text.get())
        other.fill = self.fill
        return other

    # set the text of the Entry object
    def setText(self, t):
        self.text.set(t)

    # set the fill of the Entry object using color
    def setFill(self, color):
        self.fill = color
        if self.entry:
            self.entry.config(bg=color)

    # ?
    def _setFontComponent(self, which, value):
        font = list(self.font)
        font[which] = value
        self.font = tuple(font)
        if self.entry:
            self.entry.config(font=self.font)

    # set typeface of the text of the Entry object
    def setFace(self, face):
        if face in ['helvetica','arial','courier','times roman']:
            self._setFontComponent(0, face)
        #else:
            #raise GraphicsError(BAD_OPTION)

    # set font size of the text in the entry object
    def setSize(self, size):
        if 5 <= size <= 36:
            self._setFontComponent(1,size)
        #else:
            #raise GraphicsError(BAD_OPTION)

    # set font style of text in the entry object
    def setStyle(self, style):
        if style in ['bold','normal','italic', 'bold italic']:
            self._setFontComponent(2, style)
        #else:
            #raise GraphicsError(BAD_OPTION)

    # set text color of text in the entry object
    def setTextColor(self, color):
        self.color=color
        if self.entry:
            self.entry.config(fg=color)

# Button --------------------------------------------------------------------------------------------------------------
class BButton(GraphicsObject):

    # constructor
    def __init__(self, p, text, height, width):
        GraphicsObject.__init__(self, [])
        self.text=text
        self.anchor = p.clone()
        self.height=height
        self.width=width
    
    # draw
    def _draw(self, canvas, options):
        p = self.anchor
        x,y = canvas.toScreen(p.x,p.y)
        button = tk.Button(canvas, self.text)
        return button.place(x, y)

    # move the Button by dx, dy     
    def _move(self, dx, dy):
        self.anchor.move(dx,dy)

# Image ---------------------------------------------------------------------------------------------------------------
class Image(GraphicsObject):

    idCount = 0
    imageCache = {} # tk photoimages go here to avoid GC while drawn 
    
    # constructor
    def __init__(self, p, *pixmap):
        GraphicsObject.__init__(self, [])
        self.anchor = p.clone()
        self.imageId = Image.idCount
        Image.idCount = Image.idCount + 1
        if len(pixmap) == 1: # file name provided
            self.img = tk.PhotoImage(file=pixmap[0], master=root)
        else: # width and height provided
            width, height = pixmap
            self.img = tk.PhotoImage(master=root, width=width, height=height)

    # unambiguous representation of object state
    def __repr__(self):
        return "Image({}, {}, {})".format(self.anchor, self.getWidth(), self.getHeight())
    
    # draw
    def _draw(self, canvas, options):
        p = self.anchor
        x,y = canvas.toScreen(p.x,p.y)
        self.imageCache[self.imageId] = self.img # save a reference  
        return canvas.create_image(x,y,image=self.img)
    
    # move Image by dx, dy
    def _move(self, dx, dy):
        self.anchor.move(dx,dy)
    
    # undraw the Image object
    def undraw(self):
        try:
            del self.imageCache[self.imageId]  # allow gc of tk photoimage
        except KeyError:
            pass
        GraphicsObject.undraw(self)
    
    # ?
    def getAnchor(self):
        return self.anchor.clone()
    
    # clones the current Image object
    def clone(self):
        other = Image(Point(0,0), 0, 0)
        other.img = self.img.copy()
        other.anchor = self.anchor.clone()
        other.config = self.config.copy()
        return other

    # returns the width of the image in pixels
    def getWidth(self):
        return self.img.width() 

    # returns the height of the image in pixels
    def getHeight(self):
        return self.img.height()
# returns a list [r,g,b] with the RGB color values for pixel (x,y), r,g,b are in range(256)

        '''
    def getPixel(self, x, y):
        
        
        value = self.img.get(x,y) 
        if type(value) ==  type(0):
            return [value, value, value]
        elif type(value) == type((0,0,0)):
            return list(value)
        else:
            return list(map(int, value.split())) 

    def setPixel(self, x, y, color):
        Sets pixel (x,y) to the given color
        
        """
        self.img.put("{" + color +"}", (x, y))
        

    def save(self, filename):
        Saves the pixmap image to filename.
        The format for the save image is determined from the filname extension.

        """
        
        path, name = os.path.split(filename)
        ext = name.split(".")[-1]
        self.img.write( filename, format=ext)

        
    def color_rgb(r,g,b):
        r,g,b are intensities of red, green, and blue in range(256)
        Returns color specifier string for the resulting color"""
        return "#%02x%02x%02x" % (r,g,b)

    def test():
        win = GraphWin()
        win.setCoords(0,0,10,10)
        t = Text(Point(5,5), "Centered Text")
        t.draw(win)
        p = Polygon(Point(1,1), Point(5,3), Point(2,7))
        p.draw(win)
        e = Entry(Point(5,6), 10)
        e.draw(win)
        win.getMouse()
        p.setFill("red")
        p.setOutline("blue")
        p.setWidth(2)
        s = ""
        for pt in p.getPoints():
            s = s + "(%0.1f,%0.1f) " % (pt.getX(), pt.getY())
        t.setText(e.getText())
        e.setFill("green")
        e.setText("Spam!")
        e.move(2,0)
        win.getMouse()
        p.move(2,3)
        s = ""
        for pt in p.getPoints():
            s = s + "(%0.1f,%0.1f) " % (pt.getX(), pt.getY())
        t.setText(s)
        win.getMouse()
        p.undraw()
        e.undraw()
        t.setStyle("bold")
        win.getMouse()
        t.setStyle("normal")
        win.getMouse()
        t.setStyle("italic")
        win.getMouse()
        t.setStyle("bold italic")
        win.getMouse()
        t.setSize(14)
        win.getMouse()
        t.setFace("arial")
        t.setSize(20)
        win.getMouse()
        win.close()'''

#MacOS fix 2
#tk.Toplevel(_root).destroy()

# MacOS fix 1
#update()

#if __name__ == "__main__":
    #test()