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

class Test_plane(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.has_looped = False
        self.health = 10
        self.spritesheet = pygame.image.load("greenplane"+".png")
        self.animation = [self.gs(18,0,64,72),self.gs(114,0,64,72),self.gs(210,0,64,72),self.gs(298,0,64,72)]
        self.image = self.animation[0]
        self.heading = [0,0]
        self.acceleration_vector = [0,0]
        self.rect = self.image.get_rect()
        self.rect.x = x + self.rect.width/2
        self.rect.y= y + self.rect.height/2


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
        temp3 = temp2+ .11*temp


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
        """makes y accel negative until a certain y velocity is hit, then sets self.has_looped to true"""
        self.acceleration_vector[1] = - .025
        self.acceleration_vector[0] = -self.heading[0]/2

        print(self.heading[1])

        if self.heading[1] < -3.25:
            self.image = pygame.transform.flip(self.image, True, True)
            self.heading[1] = -3.25
            self.has_looped = True
            self.acceleration_vector[1] = 0
            print("switch")

    def real_loop_de_loop():
        """should change self.acceleration to be perpendicular self.heading, causing it to do a loop additionally, should transform all of the animation rotate all the animation things bit by bit"""
        #self.acceleration_vector = C.angleToVector(C.vectorToAngle(self.heading) - C.math.pi/2, .01)
        #self.image = pygame.transform.rotate(self.image, C.math.pi)
        pass


    def update(self,playerlist,attacklist):
        """moves the player, checks if they've been hit, checks if they've died"""

        self.rect.x+= self.heading[0]
        #print(self.heading[1]) #del later
        #print(self.rect.y) #del
        self.rect.y+= self.heading[1]
        #print(self.rect.y) #del
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



        if self.rect.y > C.screenSize[1]-300 and not self.has_looped:
            self.loop_de_loop()
        else:
            self.evasive_manuvers()

        #print(self.heading[1])
        #print(self.rect.y)
        #print("___")



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



class looper2(pygame.sprite.Sprite):
    def gs(self,x,y,dx,dy):
        gsimage = pygame.Surface([dx, dy])
        gsimage.fill((234,154,45))
        gsimage.set_colorkey((234,154,45))
        gsimage.blit(self.spritesheet,(0,0),(x,y,dx,dy))
        return gsimage
    def __init__(self,x,y,direction):
        super().__init__() #64,72
        self.spritesheet = pygame.image.load("greenplane"+".png")
        self.animation = [self.gs(18,0,64,72),self.gs(114,0,64,72),self.gs(210,0,64,72),self.gs(298,0,64,72)]
        self.image=self.animation[0]
        self.rect = self.image.get_rect()
        self.rect.x = x + self.rect.width/2
        self.rect.y= y + self.rect.height/2
        self.frame = 0
        self.looping = False
        self.tim = 0
        self.heading = C.angleToVector(direction,3)
        self.health=1
    def loop(self):
        if self.frame>=len(self.animation):
            return None
        self.image=self.animation[self.frame]
        self.frame+=1
        if self.frame == 2:
            self.holdh = self.heading[1]
            self.heading[1]= 0
        elif self.frame == 3:
            self.heading[1] = -self.holdh
    def crash(self):
        self.health-=1

    def update(self,playerlist,attacklist):
        self.rect.x+=self.heading[0]
        self.rect.y+=self.heading[1]

        self.tim+=1
        if self.rect.y>500:
            self.looping = True
        if self.looping == True and self.tim>20:
            self.loop()
            self.tim=0



        hits=pygame.sprite.spritecollide(self, attacklist, False)
        for i in hits:
            temp=i.hit()
            self.health-=temp
        if self.health<=0:
            self.kill()
        if abs(self.rect.x-C.screenSize[0]/2)>1000 or abs(self.rect.y-C.screenSize[1]/2)>1000:
            self.kill()





class basicPlane(pygame.sprite.Sprite):
    def gs(self,x,y,dx,dy):
        gsimage = pygame.Surface([dx, dy])
        gsimage.blit(self.spritesheet,(0,0),(x,y,dx,dy))
        return gsimage

    def __init__(self,x,y,direction):
        super().__init__()
        self.spritesheet = pygame.image.load("greenplane"+".png")
        self.image=self.gs(0,0,56,72)
        self.rect=self.image.get_rect()
        self.rect.x=x+self.rect.width/2
        self.rect.y=y+self.rect.height/2
        self.heading=C.angleToVector(direction,2)
        self.health=2
        self.tim = 0
    def crash(self):
        self.health-=1
    def update(self,playerlist,attacklist):
        self.rect.x+=self.heading[0]
        self.rect.y+=self.heading[1]
        hits=pygame.sprite.spritecollide(self, attacklist, False)
        for i in hits:
            temp=i.hit()
            self.health-=temp
        if self.health<0:
            self.kill()
        if abs(self.rect.x-C.screenSize[0]/2)>1000 or abs(self.rect.y-C.screenSize[1]/2)>1000:
            self.kill()

        self.tim+=1
        if self.tim>100:
            self.tim=0
            target = closest(self,playerlist)
            vector=[target.rect.center[0]-self.rect.center[0],target.rect.center[1]-self.rect.bottom]
            angle=C.vectorToAngle(vector)
            return("ea",projectile.shot(self.rect.center[0],self.rect.bottom,angle))
        return None

class turret(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.origImage=pygame.Surface([7,7])
        pygame.draw.rect(self.origImage,(255,255,255),(1,1,5,5))
        pygame.draw.rect(self.origImage,(255,255,255),(2,0,3,3))
        self.health=2
        angle=0
        self.image=pygame.transform.rotate(self.origImage,angle)
        self.rect=self.image.get_rect()
        self.tim=0
    def crash(self):
        self.health-=1
    def update(self,playerlist,attacklist):

        self.tim+=1
        if self.tim==120:
            target = closest(self,playerlist)
            vector=[target.rect.center[0]-self.rect.center[0],target.rect.center[1]-self.rect.bottom]
            angle=C.vectorToAngle(vector)
            self.image=pygame.transform.rotate(self.origImage,angle)
            self.tim=0
            return("ea",projectile.shot(self.rect.center[0],self.rect.bottom,angle))


        hits=pygame.sprite.spritecollide(self, attacklist, False)
        for i in hits:
            temp=i.hit()
            self.health-=temp
        if self.health<=0:
            self.kill()



class big(pygame.sprite.Sprite):
    def gs(self,x,y,dx,dy):
        gsimage = pygame.Surface([dx, dy])
        gsimage.blit(self.spritesheet,(0,0),(x,y,dx,dy))
        return gsimage
    def crash(self):
        self.health-=1
    def __init__(self,x,y,direction):
        super().__init__()
        self.spritesheet = pygame.image.load("largplane"+".png")
        self.image=self.gs(0,0,97,96)
        self.rect=self.image.get_rect()
        self.rect.x=x+self.rect.width/2
        self.rect.y=y+self.rect.height/2
        self.heading=C.angleToVector(direction,2)
        self.health=10
        self.amp = 5
        self.lr=.5
        self.turret = turret(0,0)
        self.turret1 = turret(0,0)
        self.tim=0
    def update(self,playerlist,attacklist):
        self.rect.x+=self.heading[0]
        self.rect.y+=self.heading[1]/2

        if abs(self.heading[0])>self.amp:
            self.lr=-self.lr
        self.heading[0]+=self.lr/4*abs(self.lr)
        self.turret.rect.center=self.rect.center
        self.turret1.rect.center=[self.rect.center[0],self.rect.center[1]-40]
        hits=pygame.sprite.spritecollide(self, attacklist, False)
        for i in hits:
            temp=i.hit()
            self.health-=temp
        if self.health<0:
            self.turret.kill()
            self.turret1.kill()
            self.kill()
        if abs(self.rect.x-C.screenSize[0]/2)>1000 or abs(self.rect.y-C.screenSize[1]/2)>1000:
            self.turret.kill()
            self.turret1.kill()
            self.kill()
        if self.tim==0:
            self.tim=1
            return("ep",self.turret,self.turret1)
        return None
class strafe(pygame.sprite.Sprite):
    def gs(self,x,y,dx,dy):
        gsimage = pygame.Surface([dx, dy])
        gsimage.blit(self.spritesheet,(0,0),(x,y,dx,dy))
        return gsimage
    def crash(self):
        self.health-=1
    def __init__(self,x,y,direction):
        super().__init__()
        self.spritesheet = pygame.image.load("simple"+".png")
        self.image=self.gs(0,0,56,72)
        self.rect=self.image.get_rect()
        self.rect.x=x+self.rect.width/2
        self.rect.y=y+self.rect.height/2
        self.heading=C.angleToVector(direction,2)
        self.health=2
        self.tim = 0
    def update(self,playerlist,attacklist):
        self.rect.x+=self.heading[0]
        self.rect.y+=self.heading[1]
        hits=pygame.sprite.spritecollide(self, attacklist, False)
        for i in hits:
            temp=i.hit()
            self.health-=temp
        if self.health<=0:
            self.kill()
        if abs(self.rect.x-C.screenSize[0]/2)>1000 or abs(self.rect.y-C.screenSize[1]/2)>1000:
            self.kill()
        #adj course

        target = closest(self,playerlist)
        vector=[target.rect.center[0]-self.rect.center[0],target.rect.center[1]-self.rect.bottom]
        angleToTarget=C.vectorToAngle(vector)
        angleOfPlane = C.vectorToAngle(self.heading)
        if abs(angleToTarget-angleOfPlane)-30*C.math.pi/180<0:
            angleOfPlane=angleToTarget
        elif angleToTarget>angleOfPlane:
            angleOfPlane+=30*C.math.pi/180
        elif angleToTarget<angleOfPlane:
            angleOfPlane-=30*C.math.pi/180
        self.heading = C.angleToVector(angleOfPlane,3)

        self.tim+=1
        if self.tim>20:
            self.tim=0
            return("ea",projectile.shot(self.rect.center[0],self.rect.bottom,C.math.pi/2))


        return None
class boat(pygame.sprite.Sprite):
    def gs(self,x,y,dx,dy):
        gsimage = pygame.Surface([dx, dy])
        gsimage.fill((234,154,45))
        gsimage.set_colorkey((234,154,45))
        gsimage.blit(self.spritesheet,(0,0),(x,y,dx,dy))
        return gsimage
    def crash(self):
        return "sea"
    def __init__(self,x,y,direction):
        super().__init__()
        self.spritesheet = pygame.image.load("battleship"+".png")
        self.image=self.gs(0,0,64,311)
        self.rect = self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
        self.heading=C.angleToVector(direction,1)
        self.turrets = []
        self.locs = [(34,62),(34,238)]
        for i in range(len(self.locs)):
            self.turrets.append(turret(0,0))
        self.tim = 0
    def update(self,playerlist,attacklist):
        self.rect.x+=self.heading[0]
        self.rect.y+=self.heading[1]
        self.rect.y+=C.backgroundScroll
        for i in range(len(self.turrets)):
            self.turrets[i].rect.center=(self.rect.x+self.locs[i][0],self.rect.y+self.locs[i][1])
        if self.tim==0:
            self.tim+=1
            end=["ep"]
            for i in self.turrets:
                end.append(i)
            return end


class looper(pygame.sprite.Sprite):

    def gs(self,x,y,dx,dy):
        gsimage = pygame.Surface([dx, dy])
        gsimage.fill((234,154,45))
        gsimage.set_colorkey((234,154,45))
        gsimage.blit(self.spritesheet,(0,0),(x,y,dx,dy))

        return gsimage

    def __init__(self,x,y,direction,turnAround=300,shot=True):
        super().__init__()
        self.spritesheet = pygame.image.load("greenplane"+".png")
        self.image=self.gs(17,0,66,72)
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
        self.heading=direction
        self.turnAround=turnAround
        self.shot = shot
        self.looping = False
        self.speed = 2
        self.loopingAnimation=[self.gs(112,0,66,72),self.gs(209,0,66,72),self.gs(297,0,66,72),pygame.transform.rotate(self.gs(17,0,66,72),180)]
        self.loopFrame = -1
        self.loopcount = 0
        self.health = 1
    def crash(self):
        self.health-=1
    def shoot(self,playerloc):
        return projectile.shot(self.rect.center[0],self.rect.center[1],constants.vectorToAngle([self.rect.center[0]-playerloc[0],self.rect.center[1]-playerloc[1]]))
    def loop(self):
        self.loopcount=0
        self.loopFrame += 1
        self.image=self.loopingAnimation[self.loopFrame]
        self.heading[1]-=.5
        if self.loopFrame == len(self.loopingAnimation)-1:
            self.looping = False

    def update(self,playerlist,attacklist):
        #movement
        self.rect.x+=self.heading[0]*self.speed
        self.rect.y+=self.heading[1]*self.speed

        #looping method
        if self.rect.y>self.turnAround and self.looping == False:
            self.loop()
            self.looping = True
        if self.looping==True:
            self.loopcount+=1
            if self.loopcount>15:
                self.loop()
        #kill by player
        hits=pygame.sprite.spritecollide(self, attacklist, False)
        for i in hits:
            i.hit()
            self.health-=1
        if self.health<=0:
            self.kill()

        #killoff screen
        if abs(self.rect.x-400)>450 or abs(self.rect.y-300)>350:
            self.kill()
        #fire
        if self.rect.y>self.turnAround and self.shot == True:
            for i in playerlist:
                return ("ea",self.shoot(i.rect.center))
        return None
