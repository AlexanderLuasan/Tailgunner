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
    def gs(self,x,y,dx,dy):
        gsimage = pygame.Surface([dx, dy])
        gsimage.fill((234,154,45))
        gsimage.set_colorkey((234,154,45))
        gsimage.blit(self.spritesheet,(0,0),(x,y,dx,dy))
        return gsimage
    def __init__(self,x,y):
        super().__init__()
        self.has_looped = False
        self.health = 10
        self.spritesheet = pygame.image.load("greenplane"+".png")
        self.animation = [self.gs(18,0,64,72),self.gs(114,0,64,72),self.gs(210,0,64,72),self.gs(298,0,64,72)]
        self.image = self.animation[0]
        self.tim = 0
        self.heading = [0,0]
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
        self.health = 3
        image_path_name = C.os.getcwd() + "/assets/Hayabusa.png"
        self.spritesheet = pygame.image.load(image_path_name)
        self.animation = []
        templist = []
        for b in range(4): #0,1,2
            for i in range(5):
                templist.append(pygame.transform.flip(self.gs(56*b,48*i,57,48), False, True))
            self.animation.append(templist)
            templist = []
        self.animation.append([])
        print(len(self.animation))

        #self.animation is a nested list
        #self.animation[0] is a list of rotor, nonfiring images
        #self.animation[1] is a list of non rotor, nonfiring images
        #[2] and [3] are [0] and [1], but firing
        #[4] contains loop images, and will be altered durring the loop func
        #in these nested lists, 0 = leftmost heading, 2 = forward heading, 4 = rightmost heading
        self.image = self.animation[3][2]
        self.heading = [0,0]
        self.acceleration_vector = [0,0]
        self.rect = self.image.get_rect()
        self.rect.x = x + self.rect.width/2
        self.rect.y= y + self.rect.height/2
        self.fire = 0
        self.tim = 0

    def evasive_manuvers(self):
        """semi-randomly adjusts the acceleration vector, in such a way that will typically keep the plane onscreen"""
        """and modifies self.image as appropriate"""

        temp = (C.screenSize[0]/2- self.rect.x) #negative when x is to the right of the center, positive if to the left
        temp2 = C.random.randint(0,C.screenSize[0]) - C.screenSize[0]/2 # random num between -1/2 screen size, and positive 1/2 screensize
        temp3 = temp2+ .14 * temp


        if temp3 > 0:
            self.acceleration_vector[0] += .01
        else:
            self.acceleration_vector[0] -= .01

        if self.acceleration_vector[0] > .1:
            self.acceleration_vector[0] = .1
        elif self.acceleration_vector[0] < -.1:
            self.acceleration_vector[0] = -.1

        self.update_image()


    def update_image(self):
        """updates  self.image as apropriate to the current heading and status"""
        currentx = self.heading[0]



        #selects the animation list, as appropriate.
        #if firing, it'll select a list from self.animation that contains firing sprites
        #rotors are dependent on self.tim, and flip every update
        if self.fire < 5:
            if self.tim % 3:
                animations_list = self.animation[2]
            else:
                animations_list = self.animation[3]
        else:
            if self.tim % 3:
                animations_list = self.animation[0]
            else:
                animations_list = self.animation[1]

        #selects the correct sprite from animations_list, as dependent on x heading

        if currentx >= 2:
            self.image = animations_list[4]
        elif currentx >= 1:
            self.image = animations_list[3]
        elif 1 > currentx > -1:
            self.image = animations_list[2]
        elif currentx <= -1:
            self.image = animations_list[1]
        elif currentx <= -2:
            self.image = animations_list[0]


    def loop_de_loop(self):
        """makes y accel negative until a certain y velocity is hit, then sets self.has_looped to true"""
        """also adjusts self.image as appropriate"""
        self.acceleration_vector[0] = -self.heading[0]/3
        if self.heading[1] == 0:
            image_path_name = C.os.getcwd() + "/assets/Hayabusaflip.png"
            self.has_looped = "in progress"
            self.spritesheet = pygame.image.load(image_path_name)
            self.animation[4] = [self.gs(57,0,57,48), self.gs(114,0,57,48)]
            self.acceleration_vector[1] = - .03


        #print(self.heading[1])
        if self.heading[1] > -1:
            self.update_image()
        else:
            if self.tim % 3:
                self.image = self.animation[4][0]
            else:
                self.image = self.animation[4][1]
        if isinstance(self.has_looped, str):
            if self.has_looped == "in progress" and self.heading[1]<=-1:
                self.animation[4] = [self.gs(0,48,57,48), self.gs(60,48,57,48)]
                self.has_looped = "in progress2"
            elif self.has_looped == "in progress2" and self.heading[1] <= -2:
                self.animation[4] = [self.gs(0,96,57,48), self.gs(60,96,57,48)]
                self.has_looped = "in progress3"
            elif self.has_looped == "in progress3" and self.heading[1] <= -3:
                self.animation[4] = [self.gs(0,144,57,48), self.gs(60,144,57,48)]
                self.heading[1] = -3
                self.has_looped = [5, "4"]
                self.acceleration_vector[1] = 0


        elif isinstance(self.has_looped, list):
            if self.has_looped[0] >= 0:
                self.has_looped[0] -= 1
            elif self.has_looped[1] == "4":
                self.animation[4] = [self.gs(0,192,57,48), self.gs(60,192,57,48)]
                self.has_looped[0] = 5
                self.has_looped[1] = "5"
            elif self.has_looped[1] == "5":
                self.animation[4] = [self.gs(0,240,57,48), self.gs(60,240,57,48)]
                self.has_looped[0] = 5
                self.has_looped[1] = "6"
            elif self.has_looped[1] == "6":
                self.animation[4] = [self.gs(0,288,57,48), self.gs(60,288,57,48)]
                self.has_looped[0] = 5
                self.has_looped[1] = "7"
            elif self.has_looped[1] == "7":
                self.animation[4] = [self.gs(0,336,57,48), self.gs(60,336,57,48)]
                self.has_looped[0] = 5
                self.has_looped[1] = "8"
            elif self.has_looped[1] == "8":
                self.animation[4] = [self.gs(0,384,57,48), self.gs(60,384,57,48)]
                self.has_looped[0] = 5
                self.has_looped[1] = "9"
            elif self.has_looped[1] == "9":
                self.animation[4] = [self.gs(0,432,57,48), self.gs(60,432,57,48)]
                self.has_looped[0] = 5
                self.has_looped[1] = "10"
            elif self.has_looped[1] == "10":
                self.animation[4] = [self.gs(0,480,57,48), self.gs(60,480,57,48)]
                self.has_looped[0] = 5
                self.has_looped[1] = "11"
            elif self.has_looped[1] == "11":
                self.has_looped = True
                self.flips_images()

        #this is really unreadable, and I'm sorry if you're trying to understand it -Keaton





    def flips_images(self):
        """flips all the images in self.animation"""
        for mylist in self.animation:
            for i in range(len(mylist)):
                mylist[i] = pygame.transform.flip(mylist[i], False, True)


    def update(self,playerlist,attacklist):
        """moves the player, checks if they've been hit, checks if they've died"""
        self.rect.x+= self.heading[0]
        #print(self.heading[1]) #del later
        #print(self.rect.y) #del
        self.rect.y+= self.heading[1]
        #print(self.rect.y) #del
        self.heading[0] += self.acceleration_vector[0]
        self.heading[1] += self.acceleration_vector[1]
        #print(self.heading[0])


        if self.heading[0] > 2:
            self.heading[0] = 2
        elif self.heading[0] < -2:
            self.heading[0] = -2


        #did I get hit?
        hits=pygame.sprite.spritecollide(self, attacklist, False)
        for i in hits:
            temp=i.hit()
            self.health-=temp
        if self.health<=0:
            self.kill()

        #am I offscreen?
        if abs(self.rect.x-C.screenSize[0]/2)>1000 or abs(self.rect.y-C.screenSize[1]/2)>1000:
            self.kill()
            
        if self.rect.y > C.screenSize[1]-200 or not isinstance(self.has_looped,bool):
            self.loop_de_loop()
        else:
            self.evasive_manuvers()

        self.tim += 1

        #should I shoot?
        target = closest(self,playerlist)
        self.fire +=1
        if abs((self.rect.x+self.rect.width/2)-(target.rect.x+target.rect.width/2))<5 and self.fire>C.PlayerFPS/C.enemiesFPS*30:
            self.fire = 0
            return("ea",projectile.zeroShot(self.rect.center[0],self.rect.bottom,C.math.pi/2))

        #print(self.heading[1])
        #print(self.rect.y)
        #print("___")



class strafer(pygame.sprite.Sprite):
    def gs(self,x,y,dx,dy):
        gsimage = pygame.Surface([dx, dy])
        gsimage.fill((255,255,255))
        gsimage.set_colorkey((255,255,255))
        gsimage.blit(self.spritesheet,(0,0),(x,y,dx,dy))
        return gsimage
    def crash(self):
        self.kill()
    def __init__(self,x,y,direction,wing=5,side = "both"):
        super().__init__() #24,24
        spritesheet_path = C.os.getcwd() + "/assets/Updated0.png"
        self.spritesheet = pygame.transform.flip(pygame.image.load(spritesheet_path),False,True)
        self.angles = [0,C.math.pi/4,C.math.pi/2,3*C.math.pi/4,C.math.pi]
        self.anglePos = 2
        self.animation = [] #pygame.transform.scale2x()
        for i in range(4):
            templist = []
            for b in range(5):
                templist.append(self.gs(58*i,45*b,58,45)) # (57-59)ishx45
            self.animation.append(templist)
        #self.animation is now a nested list.
        #[0] rotor no fire, [1] no rotor no fire, [2] rotor fire, [3] no rotor fire
        """
        for i in range(len(self.animation)):
            for b in range(len(self.animation[i])):
                self.animation[i][b]=pygame.transform.scale2x(self.animation[i][b])
        """
        self.image = self.animation[0][2]
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

        self.timm = 0

        if self.wings == 4:
            self.keatflag = True
        else:
            self.keatflag = False

    def update_image(self):
        "updates self.image as appropriate"
        self.timm += 1
        if self.rect.y<100:
            if self.timm % 3:
                tempindex = 0
            else:
                tempindex = 1
            self.image = self.animation[tempindex][2]

        else:
            if self.fire < 5: #mod this val if you want the muzzle flash to be longer
                if self.timm % 3:
                    tempindex = 2
                else:
                    tempindex = 3
            else:
                if self.timm % 3:
                    tempindex = 0
                else:
                    tempindex = 1
            self.image = self.animation[tempindex][self.anglePos]





    def update(self,playerlist,attacklist):
        #print("hello!" + str(self.tim))
        self.update_image()
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
        self.tim+=1
        target = closest(self,playerlist)
        if target==None:
            return None
        if self.tim >C.PlayerFPS/C.enemiesFPS*30:
            if target.rect.x<self.rect.x:
                self.anglePos+=1
                if self.anglePos>=len(self.animation[0]):
                    self.anglePos-=1
            elif target.rect.x>self.rect.x:
                self.anglePos-=1
                if self.anglePos<0:
                    self.anglePos=0
            self.heading=C.angleToVector(self.angles[self.anglePos],2)
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





#flies in a circle

#flies in given direction untill on screen
#summons next of kin
#stright
#circle
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
        self.dead = False
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

        
        self.kin=None

        self.delayCount = SPIN_DELAY
        if wing>0:
            self.delayCount*=-1
            if side=="both":
                self.kin = SpinPlane(self.rect.x+self.rect.width/2,self.rect.y+self.rect.height/2,direction*-1,wing-1,"both")
            else:
                self.kin = SpinPlane(self.rect.x+self.rect.width/2,self.rect.y+self.rect.height/2,direction,wing-1,"left")

    def collectKin(self):
        if self.kin==None:
            return []
        else:
            lowerplanes = self.kin.collectKin()
            lowerplanes.append(self.kin)
            return lowerplanes



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
            self.dead = True
            self.kill()
        if abs(self.rect.x-C.screenSize[0]/2)>1000 or abs(self.rect.y-C.screenSize[1]/2)>1000:
            self.dead = True
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
        self.dead = True
        self.kill()
    def setSpin(self,position):#sets image and angle
        self.position=position
        self.spin(0)
    def spin(self,direction):#increments the image and angle and readjust position
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
        self.heading = C.angleToVector(self.animationAngles[self.position],SPINSPEED)
        self.spinDirection = direction
        self.tim = 0 #miain counter
        self.mode = "stright" #stright or circle or oval
        self.propCount = 0



        if self.rect.right<0:
            self.setSpin(int(self.divisions/4))
            self.rect.right = -10
            self.direction = "right"
        elif self.rect.left>C.screenSize[0]:
            self.setSpin(3*int(self.divisions/4))
            self.rect.left = C.screenSize[0]+10
            self.direction = "left"

        self.delayCount = -30
        if wing>0:
            self.delayCount*=-1
            if side=="both":
                self.kin = circlePlane(self.rect.x,self.rect.y-self.rect.height/2,direction*-1,wing-1,"both")
            else:
                self.kin = circlePlane(self.rect.x,self.rect.y-self.rect.height/2,direction,wing-1,"None")
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
            if self.tim > (self.divisions)*5:
                self.mode = "stright"
                self.tim = 0
        elif self.mode == "stright":
            if self.tim > 60:
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
