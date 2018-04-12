import pygame
import constants
import world
import random
import math
pygame.init()

clock = pygame.time.Clock()
world.fillBackground()



'''
load
mainmenu
chose campain(what layout) level map
chose level
'''
#player1

print(len(world.huds))
fullexit=False

def singlePlaneLevel(name,lives):
    count=0
    other = True
    done=False
    lives = lives
    hero = world.player.player(100,constants.screenSize[1],"ThunderboltTurns",[64,64])
    world.players.add(hero)
    for i in hero.getHud():
        world.huds.add(i)    
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                fullexit = True
            elif event.type == pygame.KEYDOWN:
                if event.key==276:
                    hero.adjustHeading([-1,0])
                elif event.key==273:
                    hero.adjustHeading([0,-1])
                elif event.key==275:
                    hero.adjustHeading([1,0])
                elif event.key==274:
                    hero.adjustHeading([0,1])
                elif event.key == 122:
                    hero.setRoll(-1)
                elif event.key == 120:
                    hero.fireToggle(True)
                elif event.key == 99:
                    hero.setRoll(1)
                else:
                    print(event.key)
            elif event.type == pygame.KEYUP:
                if event.key==276:
                    hero.adjustHeading([1,0])
                elif event.key==273:
                    hero.adjustHeading([0,1])
                elif event.key==275:
                    hero.adjustHeading([-1,0])
                elif event.key==274:
                    hero.adjustHeading([0,-1]) 
                elif event.key == 122:
                    hero.setRoll(0)
                elif event.key == 120:
                    hero.fireToggle(False)
                elif event.key == 99:
                    hero.setRoll(0)            
    
        if hero.firing:
            if hero.fire():
                s=world.projectile.playershot(hero.rect.center[0],hero.rect.center[1],-math.pi/2)
                world.attacks.add(s)
                pygame.mixer.music.load("projectile.wav")
                pygame.mixer.music.play()
        #peeter
        count +=1
        if count>60*10:
            world.spawn()
            count=0
        for i in world.enemeys:
            action=i.update(world.players,world.attacks)
            if action !=None:
                if action[0]=="ea":
                    world.enemeyattacks.add(action[1])
                if action[0]=="ep":
                    for i in range(len(action)):
                        if i != 0:
                            world.enemeys.add(action[i])
        #
        
    
        world.moveWorld()
    
        for i in world.enemeyattacks:
            i.update()
        for i in world.players:
            action = i.update(world.enemeys,world.enemeyattacks)
            if action != None:
                if action[0] == "respawn":
                    i.kill()
                    hero = world.player.player(action[1][0]-68/2,constants.screenSize[1],"ThunderboltTurns",[68,68])
                    world.players.add(hero)
                    
                    
            
        for i in world.attacks:
            i.update()
            
        if other==True:
            world.drawall()
            other=False
        else:
            other=True       
        clock.tick(60)
        
        
        
#orginization
singlePlaneLevel("temp",3)
print("done")
pygame.quit()