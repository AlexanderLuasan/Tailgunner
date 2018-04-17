import pygame
import constants as C
import projectile

#draws health bar

#FPS/Playerframes converst calls to 1/60 seconds
frameMul=C.FPS/C.PlayerFPS 

class hudBar(pygame.sprite.Sprite):
    def __init__(self,x,y,side,maxV,currentV,color):
        super().__init__()
        self.maxV = maxV
        self.currentV = currentV
        self.side = side
        self.x=x
        self.y=y  
        self.color = color
        self.placebar()
        
        #place bar
        
    def placebar(self):
        self.image = pygame.Surface([10,self.maxV])
        self.image.fill((255,255,255))
        pygame.draw.rect(self.image,self.color,(0,0,10,self.currentV))
        self.rect = self.image.get_rect()
        if self.side=="left":
            self.rect. x = C.screenSize[0] - self.x - 10
        else:
            self.rect. x= self.x
        self.rect.y=self.y 
        
    def setv(self,cV):
        self.currentV = cV
        self.placebar()
    def setmaxv(self,newmax):
        self.maxV = newmax        
        self.placebar()
    def adjv(self,a):
        self.currentV += a
        if self.currentV>self.maxV:
            self.currentV=self.maxV
        self.placebar()
    def getV(self):
        return self.currentV
    def getM(self):
        return self.maxV   
        
    
class player(pygame.sprite.Sprite):
    
    def gs(self,x,y,dx,dy):
        gsimage = pygame.Surface([dx, dy])
        gsimage.fill((234,154,45))
        gsimage.set_colorkey((234,154,45))
        gsimage.blit(self.spritesheet,(0,0),(x,y,dx,dy))
        return gsimage
    
    def __init__(self,x,y,spritesheet,size):
        super().__init__() #(68,68) spaceing(0,0), (0,0)
        #setting up animation sets
        self.spritesheet = pygame.image.load(C.getImage(spritesheet)+".png")
        self.animation = []
        self.animation.append(['center none'])
        
        #what row angle of turret,what tillt every 8 is a set,fire side,fire front,prop up/down,
        #make main set
        for turretpos in range(12):#1
            tiltlist = []
            for tilt in range(4):#8
                sidelist = []
                for side in range(2):#4
                    frontlist= []
                    for front in range(2):#2
                        proplist = []
                        for prop in range(2):#1
                            proplist.append(self.gs(turretpos*68,(tilt*8+side*4+front*2+prop)*68,68,68))
                        frontlist.append(proplist)
                    sidelist.append(frontlist)
                tiltlist.append(sidelist)
            self.animation.append(tiltlist)
        # make relected set
        for turretpos in range(12,0,-1):#1
            tiltlist = []
            for tilt in range(4):#8
                sidelist = []
                for side in range(2):#4
                    frontlist= []
                    for front in range(2):#2
                        proplist = []
                        for prop in range(2):#1
                            proplist.append(pygame.transform.flip(self.animation[turretpos][tilt][side][front][prop],True,False))
                        frontlist.append(proplist)
                    sidelist.append(frontlist)
                tiltlist.append(sidelist)
            self.animation.append(tiltlist)
            
        #top roll animation set stage[6] firing[2] prop[2] 
        #animation for rolling and reflected
        self.toproll = []
        for stage in range(3):#stage
            frontlist = []
            for front in range(2): #2fire:
                proplist = []
                for prop in range(2):
                    proplist.append(pygame.transform.flip(self.gs(stage*68,(32)*68+(2*front+prop)*68,68,68),True,False))
                frontlist.append(proplist)
            self.toproll.append(frontlist)
        for stage in range(2,-1,-1):#stage
            frontlist = []
            for front in range(2): #2fire
                proplist = []
                for prop in range(2):
                    proplist.append(pygame.transform.flip(self.toproll[stage][front][prop],True,False))
                frontlist.append(proplist)
            self.toproll.append(frontlist)
            
        #rolling varables
        self.roll = 0 #never used
        self.rolling = False
        self.rollingDir = 0 #roll direction
        self.roolCount = 0 #setps in roll
        self.toprollspeed = [8,4,0,0,-4,-8]
        self.tim = 0#conting var for animations
        
        
        #intinal conditions
        self.image = self.animation[1][0][0][0][0]
        self.rect=self.image.get_rect()#center at x,y
        self.rect.x=x+self.rect.width/2
        self.rect.y=y+self.rect.height/2
        self.heading = [0,0] #speed
        self.headingPrime = [0,0] #acceration
        self.planeSpeed = 8 #normal planes speed
        self.accStep = 1 #jerk
        self.turetAngle = 0
        
        
        #turret
        
        self.turretheading = [0,0]
        self.turretPos = [1,1]
        self.turretPosDict = {(0,-1):(1,1),(-1,-1):(2,11),(-1,0):(4,9),(-1,1):(5,8),(0,1):(6,6),(1,1):(8,5),(1,0):(9,4),(1,-1):(11,2)}
        self.turrefireangle = [-1,-1]
        self.turretfire = False
        #stat bars
        self.healthBar = hudBar(20,C.screenSize[1]-100,"right",100,100,(255,0,0))
        self.gunBar = hudBar(40,C.screenSize[1]-100,"right",100,100,(255,255,0))
        
        self.airBar = hudBar(60,C.screenSize[1]-100,"right",100,100,(255,0,255))
        self.allbar = [self.airBar,self.gunBar,self.healthBar]
        #extra frame conter
        self.other = True
        #firing variables
        self.firecount=0
        self.firing=False        
        #dieing
        self.deathdelay = 0
        self.dead = False
        self.respawn= False
        self.repsawnTime = 0
        self.iframes=False
        
        
    def getHud(self):
        #returns all huds
        return (self.healthBar,self.gunBar,self.airBar)
    def fireToggle(self,state):
        #fire on or off
        self.firing=state
    def setTurretHeading(self,direction):
        #aim turret
        self.turretheading = (direction[0],direction[1])
        if self.turretheading!=(0,0):
            self.turretPos = self.turretPosDict[self.turretheading]
    def fireTurret(self):
        #fire an angled single 
        self.turretfire = True
 
    def fire(self):
        if self.firecount<1:
            if self.gunBar.getV()>5:
                self.firecount=6
                self.gunBar.adjv(-5)
                return True
            else:
                self.firecount=60 #jam
                self.firing=False
                return False
        else:
            return False
    
    def death(self):
        #call and it will handle the explosion
        self.deathdelay-=1
        if self.deathdelay<0:
            center = self.rect.center
            self.image = pygame.Surface([self.rect.width+2,self.rect.width+2])
            self.rect = self.image.get_rect()
            self.image.fill((0,0,0))
            pygame.draw.circle(self.image,(255,0,0),((int(self.rect.width/2),int(self.rect.width/2))),int(self.rect.width/2))
            self.image.set_colorkey((0,0,0))
            self.rect.center = center
            self.deathdelay = 2
            self.dead = True
        if self.rect.width>200:
            self.deathdelay = 10
            self.respawn= True
            self.iframes=True
            return("respawn",(self.rect.center))
    def setRoll(self,direction):
        #to enter a roll and set tillt
        self.roll = direction
        if self.heading[0]<=-1.5*self.planeSpeed and self.roll<0:
            if self.rolling !=True:
                self.rollcount=len(self.toproll)-1            
            if self.airBar.getV()>60:
                self.rolling=True
                self.iframes=True
            self.rollDir=self.roll
            
        elif self.heading[0]>=1.5*self.planeSpeed and self.roll>0:
            if self.rolling !=True:
                self.rollcount=0
            if self.airBar.getV()>60:
                self.rolling=True
                self.iframes=True
            self.rollDir=self.roll
    def adjustHeading(self,direction):
        #shift heading
        self.headingPrime[0] +=direction[0]
        self.headingPrime[1] +=direction[1]
    def setHeading(self,direction):#not used but keept
        self.heading = direction
    def adjustRoll(self,direction):#not used
        self.roll+=direction
    def animate(self):
        #sets animation
        #animation #[turretpos][tilt][side][front][prop]
        self.tim= self.tim + 1
        if self.tim%4 > 1:
            prop=1 
            if self.tim>20:
                self.tim=0
        else:
            prop=0   
        if self.firing:
            front = 1
        else:
            front = 0
        if self.turretfire:
            side = 1
        else:
            side = 0        
        if self.rolling == True:
            if self.airBar.getV()>1:
                self.airBar.adjv(-1)
                
                if self.tim>5:
                    self.tim=0
                    if self.rollDir<0:
                        self.image=self.toproll[self.rollcount][front][prop]
                        self.heading[0] = self.toprollspeed[self.rollcount]
                        self.rollcount+=self.rollDir
                        if self.rollcount<0:
                            self.heading[0]=1.5*self.planeSpeed
                            self.rolling=False
                            self.iframes=False
                    elif self.rollDir>0:
                        self.image=self.toproll[self.rollcount][front][prop]
                        self.heading[0] = self.toprollspeed[self.rollcount]
                        self.rollcount+=self.rollDir
                        if self.rollcount>=len(self.toproll):
                            self.heading[0]=-1.5*self.planeSpeed
                            self.rolling=False
                            self.iframes=False                
            else:
                self.rolling=False
        else:
            self.airBar.adjv(1)
            tilt = abs(int(self.heading[0]/4))
            if self.heading[0]>0:
                if len(self.animation[-1])>tilt:
                    if self.turretPos[1]>9 and tilt>1:
                        self.image = self.animation[-9][tilt][side][front][prop]
                    else:
                        self.image = self.animation[-1*self.turretPos[1]][tilt][side][front][prop]
                    
            elif self.heading[0]<0:
                if len(self.animation[1])>tilt:
                    if self.turretPos[0]>9 and tilt>1:
                        self.image = self.animation[9][tilt][side][front][prop]
                    else:                    
                        self.image = self.animation[1*self.turretPos[0]][tilt][side][front][prop]
            else:
                self.image = self.animation[1*self.turretPos[0]][tilt][side][front][prop]
            
    def update(self,enimies,attacks):
        #die
        if self.healthBar.currentV<0:
            return self.death()
        #acceeration:
        if self.headingPrime[0]>0 and (self.heading[0]<self.planeSpeed or (self.roll>0 and self.heading[0]<1.5*self.planeSpeed)):
            self.heading[0]+=self.accStep
        elif self.headingPrime[0]<0 and (self.heading[0]>-1*self.planeSpeed or (self.roll<0 and self.heading[0]>-1.5*self.planeSpeed)):
            self.heading[0]-=self.accStep
        elif self.headingPrime[0] == 0 and self.heading[0]!=0:
            if self.heading[0]>0:
                self.heading[0]-=self.accStep
            else:
                self.heading[0]+=self.accStep
                
        if self.headingPrime[1]>0 and self.heading[1]<self.planeSpeed:
            self.heading[1]+=self.accStep
        elif self.headingPrime[1]<0 and self.heading[1]>-self.planeSpeed:
            self.heading[1]-=self.accStep
        elif self.headingPrime[1] == 0 and self.heading[1]!=0:
            if self.heading[1]>0:
                self.heading[1]-=self.accStep
            else:
                self.heading[1]+=self.accStep
        
        
        self.animate()
    
        
        #speed
        if abs(self.heading[0])==abs(self.heading[1]) and self.heading[1]!=0:
            self.rect.x += self.heading[0]/2*2**.5/2
            self.rect.y += self.heading[1]/2*2**.5/2
        else:
            self.rect.x += self.heading[0]/2
            self.rect.y += self.heading[1]/2

        #prevent moving off edge
        if self.rect.x<0:
            self.rect.x=0
        elif self.rect.x>C.screenSize[0]-self.rect.width:
            self.rect.x=C.screenSize[0]-self.rect.width
        if self.rect.y<0:
            self.rect.y=0
        elif self.rect.y>C.screenSize[1]-self.rect.height:
            self.rect.y=C.screenSize[1]-self.rect.height
        
        #shot the gun on a clock
        if self.firecount>0:
            self.firecount-=1
        if self.firing==False and self.gunBar.getV()<self.gunBar.getM():
            if self.other == True:
                self.gunBar.adjv(1)
                self.other=False
            else:
                self.other=True
        
        #getting hit
        if self.iframes == False:
            hits=pygame.sprite.spritecollide(self, attacks, False)
            for i in hits:
                dam=i.hit()
                self.healthBar.adjv(-dam)
                
            crash = pygame.sprite.spritecollide(self, enimies, False)
            for i in crash:
                temp=i.crash()
                if temp == "sea":
                    pass
                else:
                    self.healthBar.adjv(-20)
            if self.healthBar.currentV<0:
                return self.death()
        #fireing
        end = ["fire"]
        if self.firing and self.fire():
            s=projectile.playershot(self.rect.center[0],self.rect.center[1],-C.math.pi/2)
            end.append(s)
        if self.turretfire and self.fire():
            if self.turretheading[0] !=0 and self.turretheading[1] !=0 :
                s=projectile.turretshot(self.rect.center[0],self.rect.center[1],[self.turretheading[0]*(2**.5)/2,self.turretheading[1]*(2**.5)/2])
            else:
                s=projectile.turretshot(self.rect.center[0],self.rect.center[1],self.turretheading)
            end.append(s)
            self.turretfire=False
        if len(end)>1:
            return end



        
