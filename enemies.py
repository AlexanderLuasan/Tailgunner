import pygame
import constants as C
import projectile

 


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


class Real_looper(pygame.sprite.Sprite):
    def gs(self,x,y,dx,dy):
        gsimage = pygame.Surface([dx, dy])
        gsimage.fill((234,154,45))
        gsimage.set_colorkey((234,154,45))
        gsimage.blit(self.spritesheet,(0,0),(x,y,dx,dy))
        return gsimage
    
    def crash(self):
        self.kill()
    
    def __init__(self,x,y):
        super().__init__()
        self.has_looped = False
        self.health = 10
        self.spritesheet = pygame.image.load("greenplane"+".png")
        self.animation = [self.gs(18,0,64,72),self.gs(114,0,64,72),self.gs(210,0,64,72),self.gs(298,0,64,72)]
        self.image = self.animation[0]   
        self.heading = [0,.5]
        self.acceleration_vector = [0,0]
        self.rect = self.image.get_rect()
        self.rect.x = x + self.rect.width/2
        self.rect.y= y + self.rect.height/2
        self.tim = 0
    
    def evasive_manuvers(self):
        """semi-randomly adjusts the acceleration vector, in such a way that will typically keep the plane onscreen"""
        
        
        temp = (C.screenSize[0]/2- self.rect.x) #negative when x is to the right of the center, positive if to the left
        temp2 = C.random.randint(0,C.screenSize[0]) - C.screenSize[0]/2 # random num between -1/2 screen size, and positive 1/2 screensize
        temp3 = temp2+ .1*temp

        
        if temp3 > 0:
            self.acceleration_vector[0] += .01
        else:
            self.acceleration_vector[0] -= .01
        
        if self.acceleration_vector[0] > .1:
            self.acceleration_vector[0] = .1
        elif self.acceleration_vector[0] < -.1:
            self.acceleration_vector[0] = -.1
            
            
        

    
    def update_image(self):
        """will update the image as apropriate to the current heading"""
        image_dict = {} # should be a dict in the form x heading, appropriate animation index basic idea is that it will find the the key with the least difference from the current x heading, and make that value self.image. Will complete when i get the sprite
        
    def loop_de_loop(self):
        """should change self.acceleration to be perpendicular self.heading, causing it to do a loop additionally, should transform all of the animation rotate all the animation things bit by bit"""
        self.acceleration_vector = C.angleToVector(C.vectorToAngle(self.heading) - C.math.pi/2, .01)
        
        if self.heading[1] < -.5:
            self.image = pygame.transform.flip(self.image, True, True)
            self.has_looped = True
            print("switch")
        
        #self.image = pygame.transform.rotate(self.image, C.math.pi)

    
    def update(self,playerlist,attacklist):
        """moves the player, checks if they've been hit, checks if they've died"""
        
        self.rect.x+=self.heading[0]
        self.rect.y+=self.heading[1]
        self.heading[0] += self.acceleration_vector[0] 
        self.heading[1] += self.acceleration_vector[1]
        
        if self.heading[0] > 2:
            self.heading[0] = 2
        elif self.heading[0] < -2:
            self.heading[0] = -2
            

        hits=pygame.sprite.spritecollide(self, attacklist, False)
        for i in hits:
            temp=i.hit()
            self.health-=temp
        if self.health<=0:
            self.kill()
        if abs(self.rect.x-C.screenSize[0]/2)>1000 or abs(self.rect.y-C.screenSize[1]/2)>1000:
            self.kill()
        

        self.evasive_manuvers()

        if self.rect.y > C.screenSize[1]-300 and not self.has_looped:
            self.loop_de_loop()


 
class strafer(pygame.sprite.Sprite):
    def gs(self,x,y,dx,dy):
        gsimage = pygame.Surface([dx, dy])
        gsimage.fill((234,154,45))
        gsimage.set_colorkey((234,154,45))
        gsimage.blit(self.spritesheet,(0,0),(x,y,dx,dy))
        return gsimage
    def crash(self):
        self.kill()     
    def __init__(self,x,y,direction,wing=5,side = "both"):
        super().__init__() #24,24
        self.spritesheet =pygame.transform.flip(pygame.image.load(C.getImage("zeroTurn")+".png"),False,True)
        self.angles = [0,C.math.pi/4,C.math.pi/2,3*C.math.pi/4,C.math.pi]
        self.anglePos = 2
        self.animation = [self.gs(1,1,24,24),self.gs(28,1,24,24),self.gs(53,1,24,24),self.gs(79,1,24,24),self.gs(105,0,24,24)]#pygame.transform.scale2x()
        for i in range(len(self.animation)):
            self.animation[i]=pygame.transform.scale2x(self.animation[i])
        self.image=self.animation[self.anglePos]
        #self.image=self.spritesheet
        self.rect=self.image.get_rect()
        if isinstance(x,list):
            x=C.random.randint(x[0],x[1]+1)
        if isinstance(y,list):
            y=C.random.randint(y[0],y[1]+1)
        self.rect.x = x - self.rect.width/2
        self.rect.y = y - self.rect.height
        self.heading = C.angleToVector(self.angles[self.anglePos],2)
        self.tim = -30
        self.health = 1
        self.first = True
        self.split = True
        self.fire = 0
        self.wings = wing-1
        self.side = side
    
    def update(self,playerlist,attacklist):
              
        if self.rect.y<100:
            self.rect.y+=1
            if self.first == True:
                self.first=False
                if self.wings>0:
                    if self.side=="r":
                        self.anglePos = 1#C.random.randint(0,1)
                        self.heading=C.angleToVector(self.angles[self.anglePos],2)
                        #self.image = self.animation[self.anglePos]                             
                        return ("ep",strafer(self.rect.x+self.rect.width*1.5,self.rect.top-self.rect.height/4,C.math.pi/2,wing=self.wings/2,side="r"))
                    elif self.side=="l":
                        self.anglePos = 3#C.random.randint(3,4)
                        self.heading=C.angleToVector(self.angles[self.anglePos],2)
                        #self.image = self.animation[self.anglePos]                             
                        return ("ep",strafer(self.rect.x-self.rect.width/2,self.rect.top-self.rect.height/4,C.math.pi/2,wing=self.wings/2,side="l"))
                    elif self.side=="both":
                        self.anglePos = 2#C.random.randint(0,4)
                        self.heading=C.angleToVector(self.angles[self.anglePos],2)
                        #self.image = self.animation[self.anglePos]                             
                        return ("ep",strafer(self.rect.x+self.rect.width*1.5,self.rect.top-self.rect.height/4,C.math.pi/2,wing=self.wings/2,side="r"),strafer(self.rect.x-self.rect.width/2,self.rect.top-self.rect.height/4,C.math.pi/2,wing=self.wings/2,side="l"))
                else:
                    if self.side=="r":
                        self.anglePos = 0
                        self.heading=C.angleToVector(self.angles[self.anglePos],2)                    
                    elif self.side=="l":
                        self.anglePos = 4
                        self.heading=C.angleToVector(self.angles[self.anglePos],2)                    
                    elif self.side=="both":
                        self.anglePos = C.random.randint(0,4)
                        self.heading=C.angleToVector(self.angles[self.anglePos],2)                     
            return None
        self.rect.x+=self.heading[0]
        self.rect.y+=self.heading[1]          
        target = closest(self,playerlist)
        if target==None:
            return None
        self.tim+=1
        if self.tim >C.PlayerFPS/C.enemiesFPS*30: 
            if target.rect.x<self.rect.x:
                self.anglePos+=1
                if self.anglePos>=len(self.animation):
                    self.anglePos-=1
            elif target.rect.x>self.rect.x:
                self.anglePos-=1
                if self.anglePos<0:
                    self.anglePos=0
            self.heading=C.angleToVector(self.angles[self.anglePos],2)
            self.image = self.animation[self.anglePos]                 
            self.tim = 0
        self.fire +=1
        if abs((self.rect.x+self.rect.width/2)-(target.rect.x+target.rect.width/2))<5 and self.fire>C.PlayerFPS/C.enemiesFPS*30:
            self.fire = 0
            return("ea",projectile.zeroShot(self.rect.center[0],self.rect.bottom,C.math.pi/2))
        hits=pygame.sprite.spritecollide(self, attacklist, False)
        for i in hits:
            temp=i.hit()
            self.health-=temp
        if self.health<=0:
            self.kill()
        if abs(self.rect.x-C.screenSize[0]/2)>1000 or abs(self.rect.y-C.screenSize[1]/2)>1000:
            self.kill()  
        if self.tim <-10:
            self.image = self.animation[self.anglePos]
#flies in a circle

#flies in given direction untill on screen
#summons next of kin
#stright
#circle
#seting variables
SPIN_SPEED = 5
SPIN_HEALTH = 1
SPIN_DIVISIONS = 32
SPIN_DELAY = -20
SPIN_BUFFER = 20
SPIN_COUNT = 3

class SpinPlane(pygame.sprite.Sprite):
    def __init__(self,x,y,direction=1,wing=5,side = "both"):
        super().__init__()#50,38
        #make animation and angle -pi/2 is up 
        #set original position off screen circle to the right with tails
        self.spritesheet = pygame.image.load(C.getImage("rotatorplane")+".png")
        origImage = [self.gs(0,38*2,50,38),self.gs(50,38*2,50,38)]
        #-90 -> 270 possible angles 8 possible angles
        self.animationAngles = []
        self.animations = []
        divisions=SPIN_DIVISIONS
        units = 2*C.math.pi/SPIN_DIVISIONS
        for i in range(0,divisions):
            self.animationAngles.append((-C.math.pi/2)+i*units)
            self.animations.append([pygame.transform.rotate(origImage[0],360 - (i*units*180/C.math.pi)),pygame.transform.rotate(origImage[1],360 - (i*units*180/C.math.pi))])
        self.propCount = 0  
        #an inital setting
        self.position = 0
        self.image = self.animations[self.position][0]
        self.rect = self.image.get_rect()
        self.rect.x=x-self.rect.width/2
        self.rect.y=y-self.rect.height/2
        self.heading = C.angleToVector(self.animationAngles[self.position],SPIN_SPEED)
        
        self.spinDirection = direction
        self.tim = 0 #miain counter
        self.mode = "stright" #stright or circle or oval
        
        self.health=SPIN_HEALTH
        
        
            
            
        if self.rect.right<0:
            self.setSpin(int(SPIN_DIVISIONS/4))
            self.rect.right = -SPIN_BUFFER
            self.direction = "right"
            self.spinDivision = int(C.screenSize[0]/(SPIN_COUNT+1))
        elif self.rect.left>C.screenSize[0]:
            self.setSpin(3*int(SPIN_DIVISIONS/4))
            self.rect.left = C.screenSize[0] 
            self.direction = "left"
            self.spinDivision = (SPIN_COUNT)*int(C.screenSize[0]/(SPIN_COUNT+1))
        self.rect = self.image.get_rect()
        self.rect.x=x-self.rect.width/2
        self.rect.y=y-self.rect.height/2
        
        self.delayCount = SPIN_DELAY
        if wing>0:
            self.delayCount*=-1
            if side=="both":
                self.kin = SpinPlane(self.rect.x+self.rect.width/2,self.rect.y+self.rect.height/2,direction*-1,wing-1,"both")
            else:
                self.kin = SpinPlane(self.rect.x+self.rect.width/2,self.rect.y+self.rect.height/2,direction,wing-1,"left")
            
    def update(self,playerlist,attacklist):
        self.rect.x+=self.heading[0]
        self.rect.y+=self.heading[1]
        self.rect.y-=C.backgroundScroll
        
        self.tim +=1
        if self.propCount>1:
            self.image = self.animations[self.position][0]
            if self.propCount>4:
                self.image = self.animations[self.position][1]
                self.propCount=0
        #mode switch
        if self.mode == "circle":
            if self.tim%5 == 0:
                self.spin(self.spinDirection)
            if self.tim > (SPIN_DIVISIONS)*5:
                self.mode = "stright"
                self.tim = 0
        elif self.mode == "stright":
            if self.direction == "right":
                if self.rect.x+self.rect.width > self.spinDivision:
                    self.spinDivision+=int(C.screenSize[0]/(SPIN_COUNT+1))
                    if self.spinDivision<C.screenSize[0]+SPIN_BUFFER:   
                        self.mode = "circle"
                    self.tim = 0
            if self.direction == "left":
                if self.rect.x+self.rect.width < self.spinDivision:
                    self.spinDivision-=int(C.screenSize[0]/(SPIN_COUNT+1))
                    if self.spinDivision>0-SPIN_BUFFER:
                        self.mode = "circle"
                    self.tim = 0
                
        elif self.mode == "oval":#unused
            if self.heading[0]<=0 and self.direction == "left":
                if self.tim%10 == 0:
                    self.spin(self.spinDirection)
            elif self.heading[0]>=0 and self.direction == "right":
                if self.tim%10 == 0:
                    self.spin(self.spinDirection)
            elif self.tim%5 == 0:
                self.spin(self.spinDirection)

            
        #hits
        hits=pygame.sprite.spritecollide(self, attacklist, False)
        for i in hits:
            temp=i.hit()
            self.health-=temp
        if self.health<=0:
            self.kill()
        if abs(self.rect.x-C.screenSize[0]/2)>1000 or abs(self.rect.y-C.screenSize[1]/2)>1000:
            self.kill()
        if self.delayCount>0:
            self.delayCount-=1
            if self.delayCount<1:
                return ("ep",self.kin)
    def gs(self,x,y,dx,dy):
        gsimage = pygame.Surface([dx, dy])
        gsimage.fill((234,154,45))
        gsimage.set_colorkey((234,154,45))
        gsimage.blit(self.spritesheet,(0,0),(x,y,dx,dy))
        return gsimage
    def crash(self):
        self.kill()
    def setSpin(self,position):
        self.position=position
        self.spin(0)
    def spin(self,direction):
        #adjust position
        self.position = (self.position+direction)
        if self.position>len(self.animations)-1:
            self.position=0
        elif self.position<0:
            self.position=len(self.animations)-1
        #remember center
        currentcenter = (self.rect.x+self.rect.width,self.rect.y+self.rect.height)
        self.image = self.animations[self.position][0]#changeimage
        self.rect = self.image.get_rect()#new rect and center
        self.rect.x= currentcenter[0]-self.rect.width
        self.rect.y=currentcenter[1]-self.rect.height
        self.heading = C.angleToVector(self.animationAngles[self.position],SPIN_SPEED)
        #round heading to int
        if self.heading[0]>0:
            self.heading[0] = int(self.heading[0]+.5)
        elif self.heading[0]<0:
            self.heading[0] = int(self.heading[0]-.5)
        if self.heading[1]>0:
            self.heading[1] = int(self.heading[1]+.5)
        elif self.heading[1]<0:
            self.heading[1] = int(self.heading[1]-.5)
        
    
        
