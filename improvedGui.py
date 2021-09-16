from os import path
import pygame
import json
import tkinter as tk
import shutil
from tkinter.filedialog import askopenfile

from pygame.image import load
pygame.font.init()



pathToSave = ""
activeIndex = 0


def importFile(oPath,type,quit):
    """Imports the file from the given path to the given new path \n
        Keyword arguments: \n
        oPath -- original path of the file given as a raw string \n
        nPath -- new path of the file given as a raw string \n
    """
    global pathToSave
    nPath = f"data/graphics/{type}.png"
    rOPath = r"{}".format(oPath)
    shutil.move(rOPath,nPath)
    quit.destroy()
    
    pathToSave = nPath
def getName(path):
    path = path.replace("data/graphics/",'')
    path = path.replace(".png",'')
    return path
def formatPath(path):
    """Formats a path gotten from the open_file() function so that it can be used in the importFile() function \n
       Keyword arguments: \n
       path -- the string to be formatted
    """
    temp = str(path)
    temp = temp.replace("<_io.TextIOWrapper name='",'')
    temp = temp.replace("' mode='r' encoding='cp1252'>",'')
    return temp
def getFile():
    global pathToSave
    file_path = askopenfile(mode='r',filetypes=[('Image Files', '*png')])
    file_path = formatPath(file_path)
    pathToSave = file_path

ws = tk.Tk()
tk.Label(ws,text="type").grid(row = 0)
tk.Label(ws,text="file").grid(row=1)
tt = tk.Entry(ws)
tt.grid(row = 0,column= 1)
file = tk.Button(ws,
    text="import",
    command=lambda: getFile())
file.grid(row=1,column=1)
done = tk.Button(ws,
    text='add',
    command=lambda:importFile(pathToSave,tt.get(),ws)).grid(row=2)

class Button:
    def __init__(self,x,y,texture,text,buttonData):
        self.x = x 
        self.y = y 
        self.text = text
        self.selectTexture = texture

        self.buttonData = buttonData

        self.font  = pygame.font.Font("data/graphics/ROADSTORE Dafont.ttf", 16)

        self.textToRender = self.font.render(text,True,(0,0,0),(255,253,208))
        self.textRect = self.textToRender.get_rect()

        print(texture)
        self.image = pygame.image.load(texture)
        self.imageRect = self.image.get_rect()  

        if(self.textRect.width > self.imageRect.width):
            self.masterSurface = pygame.Surface((self.textRect.width+5,self.imageRect.height+self.textRect.height+1))
        else:
            self.masterSurface = pygame.Surface((self.imageRect.width+5, self.imageRect.height+self.textRect.height+1))

        self.imageRect.midtop = (self.masterSurface.get_width()//2,0)
        self.textRect.midtop = (self.masterSurface.get_width()//2,self.imageRect.bottom)

        self.masterSurface.fill((255,253,208))

        self.masterRect = self.masterSurface.get_rect(topleft=(x,y))
    
    def render(self,viewport):
        self.masterSurface.blit(self.image,self.imageRect)
        self.masterSurface.blit(self.textToRender,self.textRect)
        viewport.blit(self.masterSurface,self.masterRect)
    
    def selectTile(self):
        for i in range(len(self.buttonData["text"])):
            if self.text == self.buttonData["text"][i]:
                return i 



    def onClick(self,position):
        
        if self.masterRect.collidepoint(position):
            return True
        
    


    def getWidth(self):
        return self.masterSurface.get_width()

    def getHeight(self):
        return self.masterSurface.get_height()



class Panel:

    SIZE_X=400
    SIZE_Y=640

    BOTTOM_X=400+640
    BOTTOM_Y=200

    def __init__(self):
        self.area = pygame.Surface((Panel.SIZE_X,Panel.SIZE_Y))
        self.areaRect = self.area.get_rect(topleft = (640,0))
        self.area.fill((255,253,208))
        
        self.buttonX = 10
        self.buttonY = 0

        self.buttonArray = []

        self.bottomArea = pygame.Surface((Panel.BOTTOM_X,Panel.BOTTOM_Y))
        self.bottomAreaRect = self.bottomArea.get_rect(topleft=(0,Panel.SIZE_Y))
        self.bottomArea.fill((255,253,208))

    def addButtons(self,buttonData):
        self.buttonX = 0
        self.buttonY = 0
        self.indexToPass = 0
        self.buttonArray = []
        for i in range(len(buttonData["text"])):
            self.buttonArray.append(Button(self.buttonX + 640,self.buttonY,buttonData["path"][i],buttonData["text"][i],buttonData))
        
            self.buttonX += self.buttonArray[len(self.buttonArray)-1].getWidth()*2
            if self.buttonX + self.buttonArray[len(self.buttonArray)-1].getWidth()*2 >= 400:
                self.buttonX = 0
                self.buttonY += self.buttonArray[len(self.buttonArray)-1].getHeight() * 2

    def addAButton(self):
        global pathToSave
        ws.mainloop()

        dict = {}
        with open("types.json",'r') as types:
            dict = json.load(types)
            dict["text"].append(getName(pathToSave))
            dict["path"].append(pathToSave)
        with open("types.json",'w') as types:
            json.dump(dict,types)
        self.load("types.json")
   
    def load(self,file):
        with open(file) as toLoad:
            dict = json.load(toLoad)
            self.addButtons(dict)

    def remove(self):
        dict = {}
        with open("types.json",'r') as types:
            dict = json.load(types)
            
            dict["text"].remove(dict["text"][len(dict["text"])-1])
            dict["path"].remove(dict["path"][len(dict["path"])-1])
        with open("types.json",'w') as types:
            json.dump(dict,types)
        
        self.load("types.json")
    
    def onClick(self,position):

        for b in range(len(self.buttonArray)):
            if self.areaRect.collidepoint(position):
                if self.buttonArray[b].onClick(position):
                     self.indexToPass = self.buttonArray[b].selectTile()
                     break
        return self.indexToPass
            
    def renderButtons(self,viewport):
        for b in range(len(self.buttonArray)):
            self.buttonArray[b].render(viewport)
           
    

    def render(self,viewport):
        viewport.blit(self.bottomArea,self.bottomAreaRect)
        viewport.blit(self.area,self.areaRect)
        self.renderButtons(viewport)

    

    
