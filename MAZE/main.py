import Engine
import Level_Editor

# Updated Animation Starter Code

class Button(object):
    def __init__(self,x,y,r,color,text):
        self.x = x
        self.y = y
        self.r = r
        self.color = color
        self.text = text
    def drawSelf(self,canvas):
        canvas.create_oval(self.x-self.r,self.y-self.r,\
        self.x+self.r,self.y+self.r,fill = self.color,width=0)
        canvas.create_text(self.x,self.y,text = self.text, font = ("Courier",self.r//2))
    def checkClick(self,x,y):
        if ((self.x-x)**2+(self.y-y)**2)**.5<self.r:
            return True
        return False

size = 700
point = int(size/2)
buttonSize = int(size/10)
playButton = Button(point,point,buttonSize,"white","Play")
levelEditorButton = Button(point,point+buttonSize*2,buttonSize,"white","Editor")
    
from tkinter import *
####################################
# customize these functions
####################################

def init(data):
    data.playButton = playButton
    data.levelEditorButton = levelEditorButton
    # load data.xyz as appropriate
    pass

def mousePressed(event, data):
    if data.playButton.checkClick(event.x,event.y):
        Engine.run()
    elif data.levelEditorButton.checkClick(event.x,event.y):
        Level_Editor.run()
    # use event.x and event.y
    pass

def keyPressed(event, data):
    if event.keysym=="l":
        Level_Editor.run()
    elif event.keysym=="p":
        Engine.run()
    # use event.char and event.keysym
    pass
def timerFired(data):
    pass

def redrawAll(canvas, data):
    drawLogo(canvas,data)
    data.playButton.drawSelf(canvas)
    data.levelEditorButton.drawSelf(canvas)
    # draw in canvas
    pass

def drawLogo(canvas,data):
    titleText = "ṀǞȤḜ"
    for i in range(15):
        for j in range(20):
            x = 0+(data.width/15)*i
            y = 0+(data.height/20)*j
            canvas.create_text(x,y,text = titleText,\
            fill="white",anchor = "nw",font = ("Arial",int(data.width/50)))
    canvas.create_text(int(data.width/2),int(data.height/4),\
    text = titleText, font= ("Courier",int(data.width/10)),fill="red")

####################################
# use the run function as-is
####################################

def run(width=700, height=700):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='black', width=0)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 10000000000 # milliseconds
    root = Tk()
    root.title("Main Menu")
    root.resizable(width=False, height=False) # prevents resizing window
    init(data)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    def quit():
        root.destroy()
    # and launch the app
    root.mainloop()  # blocks until window is closed
run()