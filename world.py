import pygame
import constants
import player
import enemies
import projectile
import fx
import bosses
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

        

#choes a random out of list
def spawn(difficulty):
    doublechance = constants.random.randint(0,10)
    if doublechance>difficulty:
        count = 1
    else:
        count=2
    for i in range(count):
        choice=constants.random.randint(0,100)

        if choice>90:

            power=constants.random.choice(["sheild",'life','snake','split','prox','auto','semi','laser'])
            e=powerUp(power)#list of powerups
    
        elif choice>60:

            e=enemies.Real_looper(constants.random.randint(10,constants.screenSize[0]-10),-20)#change x to one side to other side
    
        elif choice>40:

            x=constants.random.choice([-100,constants.screenSize[0]+100])
            y=constants.random.randint(100,constants.screenSize[1]-200)
            wings = constants.random.randint(1,10)
            sidet=constants.random.choice(["both","left","right"])
            dire = constants.random.choice([-1,1])
            e=enemies.SpinPlane(x,y,direction=dire,wing=wings,side=sidet) #change both x and y and both also change direction
    
        else:

            x=constants.random.randint(100,constants.screenSize[0]-100)
            sidet=constants.random.choice(["both","left","right"])
            wings = constants.random.randint(1,3)
            if sidet=="both":
                wings=(wings*2)+1
            e=enemies.strafer(x,-10,direction=1,wing=wings,side = sidet)#change both x and y
        enemeys.add(e)
    
def explode(obj,cheap = False):
    bits = fx.makeExplosion(obj,cheap)
    for i in bits:
        FX.add(i)
def drawall():
    global screen
    screen.fill((0,0,255))
    backgrounds.draw(screen)
    
    enemeys.draw(screen)
    players.draw(screen)
    attacks.draw(screen)
    enemeyattacks.draw(screen)
    
    for i in huds:
        if i.hidden == False:
            screen.blit(i.image, i.rect)
    
    FX.draw(screen)
    #quickclear
    if len(FX)>30:
        for i in FX:
            try:
                i.count-=5
            except:
                pass
    
    
    for i in players:
        if i.iframesCount>0:
            screen=fx.flicker(i,screen)
        if i.sheild==True:
            fx.sheild(i.rect,screen)
        if i.healthBar.getM()-i.healthBar.getV() > 0:
            blob = fx.smokeTrail(i.healthBar.getM()-i.healthBar.getV(),i.rect.center[0],i.rect.bottom)
            if blob!=None:
                FX.add(blob)
    for i in enemeys:
        try:
            if i.flicker == True:
                screen=fx.flicker(i,screen,line=3)
        except:
            pass
        try:
            if i.maxHealth-i.health>0:
                blob = fx.smokeTrail(i.maxHealth-i.health,i.rect.center[0],i.rect.center[1])
                if blob!=None:
                    FX.add(blob)
        except:
            pass    
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
class arrow(pygame.sprite.Sprite):
    def __init__(self,size,time):
        super().__init__()
        MyFont = pygame.font.Font(pygame.font.get_default_font(),30)
        self.image = MyFont.render(">",True,(0,0,0))
        self.rect = self.image.get_rect()
        self.count = time
    def setpos(self,x,y):
        self.rect.right = x
        self.rect.y = y-self.rect.height/2
    def update(self):
        self.count-=1
        if self.count<1:
            self.kill()    
class levelText(pygame.sprite.Sprite):
    def __init__(self,text,position,size,color,time):
        super().__init__()
        MyFont = pygame.font.Font(pygame.font.get_default_font(),size)
        self.image = MyFont.render(text,True,color)
        self.rect = self.image.get_rect()
        self.rect.x=position[0]-self.rect.width/2
        self.rect.y=position[1]-self.rect.height/2
        self.count = time
    def update(self):
        self.count-=1
        if self.count<1:
            self.kill()

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
'''
types:
sheild
life
snake
split
prox
auto
semi
laser
'''

class powerUp(pygame.sprite.Sprite):
    def __init__(self,powerUpType):
        super().__init__()
        self.powerUp = powerUpType
        #sort by type
        if self.powerUp=='sheild':
            image="shieldPU.png"
        elif self.powerUp=='life':
            image="lifePU.png"
        elif self.powerUp=='snake':
            image="snakePU.png"
        elif self.powerUp=='split':
            image="splitPU.png"
        elif self.powerUp=='prox':
            image="proxPU.png"
        elif self.powerUp=='auto':
            image="autoPU.png"
        elif self.powerUp=='semi':
            image="semiPU.png" 
        elif self.powerUp=='laser':
            image="laserPU.png"
        self.flicker = True
        self.image=pygame.image.load("assets/"+image)
        self.rect = self.image.get_rect()
        self.rect.x=-100
        self.rect.y=-100
        sidet=constants.random.choice(["both","left","right"])
        dire = constants.random.choice([-1,1])        
        s=enemies.SpinPlane(constants.random.choice([-100,constants.screenSize[0]+100]),300,direction=dire,side=sidet)
        enemeys.add(s)
        self.powerPlanes = pygame.sprite.Group()
        for i in s.collectKin():
            self.powerPlanes.add(i)
        self.powerPlanes.add(s)
        
    def update(self,playerlist,attacklist):

        if len(self.powerPlanes)>1:
            pass
        elif len(self.powerPlanes)==1:
            for i in self.powerPlanes:
                self.rect.center = i.rect.center
        else:
            self.rect.y+=constants.backgroundScroll
        if abs(self.rect.x-constants.screenSize[0]/2)>1000 or abs(self.rect.y-constants.screenSize[1]/2)>1000:
            self.kill()
    def crash(self):
        return "powerup"
        
        
        
def rotate(angle):
    #all the stuff needs to be rotated
    
    for i in backgrounds:
        i.rotate(angle)