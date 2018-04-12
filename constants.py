import math
import random
screenSize = (1280,800)
backgroundScroll =2
import os




#speed
PlayerSpeed = 3

#framerate
FPS =60
PlayerFPS = 60
enemiesFPS = 60
projectleFPS = 60

def getImage(name):
    current_path = os.path.dirname(__file__) 
    image_path = os.path.join(current_path, name) 
    return(image_path)
def angleToVector(angle,size):
    return [round(size*math.cos(angle),3),round(size*math.sin(angle),3)]
def vectorToAngle(vector):
    if abs(vector[0])-10<0:
        return math.pi/2
    if vector[0]>0:
        return math.atan(vector[1]/vector[0])
    else:
        return round(math.pi-math.atan(vector[1]/-vector[0]),3)