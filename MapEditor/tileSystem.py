#TODO: json loading ; create chunk class ; create level class 

import pygame
import sys
class Tile:
    def __init__(self,x,y,type,globalDatDict,scale = 1):
        self.x = x 
        self.y = y 
        
        
        self.type = type 


        self.index = 0 
        self.dict = globalDatDict

        for i in range(len(globalDatDict["types"])):
            if(globalDatDict["types"][i] == self.type):
                self.index = i 
            else:
                continue

        image = globalDatDict["path"][self.index]
        self.scale = scale
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image,(int(self.image.get_width()*scale),int(self.image.get_height()*scale)))
        
        self.body = self.image.get_rect(topleft=(x,y))


        
    
    def change(self):
        if(self.index + 1 >= len(self.dict["types"])):
            self.index = 0
        else:
            self.index += 1 
        self.type = self.dict["types"][self.index]

        self.image = pygame.image.load(dict["path"][self.index])
        self.image = pygame.transform.scale(self.image,(int(self.image.get_width()*self.scale),int(self.image.get_height()*self.scale)))
        self.body = self.image.get_rect(topleft = (self.x,self.y))

    def onClick(self,position):
        if(self.body.collidepoint(position)):
            self.change()
    
    def render(self,viewport):
        viewport.blit(self.image,self.body)



class Layer:
    
    def __init__(self,sizeX,sizeY,tileDict):
        self.length = sizeX
        self.height = sizeY

        self.giveToTile = tileDict

        self.tileArray = [[0]*sizeY for x in range(sizeX)]
        self.typeArray = [[0]*sizeY for x in range(sizeX)]
        for x in range(self.length):
            for y in range(self.height):
                self.tileArray[x][y] = Tile(x*64,y*64,"filler",self.giveToTile,2)
                self.typeArray[x][y] = self.tileArray[x][y].type
        

    def render(self,viewport):
        for x in range(self.length):
            for y in range(self.height):
                self.tileArray[x][y].render(viewport)
    

    def onClick(self,pos):
        for x in range(self.length):
            for y in range(self.height):
                self.tileArray[x][y].onClick(pos)



class Chunk:
    def __init__(self,sizeX,sizeY,tileData):
        self.layerNum = 0 
        self.length = sizeX
        self.height = sizeY
        self.passOn = tileData
        self.layerDict = {
            "layers":[],
            "layer number":[]
        }
    
    def addLayers(self):
        self.layerDict["layers"].append(Layer(self.length,self.height,self.passOn))
        self.layerDict["layer number"].append(self.layerNum)
        self.layerNum += 1 
    
    def renderLayers(self,viewport):
        for x in range(len(self.layerDict["layers"])):
            self.layerDict["layers"].render(viewport)

# test dictionary before json saving/loading is implemented
dict = {
    "types":["filler","ground","dirt","stone"],
    "path":["data/graphics/filler.png","data/graphics/ground.png","data/graphics/dirt.png","data/graphics/stone.png"]
}
l = Layer(10,10,dict)

pygame.init()
screen = pygame.display.set_mode((640,640))

while True:
    pos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            l.onClick(pos)
    l.render(screen)
    pygame.display.update()



