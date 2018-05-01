import pygame
import constants
import player
import enemies
import projectile
import fx
pygame.init()
#list of things
players = pygame.sprite.Group()
attacks = pygame.sprite.Group()
enemeys = pygame.sprite.Group()
enemeyattacks = pygame.sprite.Group()
huds = pygame.sprite.Group()
backgrounds = pygame.sprite.Group()
FX = pygame.sprite.Group()
temp = pygame.sprite.Group()
#inialize screen
backgroundAngle = 0
screen = pygame.display.set_mode(constants.screenSize)
pygame.display.set_caption("1943")

class backgroundTile(pygame.sprite.Sprite):
    
    def __init__(self,x,y,image,size):
        super().__init__()
        self.size=size
        tempsheet = pygame.image.load(constants.getImage(image)+".png")
        imageSize=tempsheet.get_size()
        self.nTim = imageSize[1]/constants.backgroundScroll
        self.Tim=self.nTim
        self.tim=0
        self.spritesheet = pygame.Surface([10*imageSize[0], 10*imageSize[1]])
        self.angle=0
        for i in range(10):
            for j in range(10):
                self.spritesheet.blit(tempsheet,(i*imageSize[0],j*imageSize[1]))
        self.rect =None
        self.rotate(0)
        
        
        #self.image.blit(self.spritesheet,(0,0),(0,0,size[0],size[1]))
        #self.image=self.spritesheet
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def check(self):
        if self.rect.right<0 or self.rect.left>constants.screenSize[0]:
            self.kill()
            return "new"
        if self.rect.bottom<0 or self.rect.top>constants.screenSize[1]:
            self.kill()
            return "new"
    def rotate(self,angle):
        center=None
        if self.rect!=None:
            center = self.rect.center
        self.angle+=angle
        temp = pygame.transform.rotate(self.spritesheet,self.angle)
        self.image=pygame.Surface((2*self.size[0],2*self.size[1]))
        imageSize=temp.get_size()
        self.image.blit(temp,(0,0),(imageSize[0]/2-self.size[0]/2,imageSize[1]/2-self.size[1]/2,2*self.size[0],2*self.size[1]))
        self.rect = self.image.get_rect()
        if center != None:
            self.rect.center=center
        self.Tim=self.nTim/abs(constants.math.cos(self.angle*constants.math.pi/180))
        
    def move(self):
        self.rect.y+=constants.backgroundScroll
        self.tim+=1
        if self.tim>self.Tim:
            self.rect.y-=(constants.backgroundScroll*self.Tim+constants.backgroundScroll)
            self.tim=0

        
        

def spawn():
    e=enemies.strafer([100,constants.screenSize[0]-100],-10,constants.math.pi/2)
    enemeys.add(e)

def explode(obj):
    bits = fx.makeExplosion(obj)
    for i in bits:
        FX.add(i)
def drawall():
    global screen
    screen.fill((0,0,255))
    backgrounds.draw(screen)
    players.draw(screen)
    attacks.draw(screen)
    enemeys.draw(screen)
    enemeyattacks.draw(screen)
    huds.draw(screen)
    FX.draw(screen)
    for i in players:
        if i.iframesCount>0:
            screen=fx.flicker(i,screen)
        
    pygame.display.flip()


         
def fillBackground():
    e=backgroundTile(-50,1-constants.screenSize[1],"water",(2*constants.screenSize[0]+100,2*constants.screenSize[1]+100))
    backgrounds.add(e)  

def newBackground():
    e=backgroundTile(-50,1-constants.screenSize[1],"water",(constants.screenSize[0]+100,constants.screenSize[1]))
    backgrounds.add(e)

def moveWorld():
    for i in backgrounds:
        i.move() 
    for i in attacks:
        pass
    for i in enemeys:
        i.rect.y+=constants.backgroundScroll
    for i in enemeyattacks:
        pass
        
    '''
    new=True
    for i in backgrounds:
        if i.rect.top<0:
            new=False
    if new==True:
        newBackground()
    for i in backgrounds:
        i.rect.y+=constants.backgroundScroll
        i.check()
   '''  
    
def rotate(angle):
    #all the stuff needs to be rotated
    
    for i in backgrounds:
        i.rotate(angle)