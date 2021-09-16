import pygame

class Tile:
    
    def resize(original,newScale):

        original = pygame.transform.scale(original,(int(original.get_width()*newScale),int(original.get_height()*newScale)))

    def __init__(self,x,y,texture,type,scale = 1):

        self.x = x 
        self.y = y 

        self.scale = scale

        self.type = type
        
        self.image = pygame.image.load(texture)

        Tile.resize(self.image,scale)

        self.body = self.image.get_rect(topleft=(x,y))
    
    def change(self,index,data):
        
        self.type = data["text"][index]

        self.image = pygame.image.load(data["path"][index])
        Tile.resize(self.image,self.scale)

    def onClick(self,position,data,index):
        
        if(self.body.collidepoint(position)):
            
            self.change(index,data)
    
    def render(self,viewport):
        
        viewport.blit(self.image,self.body)

class Layer:
    def __init__(self,num,length,height,data,scale = 1):
        self.length = length
        self.height = height
        
        # dictionary derived from file that contains file types and images
        self.data = data
        
        
        # number used by chunks for rendering order
        self.num = num

        self.tileArray = [[0] * height for i in range(length)]

        # fill the array with tiles 
        for x in range(length):
            for y in range(height):
                self.tileArray[x][y] = Tile(x * (32*scale),y * (32*scale),data["path"][0],data["text"][0],scale)

        self.layer = pygame.Surface((length * (32*scale),height * (32*scale)))
        self.layerRect = self.layer.get_rect()
    
    def render(self,viewport : pygame.Surface):
        for x in range(self.length):
            for y in range(self.height):
                self.tileArray[x][y].render(self.layer)
        
        viewport.blit(self.layer,self.layerRect)
    
    def onClick(self,position,index,data):
        for x in range(self.length):
            for y in range(self.height):
                self.tileArray[x][y].onClick(position,data,index)