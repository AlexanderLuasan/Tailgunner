import pygame
import constants as C
import projectile
P_MAXHEALTH=3
maskingtester = pygame.sprite.GroupSingle()
COOP = False
#draws health bar
ROTATIONANGLE = .1
ERRORANGLE=.01
#FPS/Playerframes converst calls to 1/60 sonds
frameMul=C.FPS/C.PlayerFPS 
class counter(pygame.sprite.Sprite):
    def __init__(self,side):
        super().__init__()
        self.side =side
        self.v = 0
        self.place()
    def place(self):
        basicfont = pygame.font.SysFont(None, 48)
        self.image = basicfont.render(str(self.v), True, (255, 0, 0), (255, 255, 255))
        self.rect = self.image.get_rect()
        if self.side =="right":
            self.rect.x=0
        else:
            self.rect.x=C.screenSize[0]-self.rect.width
        self.rect.y=100-self.rect.height

    def setv(num):
        self.v=num
        self.place()
    def adjv(num):
        self.v+=num
        self.place()
        
class hudBar(pygame.sprite.Sprite):
    def __init__(self,x,y,side,maxV,currentV,color,hidden=False):
        super().__init__()
        self.maxV = maxV
        self.currentV = currentV
        self.side = side
        self.x=x
        self.y=y  
        self.color = color
        self.placebar()
        self.hidden = hidden
        
        #place bar
        
    def placebar(self):
        self.image = pygame.Surface([10,self.maxV])
        self.image.fill((255,255,255))
        self.rect = self.image.get_rect()
        pygame.draw.rect(self.image,self.color,(0,self.rect.height-self.currentV,10,self.rect.height,))
        self.rect = self.image.get_rect()
        if self.side=="left":
            self.rect.x = C.screenSize[0] - self.x - 10
        else:
            self.rect.x = self.x
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
    
    def __init__(self,x,y,spritesheet,side,name):
        super().__init__() #(68,68) spaceing(0,0), (0,0)
        
        self.name=name
        self.side = side
        self.spritesheetname = spritesheet
        self.tempangle = -C.math.pi/2
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
        self.turretFireCount = 0
        
        
        #stat bars
        self.healthBar = hudBar(20,C.screenSize[1]-100,self.side,P_MAXHEALTH,P_MAXHEALTH,(255,0,0))
        self.gunBar = hudBar(40,C.screenSize[1]-100,self.side,100,0,(255,255,0))
        self.ammmoDisplay = counter(self.side)
        self.airBar = hudBar(60,C.screenSize[1]-100,self.side,100,100,(255,0,255))
        self.allbar = [self.airBar,self.gunBar,self.healthBar]
        #coop bars
        if self.side=="right":
            self.ammo1 = hudBar(60,C.screenSize[1]-100,"left",100,100,(255,255,0),hidden=True)#left
        else:
            self.ammo1 = hudBar(60,C.screenSize[1]-100,"right",100,100,(255,255,0),hidden=True)#left
        self.allbar.append(self.ammo1)
            
        
        
        
        #extra frame conter
        self.other = True
        #firing variables
        self.mainFireCount=0
        self.firing=False        
        #dieing
        self.deathdelay = 0
        self.dead = False
        self.respawn= False
        self.repsawnTime = 0
        self.iframesCount = 0
        
        
        #power ups
        self.CurrentFireMethod = "basic" #basic shotgun split rotate toAdd laser semiauto fullauto  
        self.turretFireMode = "basicS"
        self.mainBulletCount = 0
        self.turretBulletCount = 0
        self.powerupCount = 1
        self.powerupangle = 0
        self.revive = False
        #for rotation
        self.powerupdirection = 1
        #for shield
        self.sheild=False
      
        
    def update(self,enimies,attacks):
        if self.healthBar.currentV<=0:#die
            return self.death()
        self.acceeration()
        self.animate()
        self.speed()
        self.border()#prevent moving off edge
        self.colisionDetection(enimies,attacks)
  
        if self.mainFireCount>0:
            self.mainFireCount-=1
        if self.turretFireCount>0:
            self.turretFireCount-=1
        if self.revive == True:
            self.revive=False
            return ("revive","")
        
        shots = ["fire"]
        add=self.turretFire()
        for i in add:
            shots.append(i)
        
        add=self.mainFire()
        for i in add:
            shots.append(i)        
        if len(shots)>1:
            return shots
        
    def turretFire(self):
        end = []
        if self.turretfire and self.ammo1.getV()>0 and self.turretFireCount<1:

            if self.turretheading[0]!=0:
                shots=self.makeSpecialShots(self.turretFireMode,C.vectorToAngle([self.turretheading[0],self.turretheading[1]*-1]))
            else:
                if self.turretheading[1]>0:
                    shots=self.makeSpecialShots(self.turretFireMode,-C.math.pi/2)
                else:
                    shots=self.makeSpecialShots(self.turretFireMode,C.vectorToAngle([self.turretheading[0],self.turretheading[1]*-1]))
            try:
                for s in shots:
                    end.append(s)
            except:
                end.append(shots)
            self.turretfire=False
            #calulate ammo
            self.ammo1.adjv(-1)
            if self.turretFireMode == "Tsemi" and self.turretBulletCount<5:
                self.turretfire=True
                self.turretBulletCount+=1
                self.turretFireCount=2
            elif self.turretFireMode == "Tfull":
                self.turretfire=True
                self.turretFireCount =2
            else:
                self.turretFireCount = 10
                self.turretBulletCount=0            
            
        elif self.turretfire and self.turretFireMode == "basicS" and self.turretFireCount<1:
            if self.turretheading[0]!=0:
                shots=self.makeSpecialShots("basicS",C.vectorToAngle([self.turretheading[0],self.turretheading[1]*-1]))
            else:
                if self.turretheading[1]>0:
                    shots=self.makeSpecialShots("basicS",-C.math.pi/2)
                else:
                    shots=self.makeSpecialShots("basicS",C.vectorToAngle([self.turretheading[0],self.turretheading[1]*-1]))
            self.turretfire=False
            end.append(shots)
        elif self.ammo1.getV()<1:
            self.turretFireMode = "basicS"
        return end
    def mainFire(self):
        end = []
        if self.firing and self.gunBar.getV()>0 and self.mainFireCount<1:
            shots=self.makeSpecialShots(self.CurrentFireMethod,-C.math.pi/2)
            self.firing=False
            try:
                for s in shots:
                    end.append(s)
            except:
                end.append(shots)
            if self.CurrentFireMethod=='full' or self.CurrentFireMethod=='laser' or self.CurrentFireMethod=='semi' or self.CurrentFireMethod=='snake':
                self.gunBar.adjv(-1)
            else:
                self.gunBar.adjv(-2)
           
            #delay after shot
            if (self.CurrentFireMethod == "semi" or self.CurrentFireMethod == "snake" ) and self.mainBulletCount<5:
                self.firing=True
                self.mainBulletCount+=1
                self.mainFireCount=2


            elif self.CurrentFireMethod == "full":
                self.firing=True
                self.mainFireCount =2

            elif self.CurrentFireMethod == "laser":
                self.firing=True
                self.mainFireCount =0

            elif self.CurrentFireMethod == "basic":
                self.firing=False
                self.mainFireCount =20              
            else:
                self.mainFireCount = 10
                self.mainBulletCount=0
        elif self.firing and self.CurrentFireMethod == "basic" and self.mainFireCount<1:
            shots = self.makeSpecialShots(self.CurrentFireMethod,-C.math.pi/2)
            end.append(shots)
            self.firing=False
            self.mainFireCount = 10
        elif self.gunBar.getV()<1 and self.CurrentFireMethod != "basic":
            self.CurrentFireMethod="basic"  
        return end
    def makeSpecialShots(self,method,mainangle):
        #produces shotting patterns
        if method == "basic" or method == "semi" or method == "full" or method == "laser":
            s=projectile.playershot(self.rect.center[0],self.rect.center[1],mainangle)
            return s
        if method == "basicS" or method == "Tsemi" or method == "Tfull":
            s=projectile.scaterShots(self.rect.center[0],self.rect.center[1],mainangle)
            return s
        if method == "snake":
            s=projectile.scaterShots(self.rect.center[0],self.rect.center[1],mainangle+self.powerupangle)
            self.powerupangle+= self.powerupdirection*ROTATIONANGLE
            if abs(self.powerupangle)>abs(self.powerupCount*ROTATIONANGLE):
                self.powerupdirection*=-1
                self.powerupangle+= self.powerupdirection*ROTATIONANGLE
            return s
        if method== "split":
            allshots = []
            for angle in range(self.powerupCount):
                s= projectile.scaterShots(self.rect.center[0],self.rect.center[1],mainangle+angle*ROTATIONANGLE)
                f= projectile.scaterShots(self.rect.center[0],self.rect.center[1],mainangle-angle*ROTATIONANGLE)
                allshots.append(s)
                allshots.append(f)
            return allshots
        if method == "shotgun":
            allshots = []
            for angle in range(self.powerupCount): 
                angle = C.random.randint(-self.powerupCount,self.powerupCount)
                s= projectile.scaterShots(self.rect.center[0],self.rect.center[1],mainangle+angle*ROTATIONANGLE)
                allshots.append(s)
            return allshots
    def powerup(self,poweruptype,ammo):
        self.CurrentFireMethod=poweruptype.lower()
        self.powerupCount+=1
    def getHud(self):
        #returns all huds
        return self.allbar
    def fireToggle(self,state):
        #fire on or off
        self.firing=state
    def setTurretHeading(self,direction):
        #aim turret
        self.turretheading = (direction[0],direction[1])
        if self.turretheading!=(0,0):
            self.turretPos = self.turretPosDict[self.turretheading]
    def fireTurret(self,state):
        #fire an angled single 
        self.turretfire = state
 
    
    
    def death(self):
        #call and it will handle the explosion
        self.deathdelay-=1
        self.iframesCount=5
        if self.dead == False:
            self.dead = True
            self.image.set_alpha(0)
            return("explosion","none")
            #image invisable
        if self.deathdelay<-5:
            self.deathdelay = 10
            self.respawn= True
            self.iframesCount=5
            for i in self.allbar:
                i.kill()
            return("respawn",(self.rect.center),self.name,self.side,self.spritesheetname)
    def setRoll(self,direction):
        #to enter a roll and set tillt
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
            self.iframesCount=10
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
                            self.iframes=0
                    elif self.rollDir>0:
                        self.image=self.toproll[self.rollcount][front][prop]
                        self.heading[0] = self.toprollspeed[self.rollcount]
                        self.rollcount+=self.rollDir
                        if self.rollcount>=len(self.toproll):
                            self.heading[0]=-1.5*self.planeSpeed
                            self.rolling=False
                            self.iframes=0                
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
    def acceeration(self):
        #adjust the headingprimes arcoding to keys
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
    def speed(self):
        if abs(self.heading[0])==abs(self.heading[1]) and self.heading[1]!=0:
            self.rect.x += self.heading[0]/2*2**.5/2
            self.rect.y += self.heading[1]/2*2**.5/2
        else:
            self.rect.x += self.heading[0]/2
            self.rect.y += self.heading[1]/2        
    def border(self):
        if self.rect.x<0:
            self.rect.x=0
        elif self.rect.x>C.screenSize[0]-self.rect.width:
            self.rect.x=C.screenSize[0]-self.rect.width
        if self.rect.y<0:
            self.rect.y=0
        elif self.rect.y>C.screenSize[1]-self.rect.height:
            self.rect.y=C.screenSize[1]-self.rect.height 
    def colisionDetection(self,enimies,attacks):
        if self.iframesCount>0:
            self.iframesCount -=1
        if self.iframesCount==0:
            hits=pygame.sprite.spritecollide(self, attacks, False)
            for i in hits:
                #do smarter
                if True:
                    if self.sheild == False:
                        dam=i.hit()
                        self.healthBar.adjv(-dam)
                        self.iframesCount=120
                        break
                    else:
                        self.sheild=False
                        self.iframesCount=120
                        break
            
            crash = pygame.sprite.spritecollide(self, enimies, False)
            for i in crash:
                if pygame.sprite.collide_mask(self,i)!=None:
                    temp=i.crash()
                    if temp == "powerup":
                        self.PowerUpHandLer(i)
                    elif temp == "nocolide":
                        pass
                    elif self.sheild == False:
                        if temp == "sea":
                            pass
                        else:
                            self.healthBar.adjv(-1)
                            self.iframesCount=120
                            break                    
                    else:
                        self.sheild=False
                        self.iframesCount=120
                        break
    '''
      basic shotgun split rotation toAdd laser semiauto fullauto  
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
    def PowerUpHandLer(self,ObjPowerup):
        powerUpType = ObjPowerup.powerUp
        ObjPowerup.kill()
        self.healthBar.adjv(1)

        if powerUpType=="sheild":
            self.sheild = True
        elif powerUpType=="life":
            self.revive = True
        if self.CurrentFireMethod == "basic":
            if powerUpType=="split":
                self.powerupCount=2
                self.gunBar.adjv(200)
                if self.CurrentFireMethod=="split":
                    self.powerupCount+=1
                self.CurrentFireMethod = "split"
            elif powerUpType=="snake":
                self.powerupCount=4
                self.gunBar.adjv(200)
                if self.CurrentFireMethod=="snake":
                    self.powerupCount+=1            
                self.CurrentFireMethod = "snake"
            elif powerUpType=="prox":
                self.gunBar.adjv(200)
                self.powerupCount=3
                if self.CurrentFireMethod=="shotgun":
                    self.powerupCount+=1
                self.CurrentFireMethod = "shotgun"
            elif powerUpType=="auto":
                self.gunBar.adjv(200)
                self.CurrentFireMethod = "full"
            elif powerUpType=="semi":
                self.gunBar.adjv(200)
                self.CurrentFireMethod = "semi"
            elif powerUpType=="laser":
                self.gunBar.adjv(200)
                self.CurrentFireMethod = "laser"
        else:
            if powerUpType=="split":
                self.ammo1.adjv(200)
                if self.turretFireMode=="split":
                    self.powerupCount+=1
                self.turretFireMode = "split"
            elif powerUpType=="snake":
                self.ammo1.adjv(200)
                if self.turretFireMode=="snake":
                    self.powerupCount+=1            
                self.turretFireMode = "snake"
            elif powerUpType=="prox":
                self.ammo1.adjv(200)
                if self.turretFireMode=="shotgun":
                    self.powerupCount+=1
                self.turretFireMode = "shotgun"
            elif powerUpType=="auto":
                self.ammo1.adjv(200)
                self.turretFireMode = "full"
            elif powerUpType=="semi":
                self.ammo1.adjv(200)
                self.turretFireMode = "semi"
            elif powerUpType=="laser":
                self.ammo1.adjv(200)
                self.turretFireMode = "laser"            
        
    def COOP(self,state):
        if state:
            self.ammo1.hidden = False
        elif not state:
            self.ammo1.hidden = True



        
