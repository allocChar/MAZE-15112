# Updated Animation Starter Code

from tkinter import *

##Taken from 112 notes
#Basic File IO
def readFile(path):
    with open(path, "rt") as f:
        return f.read()

def writeFile(path, contents):
    with open(path, "wt") as f:
        f.write(contents)
##
import random

class BallPlacer(object):
    def __init__(self,x,y,color,r):
        self.x = x
        self.y = y
        self.color = color
        self.r = r
    def drawSelf(self,canvas,data):
        r = self.r
        canvas.create_oval(self.x-r,self.y-r,self.x+r,self.y+r,fill=self.color)

class EndPlacer(object):
    def __init__(self,x,y,color,r):
        self.x = x
        self.y = y
        self.color = color
        self.r = r
    def drawSelf(self,canvas,data):
        r = self.r
        x = self.x
        y = self.y
        points = [(x,y-r),(x-r,y),(x,y+r),(x+r,y)]
        canvas.create_polygon(points,fill=self.color,width = 1)
        canvas.create_text(x,y,text = "f",font = ("Arial",int(r)))

class EnemyPlacer(object):
    def __init__(self,x,y,color,r):
        self.x = x
        self.y = y
        self.color = color
        self.r = r
    def drawSelf(self,canvas,data):
        r = self.r
        x = self.x
        y = self.y
        r*=3
        points = [(x,y-r),(x-r,y),(x,y+r),(x+r,y)]
        canvas.create_polygon(points,fill=self.color,width = 1)
        canvas.create_text(x,y,text = "E",font = ("Arial",int(r)))

def generateLevel(data):
    data.obsList = []
    data.ballDisplay = []
    data.enemDisplay = []
    sX = 2
    sY = 2
    for i in range(4):
        for j in range(4):
            cX = sX+4*j
            cY = sY+4*i
            choice = random.randint(1,6)
            for pos in range(-2,3):
                data.floorPlan[cX-2][cY+pos]=2
            for pos in range(-2,3):
                data.floorPlan[cX+2][cY+pos]=2
            for pos in range(-1,2):
                data.floorPlan[cX+pos][cY-2]=2
            for pos in range(-1,2):
                data.floorPlan[cX+pos][cY+2]=2
            x = cX*data.width/40
            y = cY*data.width/40
            if i!=0 and j!=0:
                if choice ==5 or choice==6:
                    data.ballDisplay.append(BallPlacer(x,y,"white",data.width/200))
                elif choice==4:
                    data.enemDisplay.append(EnemyPlacer(x,y,"red",data.width/200))
                
    for i in range(4):
        for j in range(4):
            cX = sX+4*j
            cY = sY+4*i
            openCount = 0
            while openCount<2:
                open = random.randint(1,4)
                if open==1 and data.floorPlan[cX-2][cY]!=0:
                    data.floorPlan[cX-2][cY]=0
                    openCount+=1
                elif open==2 and data.floorPlan[cX+2][cY]!=0:
                    data.floorPlan[cX+2][cY]=0
                    openCount+=1
                elif open==3 and data.floorPlan[cX][cY-2]!=0:
                    data.floorPlan[cX][cY-2]=0
                    openCount+=1
                elif open==4 and data.floorPlan[cX][cY+2]!=0:
                    data.floorPlan[cX][cY+2]=0
                    openCount+=1
    for i in range(len(data.floorPlan)):
        for j in range(len(data.floorPlan)):
            if (i==0 or j==0 or i==len(data.floorPlan)-1 \
            or j==len(data.floorPlan)-1):
                data.floorPlan[i][j]=2
    data.endDisplay = []
    data.endDisplay.append(EndPlacer(2*data.width/40,2*data.width/40,\
    "lawn green",data.width/100))

####################################
# customize these functions
####################################

def init(data):
    # load data.xyz as appropriate
    data.floorPlan = [[0 for i in range(20)] for i in range(20)]
    for i in range(len(data.floorPlan)):
        for j in range(len(data.floorPlan)):
            if i==0 or i==len(data.floorPlan)-1:
                data.floorPlan[i][j]=1
            if j==0 or j==len(data.floorPlan)-1:
                data.floorPlan[i][j]=1
    data.colors = \
    ["white","black","blue","navy","red","cadet blue","lawn green","yellow"]
    data.colorSelect = 0
    data.size = (data.width/2)/len(data.floorPlan)
    data.objectList = ["wall","ball","finish","enemy"]
    data.obSelect = 0
    data.ballDisplay = []
    data.endDisplay = []
    data.enemDisplay = []
    data.obsList= []
    data.instructionsFlag = False

def mousePressed(event, data):
    x = int(event.x//data.size)
    y = int(event.y//data.size)
    if 0<event.x<data.width/2 and event.y>0 and data.obSelect == 0:
        data.floorPlan[y][x]=data.colorSelect
    elif 0<event.x<data.width/2 and event.y>0 and data.obSelect == 1:
        data.ballDisplay.append(BallPlacer(event.x,event.y,\
        data.colors[data.colorSelect],data.width/200))
    elif 0<event.x<data.width/2 and event.y>0 and data.obSelect == 2:
        if data.colorSelect!=0:
            data.endDisplay = []
            data.endDisplay.append(EndPlacer(event.x,event.y,\
            data.colors[data.colorSelect],data.width/100))
    elif 0<event.x<data.width/2 and event.y>0 and data.obSelect == 3:
        if data.colorSelect!=0:
            data.enemDisplay.append(EnemyPlacer(event.x,event.y,\
            data.colors[data.colorSelect],data.width/200))
    elif event.y<data.height/2 and (data.width*3/4)>event.x>data.width/2:
        size = (data.height/2)/len(data.colors)
        choice = int(event.y//size)
        data.colorSelect = choice
    elif event.y>data.height/2 and (data.width*3/4)>event.x>data.width/2:
        size = (data.height/2)/len(data.objectList)
        
        choice = int((event.y-data.height/2)//size)
        if choice==data.obSelect:
            if choice == 0:
                init(data)
            elif choice == 1:
                data.ballDisplay = []
            elif choice == 2:
                data.endDisplay = []
            elif choice == 3:
                data.enemDisplay = []
        else:
            data.obSelect = choice
    elif event.y>data.height*3/4 and event.x>data.width*3/4:
        if len(data.endDisplay)>0 and len(data.ballDisplay)>0:
            writeObsList(data)
            submitLevel(data)
    # use event.x and event.y

def writeObsList(data):
    data.obsList = []
    for ball in data.ballDisplay:
        ballInfo = ("ball",ball.y/data.size,ball.x/data.size,ball.color)
        data.obsList.append(ballInfo)
    for enemy in data.enemDisplay:
        enemInfo = ("enemy",enemy.y/data.size,enemy.x/data.size,enemy.color)
        data.obsList.append(enemInfo)
    finish = data.endDisplay[0]
    finishInfo = ("finish",finish.y/data.size,finish.x/data.size,finish.color)
    data.obsList.append(finishInfo)
        

def submitLevel(data):
    info = "map: "
    info+="\n"
    info += str(data.floorPlan)
    info+="\n"
    info+="Objects: "
    info+="\n"
    info+=str(data.obsList)
    writeFile("Level_Info.txt",info)
    
def keyPressed(event, data):
    if event.keysym=="i":
        data.instructionsFlag = not data.instructionsFlag
    if event.keysym=="g":
        generateLevel(data)
    # use event.char and event.keysym
    pass

def timerFired(data):
    pass

def redrawAll(canvas, data):
    drawLevel(canvas,data)
    drawColors(canvas,data)
    drawBalls(canvas,data)
    drawObSelection(canvas,data)
    if len(data.endDisplay)==1:
        data.endDisplay[0].drawSelf(canvas,data)
    drawEnems(canvas,data)
    drawSubmit(canvas,data)
    drawInstructions(canvas,data)

def drawInstructions(canvas,data):
    x = data.width - (data.width/4)
    y = 0
    fS = int(data.width/50)
    if not data.instructionsFlag:
        info = "Instructions: I"
        canvas.create_text(x,y,font = ("Courier",fS),\
        text = info,anchor="nw",width = data.width/4)
    else:
        fS = fS = int(data.width/75)
        info = """Select object you wish to add to level by clicking on words (bottom left)::\n
Clear all objects of that type by reselecting whats already selected::\n
Select Color on the top left::\n
Trying to clear walls clears all objects, instead select color white to clear specific walls::\n
To finish level, level must include the finish and atleast one ball::\n
Certain colors are not allowed for the finish and enemies::\n
Submit level at bottom right::\n
Edit level on left::\n
Random Level: press G\n
        """
        canvas.create_text(x,y,font = ("Courier",fS),\
        text = info,anchor="nw",width = data.width/4)
        
        
def drawSubmit(canvas,data):
    x0 = data.width*3/4
    y0 = data.height
    x1 = data.width
    y1 = data.height*3/4
    x2 = data.width
    y2 = data.height
    points = [(x0,y0),(x1,y1),(x2,y2)]
    color = "lawn green"
    textSubmit = "Submit Level"
    textWidth = data.width/4
    if len(data.endDisplay)==0 or len(data.ballDisplay)==0:
        color = "red"
        textSubmit = "(Incomplete)"
    canvas.create_polygon(points,fill=color,width = 0)
    textX = data.width*3/4
    textY = data.height*5/6
    canvas.create_text(textX+data.width/8,textY+data.height/8,\
    text=textSubmit,font=("Courier",int(data.width/50)),width=textWidth)

def drawEnems(canvas,data):
    for enemy in data.enemDisplay:
        enemy.drawSelf(canvas,data)
        
def drawObSelection(canvas,data):
    size = (data.height/2)/len(data.objectList)
    for i in range(len(data.objectList)):
        x0 = data.width/2
        y0 = data.height/2+size*i
        x1 = x0+size*2
        y1 = y0+size
        if i==data.obSelect:
            color = "yellow"
        else:
            color = "white"
        canvas.create_rectangle(x0,y0,x1,y1,fill=color,width=0)
        canvas.create_text(x0+size/3,y0, anchor = "nw",\
        text=data.objectList[i],font=("Courier",int(data.width/50)))
        
def drawBalls(canvas,data):
    for ball in data.ballDisplay:
        ball.drawSelf(canvas,data)
def drawLevel(canvas,data):
    size = (data.width/2)/len(data.floorPlan)
    for i in range(len(data.floorPlan)):
        for j in range(len(data.floorPlan)):
            x0 = 0+size*j
            x1 = x0+size
            y0 = 0+size*i
            y1 = y0+size
            canvas.create_rectangle(x0,y0,x1,y1,\
            fill = data.colors[data.floorPlan[i][j]],width = 0)

def drawColors(canvas,data):
    size = (data.height/2)/len(data.colors)
    for j in range(len(data.colors)):
        x0 = data.width/2
        x1 = x0+(x0/2)
        y0 = 0 + size*j
        y1 = y0+size
        canvas.create_rectangle(x0,y0,x1,y1,fill=data.colors[j],width=0)
        if j == data.colorSelect:
            color = "white"
            if j==0:
                color = "black"
            canvas.create_line(x0+size/4,y0+size/2,x1,y0+size/2,\
            width = data.width/100,fill=color)
    x0 = data.width*3/4
    y0 = 0
    x1 = (data.width*5/8)
    y1= data.height/2
    x2 = x0
    y2 = y1
    canvas.create_polygon([x0,y0,x1,y1,x2,y2],fill="white")
    # draw in canvas

####################################
#MVC starter code from 112 Notes:
####################################

def run(width=1200, height=600):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
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
    data.timerDelay = 100 # milliseconds
    Lroot = Tk()
    Lroot.title("Level Editor")
    Lroot.resizable(width=False, height=False) # prevents resizing window
    init(data)
    # create the Lroot and the canvas
    canvas = Canvas(Lroot, width=data.width, height=data.height)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    # set up events
    Lroot.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    Lroot.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    Lroot.mainloop()