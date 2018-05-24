import pygame
import constants as C
import projectile
import random
pygame.init()
'''
make a big plane flying upwards slowly lowers to just most of the upper screen
secioned weekspots and turrets 
no onhit for player but has rapit fire turets
drifts back and forth
'''
def closest(me,possible):
    end=None
    distance=None
    for i in possible:
        if distance==None:
            end=i
            distance=((me.rect.center[0]+i.rect.center[0])**2+(me.rect.center[1]+i.rect.center[1])**2)**.5
        elif distance > ((me.rect.center[0]+i.rect.center[0])**2+(me.rect.center[1]+i.rect.center[1])**2)**.5:
            distance = ((me.rect.center[0]+i.rect.center[0])**2+(me.rect.center[1]+i.rect.center[1])**2)**.5
            end=i
    return end

class turret(pygame.sprite.Sprite):
    def __init__(self,x,y,size):
        super().__init__()
        self.origimage = pygame.Surface(size)
        self.origimage.fill((255,255,255))
        self.origimage.set_colorkey((255,255,255))
        self.rect=self.origimage.get_rect()
        pygame.draw.circle(self.origimage,(0,0,0),[int(self.rect.width/2),int(self.rect.height/2)],int(self.rect.width/4))
        self.relative = [int(x),int(y)]
        self.turretAngle=0
        self.image = self.origimage 
        self.mode = "basic"
        self.firecount = 5
    def setloc(self,x,y):
        self.rect.x=x+self.relative[0]-self.rect.width/2
        self.rect.y=y+self.relative[1]-self.rect.height/2 
    def update(self,playerlist,attacklist):
        
        
        target = closest(self,playerlist)
        if target == None:
            return None
        targetangle = C.vectorToAngle([self.rect.center[0]-target.rect.center[0],self.rect.center[1]-target.rect.center[1]])
        if abs(self.turretAngle-targetangle)>2*3:
            self.turretAngle=targetangle
        self.turretAngle=(self.turretAngle+targetangle)/2        
        self.firecount+=1
        if self.mode=="basic"and self.firecount>30:
            
            anglelinepos=C.angleToVector(self.turretAngle,self.rect.width/2)         
            self.firecount=0
            return("ea",projectile.shot(self.rect.center[0]-anglelinepos[0],self.rect.center[1]-anglelinepos[1],self.turretAngle+3.1415))
        elif self.mode=="circle" and self.firecount>10:
            self.turretAngle+=.5
            self.firecount=0
            return("ea",projectile.shot(self.rect.center[0]-anglelinepos[0],self.rect.center[1]-anglelinepos[1],self.turretAngle+3.1415))            
        anglelinepos=C.angleToVector(self.turretAngle,self.rect.width/2) 
        self.image=self.origimage.copy()
        pygame.draw.line(self.image,(0,0,0),(self.rect.width/2,self.rect.height/2),[self.rect.width/2-anglelinepos[0],self.rect.height/2-anglelinepos[1]],5)        
    def crash(self):
        return "nocolide"    
class WeakPoint(pygame.sprite.Sprite):
    def __init__(self,image,x,y):
        super().__init__()
        self.image = image
        
        self.image.set_colorkey(self.image.get_at((0,0)))
        self.rect = self.image.get_rect()
        self.relative = [int(x),int(y)]
        self.setloc(0,0)
        self.flicker = True
        self.health=10
        self.maxHealth = 10
        
    def setloc(self,x,y):
        self.rect.x=x+self.relative[0]
        self.rect.y=y+self.relative[1]
    def update(self,playerlist,attacklist):
        self.rect.y-=C.backgroundScroll
        hits=pygame.sprite.spritecollide(self, attacklist, False)
        for i in hits:
            temp=i.hit()
            self.health-=temp
        
    def crash(self):
        return "nocolide"
MAXSPEED = 1
accelfactor=3
class bigPlane(pygame.sprite.Sprite):
    def gs(self,x,y,dx,dy):
        gsimage = pygame.Surface([dx, dy])
        gsimage.fill((234,154,45))
        gsimage.set_colorkey((234,154,45))
        gsimage.blit(self.spritesheet,(0,0),(x,y,dx,dy))
        return gsimage    
    def __init__(self,x,y):#50,38
        super().__init__()
        self.spritesheet = pygame.image.load("assets/boss.png")
        animations = [self.gs(0,38*2,50,38),self.gs(50,38*2,50,38)]
        for t in range(4):
            for i in range(len(animations)):
                animations[i] = pygame.transform.scale2x(animations[i])
        self.image=animations[0]
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        
        self.leftWingSpot = self.makeWeakPoints(6*16,11*16,4*17,4*17,50)#6,11
        self.rightWingSpot = self.makeWeakPoints(self.rect.width-6*16-4*17,11*16,4*17,4*17,50)#6,11
        self.weakspots = [self.leftWingSpot,self.rightWingSpot]
        
        self.turret = turret(self.rect.width/2,self.rect.height/2,[32,32])
        self.turrets = [self.turret]
        #
        if 1==random.randint(0,1):
            self.headingPrime=[1,0] #where I want to go
        else:
            self.headingPrime=[-1,0]
        self.heading=[0,0]#current speed
        
        self.first = True
    def update(self,playerlist,attacklist):
        
        self.accel()
        self.speed()
        self.pos()
        for i in self.weakspots:
            i.setloc(self.rect.x,self.rect.y)
        for i in self.turrets:
            i.setloc(self.rect.x,self.rect.y)
        if self.first==True:
            self.first=False
            return ("ep",self.leftWingSpot,self.rightWingSpot,self.turret)        
    def crash(self):
        return "nocolide"
    def makeWeakPoints(self,x,y,dx,dy,health):#pygame.transform.chop()
        croped = pygame.Surface((dx,dy))
        croped.blit(self.image,(0,0),(x,y,dx,dy))
        return WeakPoint(croped,x,y)
        
    def accel(self):
        if self.rect.left<-100+random.randint(-50,50):
            self.headingPrime[0] = 1
        elif self.rect.right>C.screenSize[0]+100+random.randint(-50,50):
            self.headingPrime[0] = -1
        if self.rect.top<-100+random.randint(-50,50):
            self.headingPrime[1] = 1
        elif self.rect.bottom>C.screenSize[1]+100+random.randint(-50,50):
            self.headingPrime[1] = -1
    def speed(self):
        if self.headingPrime[0]>0 and self.heading[0] < MAXSPEED:
            self.heading[0]+=self.headingPrime[0]/accelfactor
        elif self.headingPrime[0]<0 and self.heading[0] > -MAXSPEED:
            self.heading[0]+=self.headingPrime[0]/accelfactor
        if self.headingPrime[1]>0 and self.heading[1] < MAXSPEED:
            self.heading[1]+=self.headingPrime[1]/accelfactor
        elif self.headingPrime[1]<0 and self.heading[1] > -MAXSPEED:
            self.heading[1]+=self.headingPrime[1]/accelfactor
    def pos(self):
        self.rect.x+=self.heading[0]
        self.rect.y+=self.heading[1]