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
RUBBLESPEED = 4
class rubble(pygame.sprite.Sprite):
    def __init__(x,y,color=(0,0,0),size=[1,1],direction=None,duration=60*6):
        self.image = pygame.Surface(size)
        self.image.fill(color)
        self.rect=self.image.get_rect()
        self.rect.x = x+self.rect.width/2
        self.rect.y = y+self.rect.height/2
        self.heading = direction
        if direction==None:
            direction=random.uniform()*2*constants.math.pi
            self.heading = constants.angleToVector(direction,RUBBLESPEED)
        self.count = duration
    def update():
        self.rect.x+=self.heading[0]
        self.rect.y+=self.heading[1]
        self.count-=1
        
        if self.count <1:
            self.kill()
        if abs(self.rect.x-constants.screenSize[0]/2)>50+constants.screenSize[0]/2 or abs(self.rect.y-constants.screenSize[1]/2)>50+constants.screenSize[1]/2:
            self.kill()        
def makeExplosion(obj):
    end = []
    for i in range(10):
        end.append(rubble(obj.rect.center[0],obj.rect.center[1]))
    return end
    #returns a list of ruble objs to show an explosion