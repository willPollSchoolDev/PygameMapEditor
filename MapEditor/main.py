import json
import sys
from tileSystem import Chunk
import pygame

import improvedGui as gui

td = {}

with open("types.json",'r') as types:
    td = json.load(types)
activeIndex = 0


a = 0
pygame.init()

screen = pygame.display.set_mode((640+400,640+150))

p = gui.Panel()
p.load("types.json")
loadButton = gui.Button(0,650,"data/graphics/import.png","import tile",td)
downloadLevelButton = gui.Button(loadButton.masterRect.width + 10, 650,"data/graphics/download.png","download level",td)
c = Chunk(10,10,td)

while True:
    pos = pygame.mouse.get_pos(0)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if loadButton.onClick(pos):
                p.addAButton()
            a = p.onClick(pos)
    c.onClick(pos,a)
            
    
    p.render(screen)      
    loadButton.render(screen) 
    downloadLevelButton.render(screen)
    c.renderChunk(screen)
    pygame.display.update()