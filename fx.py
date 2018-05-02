import pygame
import random
import constants
pygame.init()


    
    
def outlineObject(thing):
    #return the outline in a image or nothing
    end = pygame.Surface((thing.rect.width,thing.rect.height))
    mask = pygame.mask.from_surface(thing.image)
    points=mask.outline()
    end.set_colorkey((0,0,0))
    pygame.draw.polygon(end, (255,255,255), points, 1)
    
    return end
def flicker(thing,screen):
    if random.randint(0,1):
        screen.blit(outlineObject(thing),thing.rect)
    return screen
def sheild(rect,screen):
    if random.randint(0,1):
        pygame.draw.ellipse(screen,(255,200,200),rect,3)
    return screen    
RUBBLESPEED = 9
class rubble(pygame.sprite.Sprite):
    def __init__(self,x,y,color=(0,255,0),size=[2,2],direction=None,duration=60*6):
        super().__init__()
        self.image = pygame.Surface(size)
        self.image.fill(color)
        self.rect=self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.heading=[0,0]
        self.heading = direction
        if direction==None:
            direction=random.uniform(0,1)*2*constants.math.pi
            self.heading = constants.angleToVector(direction,RUBBLESPEED+random.randint(-4,4))
        self.count = duration
    def update(self):
        if self.count%3==0:
            self.rect.x+=self.heading[0]
            self.rect.y+=self.heading[1]
        self.count-=1
        
        if self.count <1:
            self.kill()
        if abs(self.rect.x-constants.screenSize[0]/2)>50+constants.screenSize[0]/2 or abs(self.rect.y-constants.screenSize[1]/2)>50+constants.screenSize[1]/2:
            self.kill() 

def makeExplosion(obj):
    end = []
    
    colors = []
    for x in range(obj.image.get_width()):
        tower=[]
        for y in range(obj.image.get_height()):
            tower.append(obj.image.get_at((x,y)))
        colors.append(tower)
    brickSize = [5,5]
    y=0
    while y <len(colors[0]):
        x=0
        while x < len(colors):#main index
            if colors[x][y][0:3] != constants.ColorKey:
                end.append(rubble(obj.rect.x+x,obj.rect.y+y, size = brickSize, color = colors[x][y][0:3]))
                x+=2
            else:
                x+=1
            
        y+=2
            
    return end
    #returns a list of ruble objs to show an explosion