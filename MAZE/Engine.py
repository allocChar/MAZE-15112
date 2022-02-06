#Main 3D Engine
#Jorge Tamayo
#112-term project
#Andrew ID: jtamayo
from __future__ import print_function

from tkinter import *
import math

import tkinter as tk

from debouncer import Debouncer

import ast

from floor_analysis import *

import copy
##read file taken from notes
def readFile(path):
    with open(path, "rt") as f:
        return f.read()

##gets map from txt file
def getFloorPlan(info):
    levelString = ""
    toggleRead = False
    count = 0
    for elem in info:
        if elem=="\n" and count<2:
            toggleRead = not toggleRead
            count+=1
        if toggleRead:
            levelString +=elem
    return ast.literal_eval(levelString)

##gets objecrs from txt file
def getObsList(info):
    count = 0
    obsList = ""
    toggleRead = False
    for elem in info:
        if elem=="\n":
            count+=1
        if count==3:
            toggleRead = True
        if toggleRead:
            obsList+=elem
    return ast.literal_eval(obsList)

##

def wallBetween(x0,y0,x1,y1,floor):
    accuracy = 150
    stepX = (x1-x0)/accuracy
    stepY = (y1-y0)/accuracy
    while abs(x1-x0)>1 or abs(y1-y0)>.2:
        x0+=stepX
        y0+=stepY
        if floor[int(x0)][int(y0)]!=0:
            return True
    return False
#####
#    ________    ___   __________ ___________
#   / ____/ /   /   | / ___/ ___// ____/ ___/
#  / /   / /   / /| | \__ \\__ \/ __/  \__ \ 
# / /___/ /___/ ___ |___/ /__/ / /___ ___/ / 
# \____/_____/_/  |_/____/____/_____//____/  
#
#####

#         ___  __                 
#  ____  / _ \/ /__ ___ _____ ____
# /___/ / ___/ / _ `/ // / -_) __/
#      /_/  /_/\_,_/\_, /\__/_/   
#                  /___/          

##Main Player Class
class Player(object):
    def __init__(self,pX,pY,angle):
        self.pX = pX
        self.pY = pY
        self.angle = angle
        self.health = 100
        self.holding = False
    def move(self,pressedKey,data):
        (oldX,oldY)=(data.player.pX,data.player.pY)
        MDS = .15 #moveDistanceScaler
        strafeAngle = 90
        if pressedKey=="Left":
            self.angle+=data.lookSensitivity
            self.angle%=360
        elif pressedKey=="Right":
            self.angle-=data.lookSensitivity
            self.angle%=360
        elif pressedKey=="Up":
            self.pX+=math.cos(math.radians(self.angle))*MDS
            self.pY+=math.sin(math.radians(self.angle))*MDS
        elif pressedKey=="Down":
            self.pX-=math.cos(math.radians(self.angle))*MDS
            self.pY-=math.sin(math.radians(self.angle))*MDS
        
        #STRAFING WIP============================================================+++
        verifyMove(data,oldX,oldY)
        

#Verify Move
def verifyMove(data,oldX,oldY):
    (newX,newY) = (int(data.player.pX),int(data.player.pY))
    if data.floorPlan[newX][newY]!=0:
        (data.player.pX,data.player.pY) = (oldX,oldY)

#         ____         _ __     
#  ____  / __/__  ____(_) /____ 
# /___/ _\ \/ _ \/ __/ / __/ -_)
#      /___/ .__/_/ /_/\__/\__/ 
#         /_/                   

##Main Sprite Class
class Sprite(object):
    def __init__(self,pX,pY):
        self.pX = pX
        self.pY = pY
        self.relativeAngle = None #angle is relative to player
        self.screenPos = None
        self.distanceFromPlayer = None
        self.wallInWay = True
        self.shadowSize = .2
    #
    # UPDATE INFORMATION FUNCTIONS==============================================000
    #
    
    #sight range is (1/2) player view Range
    #changes distanceFromPlayer Variabale
    def updateDistanceFromPlayer(self,playerX,playerY):
        (x1,y1,x2,y2) = (playerX,playerY,self.pX,self.pY)
        self.distanceFromPlayer = (((x2-x1)**2)+((y2-y1)**2))**.5
        #in case object right on player position
        if self.distanceFromPlayer==0:
            self.distanceFromPlayer+=.0000001#avoid division by zero
    #Gets value for relative view angle variable
    def updateViewAngle(self,playerX,playerY):
        (x1,y1,x2,y2) = (playerX,playerY,self.pX,self.pY)
        distance = (((x2-x1)**2)+((y2-y1)**2))**.5
        if distance>0:
            viewAngle1 = math.acos((x1-x2)/distance)
            viewAngle2 = math.asin((y1-y2)/distance)
            viewAngle1 = math.degrees(viewAngle1)
            viewAngle2 = math.degrees(viewAngle2)
        else:
            (viewAngle1,viewAngle2)=(0,0)
        dividor = abs(viewAngle2)
        if dividor == 0: dividor = 1#avoid division by zero
        mainViewAngle = (viewAngle1*viewAngle2)/dividor
        mainViewAngle+=180 #conversion for relative player angle(180 degrees)
        mainViewAngle%=360 #modded for consistency (360 degrees)
        if y2==y1 and x2>x1:
            self.relativeAngle = 0
        else:
            self.relativeAngle = mainViewAngle
    #sight range is (1/2) player view Range
    #changes screenPos, 0-data.viewRange values when seen
    def updateScreenPos(self,viewAngle,sightRange):
        self.screenPos = self.relativeAngle - (viewAngle-sightRange)
        #below are base cases for angles close to 0
        if 360-sightRange<viewAngle<360:
            self.screenPos = self.relativeAngle - (viewAngle-360-sightRange)
            if self.screenPos>360:
                self.screenPos = self.relativeAngle - (viewAngle-sightRange)
        if 0<=viewAngle<sightRange:
            self.screenPos = self.relativeAngle - (viewAngle+360-sightRange)
            if self.screenPos<-sightRange:
                self.screenPos = self.relativeAngle - (viewAngle-sightRange)
    #changes variable WallInWay so Sprite is not drawn when behind wall
    def updateWallInWay(self,data,playerX,playerY,playerAngle):
        accuracy = 10
        posX = playerX
        posY = playerY
        while True:
            posX+=math.cos(math.radians(self.relativeAngle))/accuracy
            posY+=math.sin(math.radians(self.relativeAngle))/accuracy
            distance = ((self.pX-posX)**2+(self.pY-posY)**2)**.5
            if distance<=.5:
                self.wallInWay=False
                return False
            if data.floorPlan[int(posX)][int(posY)]!=0:
                self.wallInWay = True
                return True
            if distance>self.distanceFromPlayer:
                self.wallInWay = False
                return False
    #=========================DRAW FUNCIONS===========================000
    #Preliminary test Sprite 
    def drawSelf(self,data,canvas):
        if not self.wallInWay:
            sizeScaler = .2
            screenSize = data.width-(2*data.marginSize)
            interval = screenSize/data.viewRange
            rightBound = data.width-data.marginSize
            size = data.height/self.distanceFromPlayer
            size*=sizeScaler
            xPos = rightBound - (interval*self.screenPos)
            heightOffGround = (data.height/4)/self.distanceFromPlayer
            yPos = (data.height/2)+heightOffGround
            canvas.create_rectangle(xPos-size/2,\
            yPos-size/2,xPos+size/2,yPos+size/2,fill="white",width=1)
    #main shadow drawing function
    def drawShadow(self,data,canvas):
        if not self.wallInWay:
            screenSize = data.width-(2*data.marginSize)
            interval = screenSize/data.viewRange
            rightBound = data.width-data.marginSize
            sizeScaler = self.shadowSize
            size = data.height/self.distanceFromPlayer
            size*=sizeScaler
            xPos = rightBound - (interval*self.screenPos)
            yPos = (data.height/2)+(data.height/2)/self.distanceFromPlayer
            (proportionX,proportionY) = (2,6)
            canvas.create_oval(xPos-(size/proportionX),yPos-(size/proportionY),\
            xPos+(size/proportionX),yPos+(size/proportionY),fill="black")
    def updateAllVisualParameters(self,data):
        self.updateViewAngle(data.player.pX,data.player.pY)
        self.updateDistanceFromPlayer(data.player.pX,data.player.pY)
        self.updateScreenPos(data.player.angle,data.viewRange/2)
        self.updateWallInWay(data,\
        data.player.pX,data.player.pY,data.player.angle)
         

##
#Ball
##

class Ball(Sprite):
    def __init__(self,pX,pY,color):
        super().__init__(pX,pY)
        self.grabbed= False
        self.isThrown = False
        self.color = color
        self.angle = None
        self.speedX = 0
        self.speedY = 0
    def drawSelf(self,data,canvas):
        if not self.wallInWay and not self.grabbed:
            sizeScaler = .2
            screenSize = data.width-(2*data.marginSize)
            interval = screenSize/data.viewRange
            rightBound = data.width-data.marginSize
            size = data.height/self.distanceFromPlayer
            size*=sizeScaler
            xPos = rightBound - (interval*self.screenPos)
            heightOffGround = (data.height/4)/self.distanceFromPlayer
            yPos = (data.height/2)+heightOffGround
            canvas.create_oval(xPos-size/2,\
            yPos-size/2,xPos+size/2,yPos+size/2,fill=self.color,width=0)
        elif self.grabbed:
            centerX = data.width-data.marginSize
            centerY = data.height
            radius = data.width/10
            (x0,y0,x1,y1) = (centerX-radius,centerY-radius,\
            centerX+radius,centerY+radius)
            canvas.create_oval(x0,y0,x1,y1,fill=self.color,width=0)
    def drawShadow(self,data,canvas):
        if not self.wallInWay and not self.grabbed:
            screenSize = data.width-(2*data.marginSize)
            interval = screenSize/data.viewRange
            rightBound = data.width-data.marginSize
            sizeScaler = self.shadowSize
            size = data.height/self.distanceFromPlayer
            size*=sizeScaler
            xPos = rightBound - (interval*self.screenPos)
            yPos = (data.height/2)+(data.height/2)/self.distanceFromPlayer
            (proportionX,proportionY) = (2,6)
            canvas.create_oval(xPos-(size/proportionX),yPos-(size/proportionY),\
            xPos+(size/proportionX),yPos+(size/proportionY),fill="black")
    def throw(self,data):
        stopSpeed = .01
        slowDown = .01
        self.pX+=self.speedX
        x,y = int(self.pX),int(self.pY)
        if data.floorPlan[x][y]!=0:
            self.speedX,self.speedY = 0,0
                
        self.pY+=self.speedY
        self.speedX-=math.cos(math.radians(self.angle))*slowDown
        self.speedY-=math.sin(math.radians(self.angle))*slowDown
        if abs(self.speedX)<stopSpeed and abs(self.speedY)<stopSpeed:
            self.isThrown = False
            
##
#Finish
##
class Finish(Sprite):
    def __init__(self,pX,pY,color):
        super().__init__(pX,pY)
        self.color = color
    def checkFinish(self,data):
        count = 0
        for sprite in data.allSprites:
            if isinstance(sprite,Ball):
                x0 = self.pX
                y0 = self.pY
                x1 = sprite.pX
                y1 = sprite.pY
                distance = ((x1-x0)**2+(y1-y0)**2)**.5
                if ((x1-x0)**2+(y1-y0)**2)**.5>2:
                    count = 1
        if count==0:
            data.levelFinish = True
        else:
            data.levelFinish = False
    def drawSelf(self,data,canvas):
        if not self.wallInWay:
            sizeScaler = .3
            screenSize = data.width-(2*data.marginSize)
            interval = screenSize/data.viewRange
            rightBound = data.width-data.marginSize
            size = data.height/self.distanceFromPlayer
            size*=sizeScaler
            xPos = rightBound - (interval*self.screenPos)
            heightOffGround = (data.height/10)/self.distanceFromPlayer
            yPos = (data.height/2)+heightOffGround
            #canvas.create_oval(xPos-size/2,\
            #yPos-size,xPos+size/2,yPos+size,fill=self.color,width=1)
            front = "♕"
            canvas.create_text(xPos,yPos,text = front,\
            font=("Courier",int(size)),fill=self.color)
            front = "finish"
            canvas.create_text(xPos,yPos+size/2,text = front,\
            font=("Courier",int(size/4)),fill=self.color)
##
#Enemy
##
class Enemy(Sprite):
    def __init__(self,pX,pY,color):
        super().__init__(pX,pY)
        self.color = color
        self.movePoints = [(pX,pY)]
        self.movIndex = 1
        self.count = 0
    def enemMove(self,data):
        moveScaler = .05
        dX = 0
        dY = 0
        if not self.wallInWay:
            self.count = 0
            self.movePoints = [(self.pX,self.pY)]
            self.movIndex = 0
            dX = math.cos(math.radians(self.relativeAngle))*moveScaler
            dY = math.sin(math.radians(self.relativeAngle))*moveScaler
            self.pX-=dX
            self.pY-=dY
        else:
            #find path if you dont have one
            if self.count == 0:
                moves = self.pathFind(data)
                if moves!=None:
                    moves.append((data.player.pX,data.player.pY))
                self.movePoints = moves
            self.count+=1
            movCoords = self.movePoints[self.movIndex]
            movX = movCoords[0]
            movY = movCoords[1]
            if ((self.pX-movX)**2+(self.pY-movY)**2)**.5<.2 and \
            self.movIndex<len(self.movePoints)-1:
                self.movIndex+=1
            if self.movIndex==len(self.movePoints)-1 and self.wallInWay:
                self.count = 0
            slowDown = 30
            dX = (movX-self.pX)/slowDown
            dY = (movY-self.pY)/slowDown
            self.pX+=dX
            self.pY+=dY
        if data.floorPlan[int(self.pX)][int(self.pY)]!=0:
            pass
            
    
    def pathFind(self,data,depth=0,movPoints=[],sol=None,Nodes=[]):
        if depth==0:
            movPoints = self.movePoints
            Nodes = data.AINodes
        x = movPoints[-1][0]
        y = movPoints[-1][1]
        
        if not wallBetween(x,y,data.player.pX,data.player.pY,data.floorPlan):
            return movPoints
        for node in Nodes:
            if not wallBetween(x,y,node[0],node[1],data.floorPlan):
                movPoints.append(node)
                N = copy.deepcopy(Nodes)
                N.remove(node)
                tempSol = self.pathFind(data,depth+1,movPoints,sol,N)
                if tempSol!=None:
                    return tempSol
                movPoints.pop()
        return None

    def damage(self,data):
        x0 = self.pX
        y0 = self.pY
        x1 = data.player.pX
        y1 = data.player.pY
        if ((x1-x0)**2+(y1-y0)**2)**.5<1:
            data.player.health-=1
        if data.player.health<=0:
            data.death = True
    def drawSelf(self,data,canvas):
        if not self.wallInWay:
            sizeScaler = .3
            screenSize = data.width-(2*data.marginSize)
            interval = screenSize/data.viewRange
            rightBound = data.width-data.marginSize
            size = data.height/self.distanceFromPlayer
            size*=sizeScaler
            xPos = rightBound - (interval*self.screenPos)
            heightOffGround = (data.height/10)/self.distanceFromPlayer
            yPos = (data.height/2)+heightOffGround
            points = [(xPos-size/2,yPos),(xPos,yPos-size/2),(xPos+size/2,yPos),(xPos,yPos+size/2)]
            canvas.create_polygon(points,fill=self.color)
            face = "☜ ⍚ ╻ ⍚ ☞"
            arms = "☜       ☞"
            canvas.create_text(xPos,yPos,text = face,\
            font=("Courier",int(size/4)))
            canvas.create_text(xPos,yPos,text = arms,\
            font=("Courier",int(size/4)),fill="white")
        
####################################
##BEGINNING OF MAIN CODE
####################################

#########
#     _____   ____________
#    /  _/ | / /  _/_  __/
#    / //  |/ // /  / /   
#  _/ // /|  // /  / /    
# /___/_/ |_/___/ /_/     
#
#########

def init(data):
    data.levelInfo = readFile("Level_Info.txt")
    #basic UI variables-------
    data.barColor = "black"
    data.floorColor = "grey50"
    data.roofColor = "grey25"
    data.marginSize = (data.width-data.height)/2
    data.floorPlan = getFloorPlan(data.levelInfo)
    #fixes wall gaps
    for i in range(len(data.floorPlan)):
        for j in range(len(data.floorPlan)):
            if (i==0 or j==0 or i==len(data.floorPlan)-1 or j==len(data.floorPlan)-1):
                data.floorPlan[i][j]=1
    #nodes for enemy AI
    data.AINodes = makeNodes(data.floorPlan)
    data.obsInfo = getObsList(data.levelInfo)
    data.wallColorList = \
    [None,"black","blue","navy","red","cadet blue","lawn green","yellow"]
    #player position and angle
    data.player = Player(18,18,180)
    data.lookSensitivity = 3.5
    #raycasting info
    data.viewRange = 40
    data.sweepAmount = 40
    data.sweepAccuracy = 10
    data.seesList = []
    data.allSprites = []
    #Adds objects from level information
    for elem in data.obsInfo:
        if elem[0]=="ball":
            data.allSprites.append(Ball(elem[1],elem[2],elem[3]))
        elif elem[0]=="finish":
            data.finishSprite = Finish(elem[1],elem[2],elem[3])
            data.allSprites.append(data.finishSprite)
        elif elem[0]=="enemy":
            data.allSprites.append(Enemy(elem[1],elem[2],elem[3]))
    data.move = None
    data.left = False
    data.right = False
    data.levelFinish = False
    data.death = False
    data.instructionsFlag = False
    
########
#    __  _______ __________     _____   ______  __  ________
#   / / / / ___// ____/ __ \   /  _/ | / / __ \/ / / /_  __/
#  / / / /\__ \/ __/ / /_/ /   / //  |/ / /_/ / / / / / /   
# / /_/ /___/ / /___/ _, _/  _/ // /|  / ____/ /_/ / / /    
# \____//____/_____/_/ |_|  /___/_/ |_/_/    \____/ /_/     
#                                                          
########
def mousePressed(event, data):
    if event.x>data.marginSize and event.x<data.width-data.marginSize:
        shootAngle = event.x-data.marginSize
        shootAngle/=(data.viewRange/2)
        shootAngle-=data.viewRange/2
        shootAngle*=-1
        shootAngle+=data.player.angle
        for sprite in data.allSprites:
            if isinstance(sprite,Ball) and sprite.grabbed:
                throwScaler = .3
                sprite.grabbed = False
                sprite.isThrown = True
                data.player.holding = False
                sprite.speedX = math.cos(math.radians(shootAngle))*throwScaler
                sprite.speedY = math.sin(math.radians(shootAngle))*throwScaler
                sprite.angle = shootAngle

def keyPressed(event, data):
    if event.keysym in ["Up","Down"]:
        data.move = event.keysym
    elif event.keysym =="Return":
        for sprite in data.allSprites:
            if isinstance(sprite,Ball) and sprite.distanceFromPlayer<2:
                if not data.player.holding:
                    sprite.grabbed = not sprite.grabbed
                    data.player.holding = not data.player.holding
                    data.finishSprite.checkFinish(data)
                elif sprite.grabbed:
                    sprite.grabbed = not sprite.grabbed
                    data.player.holding = not data.player.holding
                    data.finishSprite.checkFinish(data)
                    sprite.pX = data.player.pX+math.cos(math.radians(data.player.angle))
                    sprite.pY = data.player.pY+math.sin(math.radians(data.player.angle))
    elif event.keysym=="r":
        init(data)
    elif event.keysym=="i":
        data.instructionsFlag = not data.instructionsFlag
    


def keyReleased(event,data):
    data.move = None

#
#LEFT ARROW KEY
#
def leftPress(event,data):
    data.left=True
def leftRelease(event,data):
    data.left = False
#
#Right ARROW KEY
#
def rightPress(event,data):
    data.right=True
def rightRelease(event,data):
    data.right = False
######
#   _______                        _______               __
#  /_  __(_)___ ___  ___  _____   / ____(_)_______  ____/ /
#   / / / / __ `__ \/ _ \/ ___/  / /_  / / ___/ _ \/ __  / 
#  / / / / / / / / /  __/ /     / __/ / / /  /  __/ /_/ /  
# /_/ /_/_/ /_/ /_/\___/_/     /_/   /_/_/   \___/\__,_/   
#                                                          
######

def timerFired(data):
    if not data.death and not data.levelFinish:
        if data.left:
            data.player.move("Left",data)
        elif data.right:
            data.player.move("Right",data)
        data.player.move(data.move,data)
        Sweep(data)
        updateSpriteVisuals(data)
        checkBallAndEnem(data)

#calls updateAllVisualParameters and sorts Sprites based on distance
#to avoid farther away Sprites being drawn over closer Sprites
def updateSpriteVisuals(data):
    for sprite in data.allSprites:
        sprite.updateAllVisualParameters(data)
    data.allSprites.sort(key=lambda sprite: sprite.distanceFromPlayer,\
        reverse = True)

def checkBallAndEnem(data):
    for sprite in data.allSprites:
        if isinstance(sprite,Ball) and sprite.grabbed:
            sprite.pX = data.player.pX#+math.cos(math.radians(data.player.angle))
            sprite.pY = data.player.pY#+math.sin(math.radians(data.player.angle))
        elif isinstance(sprite,Ball) and sprite.isThrown:
            sprite.throw(data)
            data.finishSprite.checkFinish(data)
        elif isinstance(sprite,Enemy):
            # moves = sprite.pathFind(data)
            # moves.append((data.player.pX,data.player.pY))
            # sprite.movePoints = moves
            
            #sprite.movePoints = sprite.pathFind(data)
            sprite.enemMove(data)
            sprite.damage(data)
######
#    _____                       
#   / ___/      _____  ___  ____ 
#   \__ \ | /| / / _ \/ _ \/ __ \
#  ___/ / |/ |/ /  __/  __/ /_/ /
# /____/|__/|__/\___/\___/ .___/ 
#                       /_/      
#######

#function that gets wall height information
def Sweep(data):
    x = data.player.pX
    y = data.player.pY
    data.seesList = []
    for look in range(data.sweepAmount):
        interval = (data.viewRange/data.sweepAmount)*look
        angle = data.player.angle+(data.viewRange/2)-interval
        info = getDistanceAndColor(data,x,y,angle)
        data.seesList.append(info)

#gets distance for a specific position and angle
def getDistanceAndColor(data,posX,posY,angle):
    addX = math.cos(math.radians(angle))/data.sweepAccuracy
    addY = math.sin(math.radians(angle))/data.sweepAccuracy
    while True:
        posX += addX
        posY += addY
        iX = int(posX)
        iY = int(posY)
        if data.floorPlan[iX][iY]!=0:
            break
    distance = ((posX-data.player.pX)**2+(posY-data.player.pY)**2)**.5
    return (distance,data.floorPlan[iX][iY])
        
        

####################################
#
#     ____           __                       ___    ____
#    / __ \___  ____/ /________ __      __   /   |  / / /
#   / /_/ / _ \/ __  / ___/ __ `/ | /| / /  / /| | / / / 
#  / _, _/  __/ /_/ / /  / /_/ /| |/ |/ /  / ___ |/ / /  
# /_/ |_|\___/\__,_/_/   \__,_/ |__/|__/  /_/  |_/_/_/   
#                                                        
####################################

#MAIN FUNCTION
def redrawAll(canvas, data):
    drawUIBase(canvas,data)
    drawView(canvas,data)
    for sprite in data.allSprites:
        sprite.drawShadow(data,canvas)
        sprite.drawSelf(data,canvas)
    drawBlackBars(canvas,data)
    if data.levelFinish:
        titleText = "ṀǞȤḜ"
        canvas.create_text(data.width/2,data.height/2,\
        text = titleText, font=("Courier",int(data.width/10)),fill="red")
    if data.death:
        words = "ḊḜÅṮḦ"
        canvas.create_text(data.width/2,data.height/2,\
        text = words, font=("Courier",int(data.width/10)),fill="red")
    drawHealthBar(canvas,data)
    drawMiniMap(canvas,data)
    drawInstructions(canvas,data)
    
#HELPERS===========================

def drawInstructions(canvas,data):
    x = data.width-data.marginSize
    fS = int(data.width/100)
    if data.instructionsFlag:
        info = """ Pick up/drop ball: Enter
        \n Throw ball:click on screen(picks direction)
        \n Move: Arrow keys
        \n Reset: R
        \n UI:
        \n Top Right: Mini Map
        \n Red Bar Left: Health
        \n Objective:
        \n get all balls to goal"""
        canvas.create_text(x,data.height/2,anchor = "nw",\
        font = ("Courier",fS),text = info,fill="white",width=data.marginSize)
    else:
        canvas.create_text(x,data.height/2,anchor = "nw",\
        font = ("Courier",fS),text = "Instructions: I",fill="white",\
        width=data.marginSize)
    
def drawView(canvas,data):
    for i in range(len(data.seesList)):
        pilarHeight = (data.height/data.seesList[i][0])
        interval = (data.width - (data.marginSize*2))/data.sweepAmount
        x0 = data.marginSize + interval*i
        x1 = x0+interval
        y0 = (data.height/2)-(pilarHeight/2)
        y1 = (data.height/2)+(pilarHeight/2)
        color = data.wallColorList[data.seesList[i][1]]
        canvas.create_rectangle(x0,y0,x1,y1,\
            fill = color,width = 0)
            
#Draws UI Base and background
def drawUIBase(canvas,data):
    canvas.create_rectangle(0,0,data.width,data.height/2,\
        fill=data.roofColor,width = 0)
    #---
    canvas.create_rectangle(0,data.height/2,data.width,data.height,\
        fill = data.floorColor,width = 0)
    #---

def drawBlackBars(canvas,data):
    canvas.create_rectangle(0,0,data.marginSize,data.height,\
        fill = data.barColor, width = 0)
    #---
    canvas.create_rectangle(data.width-data.marginSize,\
        0,data.width,data.height,fill=data.barColor,width = 0)

def drawHealthBar(canvas,data):
    size = data.height*(data.player.health*(10**-2))
    x = data.marginSize/2
    mid = data.height/2
    adjust = size/2
    thickness = data.marginSize/25
    canvas.create_line(x,mid-adjust,x,mid+adjust,fill="red",width=thickness)

def drawMiniMap(canvas,data):
    tileSize = data.marginSize/len(data.floorPlan)
    xI = data.width-data.marginSize
    yI = 0
    for j in range(len(data.floorPlan)):
        for i in range(len(data.floorPlan)):
            x0 = xI+tileSize*j
            y0 = yI+tileSize*i
            x1 = x0+tileSize
            y1 = y0+tileSize
            color = "white"
            if i==int(data.player.pX) and j == int(data.player.pY):
                color="red"
            if data.floorPlan[i][j]!=0:
                color = "black"
            if i == int(data.finishSprite.pX) and j== int(data.finishSprite.pY):
                color = "lawn green"
            canvas.create_rectangle(x0,y0,x1,y1,fill=color,width = 0)
    
####################################
#     __  ____    ________   _____ __             __           
#    /  |/  / |  / / ____/  / ___// /_____ ______/ /____  _____
#   / /|_/ /| | / / /       \__ \/ __/ __ `/ ___/ __/ _ \/ ___/
#  / /  / / | |/ / /___    ___/ / /_/ /_/ / /  / /_/  __/ /    
# /_/  /_/  |___/\____/   /____/\__/\__,_/_/   \__/\___/_/     
#                                                              
###################################
#taken from 112 course notes
#Its been eddited from its original version(added debouncer for key holds)
####################################

def run(width=1200, height=750):
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
        
    def keyReleasedWrapper(event,canvas,data):
        keyReleased(event,data)
       
    #
    #LEFT ARROW KEY
    #
    def leftPressWrapper(event,canvas,data):
        leftPress(event,data)
        redrawAllWrapper(canvas,data)
        
    def leftReleaseWrapper(event,canvas,data):
        leftRelease(event,data)
    #
    #Right ARROW KEY
    #
    def rightPressWrapper(event,canvas,data):
        rightPress(event,data)
        redrawAllWrapper(canvas,data)
        
    def rightReleaseWrapper(event,canvas,data):
        rightRelease(event,data)
    #==========================================================================
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
    data.timerDelay = 20 # milliseconds
    root = Tk()
    root.title("Advanced Ball Collection")
    root.resizable(width=False, height=False) # prevents resizing window
    init(data)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    # set up events
    """
    The script debouncer.py is not my own,
    reference <https://github.com/adamheins/tk-debouncer>
    """
    
    def pressedMain(event):
        keyPressedWrapper(event, canvas, data)
    def releasedMain(event):
        keyReleasedWrapper(event,canvas,data)
    
    debouncerMovement = Debouncer(pressedMain, releasedMain)
    root.bind("<KeyPress>", debouncerMovement.pressed)
    root.bind("<KeyRelease>", debouncerMovement.released)
    
    
    
    #
    #LEFT ARROW KEY
    #
    def pressLeft(event):
        leftPressWrapper(event,canvas,data)
        rightReleaseWrapper(event,canvas,data)
    def releaseLeft(event):
        leftReleaseWrapper(event,canvas,data)
    debouncerLeft = Debouncer(pressLeft,releaseLeft)
    root.bind("<KeyPress-Left>", debouncerLeft.pressed)
    root.bind("<KeyRelease-Left>",debouncerLeft.released)
    
    
    #
    #Right ARROW KEY
    #
    def pressRight(event):
        rightPressWrapper(event,canvas,data)
        leftReleaseWrapper(event,canvas,data)
    def releaseRight(event):
        rightReleaseWrapper(event,canvas,data)
    debouncerRight = Debouncer(pressRight,releaseRight)
    root.bind("<KeyPress-Right>", debouncerRight.pressed)
    root.bind("<KeyRelease-Right>",debouncerRight.released)
    
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed