import math
import random

import os


#class used to pass constants around
class constant():
    def __init__(self):
        self.constants = {}
    def addC(self,key,value):
        self.constants[key] = value
    def getC(self,key):
        return self.constants[key]
    def getImage(name):
        """ Arguments: the name of the file
        returns the absolute path to said file as a string
        (Keaton's side note, doesn't this just do the exact same thing as os.path.abspath(filename)?
        """
        current_path = os.path.dirname(__file__) 
        image_path = os.path.join(current_path, name) 
        return(image_path)    
    def angleToVector(angle,size):
        """arguments: the angle in radians, the magnitude of the vecto
        returns a list with list[0] being the x component, and list[1] being the y component
        """
        return [round(size*math.cos(angle),3),round(size*math.sin(angle),3)]
    def vectorToAngle(vector):
        """Agruments: A list, list[0] represents the x component of the vector, list[1] represents the Y
        if the x component of a the vector has a magnitude of less then 10, return pi/2.
        else, return the angle in radians
        """
        if abs(vector[0])-.001<0:
            return math.pi/2
        if vector[0]>0:
            return math.atan(vector[1]/vector[0])
        else:
            return round(math.pi-math.atan(vector[1]/-vector[0]),3)
    def roundVector(vector):
        end = [0,0]
        if vector[0]>0:
            end[0] = int(vector[0]+.5)
        elif vector[0]<0:
            end[0] = int(vector[0]-.5)
        if vector[1]>0:
            end[1] = int(vector[1]+.5)
        elif vector[1]<0:
            end[1] = int(vector[1]-.5)
        return end



def makeConstants():
    end = constant()
    end.addC("PlayerSpeed",3)
    end.addC("FPS",60)
    end.addC("PlayerFPS",60)
    end.addC("enemiesFPS",60)
    end.addC("projectleFPS",60)
    end.addC("screenSize",(1280,800))
    end.addC("backgroundScroll",2)
    return end
    
#speed
PlayerSpeed = 3

#framerate
FPS =60
PlayerFPS = 60
enemiesFPS = 60
projectleFPS = 60

screenSize = (1280,800)
backgroundScroll =2


def getImage(name):
    """ Arguments: the name of the file
    returns the absolute path to said file as a string
    (Keaton's side note, doesn't this just do the exact same thing as os.path.abspath(filename)?
    """
    current_path = os.path.dirname(__file__) 
    image_path = os.path.join(current_path, name) 
    return(image_path)

def angleToVector(angle,size):
    """arguments: the angle in radians, the magnitude of the vecto
    returns a list with list[0] being the x component, and list[1] being the y component
    """
    return [round(size*math.cos(angle),3),round(size*math.sin(angle),3)]

def vectorToAngle(vector):
    """Agruments: A list, list[0] represents the x component of the vector, list[1] represents the Y
    if the x component of a the vector has a magnitude of less then 10, return pi/2.
    else, return the angle in radians
    """
    if abs(vector[0])-.001<0:
        return math.pi/2
    if vector[0]>0:
        return math.atan(vector[1]/vector[0])
    else:
        return round(math.pi-math.atan(vector[1]/-vector[0]),3)

def roundVector(vector):
    end = [0,0]
    if vector[0]>0:
        end[0] = int(vector[0]+.5)
    elif vector[0]<0:
        end[0] = int(vector[0]-.5)
    if vector[1]>0:
        end[1] = int(vector[1]+.5)
    elif vector[1]<0:
        end[1] = int(vector[1]-.5)
    return end
        
    
 