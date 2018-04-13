import pygame
import constants
import projectile

#draws health bar

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
            self.rect. x = constants.screenSize[0] - self.x - 10
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
        self.size = size       
        self.spritesheet = pygame.image.load(constants.getImage(spritesheet)+".png")
        self.animation = []
        self.animation.append([''])
        for i in range(12):
            tower = []
            for j in range(14):
                tower.append(self.gs(i*68,j*68,68,68))
            self.animation.append(tower)
        for i in range(12):
            tower = []
            for j in range(14):
                tower.append(pygame.transform.flip(self.animation[12-i][j],True,False))
            self.animation.append(tower)
        self.toproll = [self.animation[-1][8],self.animation[-1][9],self.animation[-1][10],self.animation[-1][11],self.animation[-1][12],self.animation[-1][13],self.animation[1][13],self.animation[1][12],self.animation[1][11],self.animation[1][10],self.animation[1][9],self.animation[1][8]]
        self.toprollspeed = [8,8,4,4,0,0,0,0,-4,-4,-8,-8]
        self.image = self.animation[1][0]
        self.rect=self.image.get_rect()
        self.rect.x=x+self.rect.width/2
        self.rect.y=y+self.rect.height/2
        self.heading = [0,0]
        self.headingPrime = [0,0]
        self.planeSpeed = 8
        self.accStep = 1
        self.turetAngle = 0
        
        
        #turret
        self.turretheading = [0,0]
        self.turretPos = [1,1]
        self.turretPosDict = {(0,-1):(1,1),(-1,-1):(2,11),(-1,0):(4,9),(-1,1):(5,8),(0,1):(6,6),(1,1):(8,5),(1,0):(9,4),(1,-1):(11,2)}
        self.turrefireangle = [-1,-1]
        self.turretfire = False
        #stat bars
        self.healthBar = hudBar(20,constants.screenSize[1]-100,"right",100,100,(255,0,0))
        self.gunBar = hudBar(40,constants.screenSize[1]-100,"right",100,100,(255,255,0))
        self.firecount=0
        self.firing=False
        self.airBar = hudBar(60,constants.screenSize[1]-100,"right",100,100,(255,0,255))
        self.allbar = [self.airBar,self.gunBar,self.healthBar]
        self.other = True
        #dieng
        self.deathdelay = 0
        self.dead = False
        self.respawn= False
        self.repsawnTime = 0
        self.iframes=False
        #rolling
        self.roll = 0
        self.rolling = False
        self.rollingDir = 0
        self.roolCount = 0
        self.tim = 0
        
    def getHud(self):
        return (self.healthBar,self.gunBar,self.airBar)
    def fireToggle(self,state):
        self.firing=state
    def setTurretHeading(self,direction):
        self.turretheading = (direction[0],direction[1])
        if self.turretheading!=(0,0):
            self.turretPos = self.turretPosDict[self.turretheading]
    def fireTurret(self):
        self.turretfire = True
    def adjTurretHeading(self,direction):
        
        
        self.turretheading=(direction[0],direction[1])
        
        if self.turretheading!=(0,0):
            self.turretPos = self.turretPosDict[self.turretheading]        
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
    def rollOver(self):
        self.tim +=1
        if self.tim>4:
            self.tim=0
            if self.rollDir<0:
                self.image=self.toproll[self.rollcount]
                self.heading[0] = self.toprollspeed[self.rollcount]
                self.rollcount+=self.rollDir
                if self.rollcount<0:
                    self.heading[0]=1.5*self.planeSpeed
                    self.rolling=False
                    
            elif self.rollDir>0:
                self.image=self.toproll[self.rollcount]
                self.heading[0] = self.toprollspeed[self.rollcount]
                self.rollcount+=self.rollDir
                if self.rollcount>=len(self.toproll):
                    self.heading[0]=-1.5*self.planeSpeed
                    self.rolling=False
    def adjustHeading(self,direction):
        self.headingPrime[0] +=direction[0]
        self.headingPrime[1] +=direction[1]
    def setHeading(self,direction):
        self.heading = direction
    def adjustRoll(self,direction):
        self.roll+=direction
    def setRoll(self,direction):
        print("selfRoll",direction)
        self.roll = direction
        if self.heading[0]<=-1.5*self.planeSpeed and self.roll<0:
            if self.rolling !=True:
                self.rollcount=len(self.toproll)-1            
            if self.airBar.getV()>60:
                self.rolling=True
            self.rollDir=self.roll
            
        elif self.heading[0]>=1.5*self.planeSpeed and self.roll>0:
            if self.rolling !=True:
                self.rollcount=0
            if self.airBar.getV()>60:
                self.rolling=True
            self.rollDir=self.roll
    def recuceRoll(self):
        if self.roll>0:
            self.roll=0
        elif self.roll<0:
            self.roll=0
    def update(self,enimies,attacks):
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
        
        #animation
        if self.rolling == True:
            if self.airBar.getV()>1:
                self.airBar.adjv(-1)
                self.rollOver()
            else:
                self.rolling=False
        else:
            self.airBar.adjv(1)
            tilt = 2*abs(int(self.heading[0]/4))
            self.tim+=1    
            if self.tim%4 > 1:
                tilt+=1
            if self.heading[0]>0:
                if len(self.animation[-1])>tilt:
                    if tilt>3 and self.turretPos[1] == 11:
                        self.image = self.animation[-2][tilt]
                    else:
                        self.image = self.animation[-1*self.turretPos[1]][tilt]
            elif self.heading[0]<0:
                if len(self.animation[1])>tilt:
                    if tilt>3 and self.turretPos[0] == 11:
                        self.image = self.animation[2][tilt] 
                    else:
                        self.image = self.animation[1*self.turretPos[0]][tilt]
                  
            else:
                self.image = self.animation[1*self.turretPos[0]][tilt%2]
        
        
        #speed
        if abs(self.heading[0])==abs(self.heading[1]) and self.heading[1]!=0:
            self.rect.x += self.heading[0]/2*2**.5/2
            self.rect.y += self.heading[1]/2*2**.5/2
        else:
            self.rect.x += self.heading[0]/2
            self.rect.y += self.heading[1]/2

        
        if self.rect.x<0:
            self.rect.x=0
        elif self.rect.x>constants.screenSize[0]-self.rect.width:
            self.rect.x=constants.screenSize[0]-self.rect.width
        if self.rect.y<0:
            self.rect.y=0
        elif self.rect.y>constants.screenSize[1]-self.rect.height:
            self.rect.y=constants.screenSize[1]-self.rect.height
        
        if self.firecount>0:
            self.firecount-=1
        if self.firing==False and self.gunBar.getV()<self.gunBar.getM():
            if self.other == True:
                self.gunBar.adjv(1)
                self.other=False
            else:
                self.other=True
        
        #getting hit
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
            s=projectile.playershot(self.rect.center[0],self.rect.center[1],-constants.math.pi/2)
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



        
