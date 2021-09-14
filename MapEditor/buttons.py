from os import path
import pygame
import json
import tkinter as tk
import shutil
from tkinter.filedialog import askopenfile
pygame.font.init()



pathToSave = ""


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




class TileButton:
    def __init__(self,x,y,texture,text):
        self.x = x 
        self.y = y 
        self.textA = text
        if texture is not None:
            self.image = pygame.image.load(texture)
        self.imageRect = self.image.get_rect()

        self.font  = pygame.font.Font('freesansbold.ttf', 16)
        self.text = self.font.render(text,True,(0,0,0),(255,253,208))

        self.textRect = self.text.get_rect()
        if(self.textRect.width > self.imageRect.width):
            self.masterSurface = pygame.Surface((self.textRect.width+5,self.image.get_height()+1+self.textRect.height))
        elif(self.imageRect.width > self.textRect.width):
            self.masterSurface = pygame.Surface((self.imageRect.width+5,self.image.get_height()+1+self.textRect.height))


        self.masterSurface.fill((255,253,208))
        self.imageRect.midtop = (self.masterSurface.get_width()//2,0)
        self.textRect.midbottom = (self.masterSurface.get_width()//2,self.imageRect.top + 50)
        self.clicked = False

        

    def render(self,screen):
        self.masterSurface.blit(self.image,self.imageRect)
        self.masterSurface.blit(self.text,self.textRect)
        screen.blit(self.masterSurface,(self.x,self.y))
    
    def getWidth(self):
        return self.masterSurface.get_width()
    def getHeight(self):
        return self.masterSurface.get_height()

    def onClick(self,screen):
        pass
    
class Panel: 
    PANEL_SIZE_X = 400
    PANEL_SIZE_Y = 600
    BOTTOM_PANEL_X = 1200
    BOTTOM_PANEL_Y= 150
    def __init__(self,surfX,surfY):
        self.area = pygame.Surface((Panel.PANEL_SIZE_X,Panel.PANEL_SIZE_Y))
        self.areaRect = self.area.get_rect(topleft = (surfX,surfY))
        self.area.fill((255,253,208))
        self.buttonLocationX = 10
        self.buttonLocationY = 0
        self.buttonArray = []
        self.bottomArea = pygame.Surface((Panel.BOTTOM_PANEL_X,Panel.BOTTOM_PANEL_Y))
        self.bottomArea.fill((255,253,208))
        self.font  = pygame.font.Font('freesansbold.ttf', 16)
        self.addButtonText = self.font.render("add",True,(0,0,0),(255,253,208))
        self.addButtonRect = self.addButtonText.get_rect(topleft = (0,0))
        
        
    def createButton(self,data):
        self.buttonArray.append(TileButton(self.buttonLocationX,self.buttonLocationY,data["path"],data["type"]))


    def addButton(self,data):
        for b in range(len(self.buttonArray)):
            self.typetemp = self.buttonArray[b].textA
        breakFromX = False
        for x in range(len(data["path"])):
            for button in range(len(self.buttonArray)):
                if(self.buttonArray[button].textA == data["path"][x]):
                    break
                    breakFromX = True
            if breakFromX: continue
            self.createButton(data)

                
                    
       
        self.buttonLocationX += self.buttonArray[len(self.buttonArray)-1].getWidth() * 2 
        if(self.buttonLocationX == 390):
            self.buttonLocationY += self.buttonArray[len(self.buttonArray)-1].getHeight() * 2
    
        
    def save(self):
        global pathToSave
        dict= {}
        with open("types.json",'r') as types:
            dict = json.load(types)
            dict["type"].append(getName(pathToSave))
            dict["path"].append(pathToSave)
        with open("types.json",'w') as types:
            json.dump(dict,types)
        self.loadButtons("types.json")
        
    def addButtonOnClick(self,position):
           ws.mainloop()
           self.save()
           


    def render(self,screen):
        for button in self.buttonArray:
            button.render(self.area)
        screen.blit(self.bottomArea,(0,600))
        self.bottomArea.blit(self.addButtonText,self.addButtonRect)
        screen.blit(self.area,self.areaRect)

    def loadButtons(self,file):
        with open(file) as toLoad:
            dict = json.load(toLoad)
            
            for type in range(len(dict["type"])):
                tempDict = {
                    "type":dict["type"][type],
                    "path":dict["path"][type]
                }
                self.addButton(tempDict)


pygame.init()
VIEWPORT_X = 800+400
VIEWPORT_Y = 600



screen = pygame.display.set_mode((VIEWPORT_X,VIEWPORT_Y+Panel.BOTTOM_PANEL_Y))
panel = Panel(VIEWPORT_X-Panel.PANEL_SIZE_X,VIEWPORT_Y-Panel.PANEL_SIZE_Y)
panel.loadButtons("types.json")

while True:
    pos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            panel.addButtonOnClick(pos)
    panel.render(screen)
    pygame.display.update()
    