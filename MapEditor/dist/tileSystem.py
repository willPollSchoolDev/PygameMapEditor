#TODO: json loading ; create chunk class ; create level class 

from typing import Text
import pygame
import sys
class Tile:
    def __init__(self,x,y,type,globalDatDict,scale = 1):
        self.x = x 
        self.y = y 
        
        
        self.type = type 


        self.index = 0 
        self.dict = globalDatDict

        for i in range(len(globalDatDict["text"])):
            if(globalDatDict["text"][i] == self.type):
                self.index = i 
            else:
                continue

        image = "data/graphics/filler.png"
        self.scale = scale
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image,(int(self.image.get_width()*scale),int(self.image.get_height()*scale)))
        
        self.body = self.image.get_rect(topleft=(x,y))


        
    
    def change(self,index):
        print(self.dict["text"][index])
        self.type = self.dict["text"][index]
        self.image = pygame.image.load(dict["path"][index])
        self.image = pygame.transform.scale(self.image,(int(self.image.get_width()*self.scale),int(self.image.get_height()*self.scale)))
        self.body = self.image.get_rect(topleft = (self.x,self.y))

    def onClick(self,position,index):
        if(self.body.collidepoint(position)):
            if pygame.mouse.get_pressed()[0] == 1:
                self.change(index)
    
    def render(self,viewport):
        viewport.blit(self.image,self.body)



class   Chunk:
    x = 0
    y = 0
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
        
        self.surf = pygame.Surface((sizeX*64,sizeY*64))
        self.surfBody = self.surf.get_rect(topleft=(Chunk.x,Chunk.y))

        Chunk.x += sizeX * 64

    def render(self):
        
        for x in range(self.length):
            for y in range(self.height):
                self.tileArray[x][y].render(self.surf)
            
    def renderChunk(self,viewport):
        self.render()
        viewport.blit(self.surf,self.surfBody)
    

    def onClick(self,pos,index):
            for x in range(self.length):
                for y in range(self.height):
                    self.tileArray[x][y].onClick(pos,index)
    





# test dictionary before json saving/loading is implemented
dict = {
    "types":["filler","ground","dirt","stone"],
    "path":["data/graphics/filler.png","data/graphics/ground.png","data/graphics/dirt.png","data/graphics/stone.png"]
}
