import pygame
import constants as C
import world
pygame.init()
clock = pygame.time.Clock()
world.fillBackground()



'''
load
mainmenu
chose campain(what layout) level map
chose level
'''
#player1 if dies guns for player two
#player2 if dies guns for player one




fullexit=False

def singlePlaneLevel(name,lives,twoPlayer = False):
    count=0
    other = True
    done=False
    lives = lives
    tim = 0
    turretComb = []
    
    deadplayer = ["","","",""]
    hero = world.player.player(100,C.screenSize[1],"FinalSprite","left","playerOne")
    world.players.add(hero)
    hero2 = world.player.player(100,C.screenSize[1],"FinalSprite","right","playerTwo")
    if twoPlayer == True:
        world.players.add(hero2)
    
    playerOneDead = False
    playerTwoDead = False
    
    
    for i in hero.getHud():
        world.huds.add(i)
    if twoPlayer == True:
        for i in hero2.getHud():
            world.huds.add(i)
    
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                fullexit = True
            elif event.type == pygame.KEYDOWN:
                if event.key==276:
                    if playerOneDead == False:
                        hero.adjustHeading([-1,0])
                    elif playerOneDead==True:
                        turretComb.append(119)
                elif event.key==273:
                    if playerOneDead == False:
                        hero.adjustHeading([0,-1])
                    elif playerOneDead==True:
                        turretComb.append(97)                     
                elif event.key==275:
                    if playerOneDead == False:
                        hero.adjustHeading([1,0])
                    elif playerOneDead==True:
                        turretComb.append(115)                    
                elif event.key==274:
                    if playerOneDead == False:
                        hero.adjustHeading([0,1])
                    elif playerOneDead==True:
                        turretComb.append(119)                    
                elif event.key == 122:
                    if playerOneDead == False:
                        hero.setRoll(-1)
                elif event.key == 99:
                    if playerOneDead == False:
                        hero.setRoll(1)
                elif event.key == 103:
                    if playerTwoDead == False:
                        hero2.setRoll(-1)
                elif event.key == 106:
                    if playerTwoDead == False:
                        hero2.setRoll(1)                
                elif event.key == 120:
                    if playerOneDead == False:
                        hero.fireToggle(True)
                    elif playerOneDead==True:
                        hero2.fireTurret(True)
                elif event.key == 104:
                    if playerTwoDead == True:
                        hero.fireTurret(True)
                    elif playerTwoDead == False:
                        hero2.fireToggle(True)
                elif event.key == 119:
                    if playerTwoDead == True:
                        turretComb.append(119)
                    elif playerTwoDead == False:
                        hero2.adjustHeading([0,-1])
                elif event.key == 97:
                    if playerTwoDead == True:
                        turretComb.append(97)
                    elif playerTwoDead == False:
                        hero2.adjustHeading([-1,0])
                elif event.key == 115:
                    if playerTwoDead == True:
                        turretComb.append(115)
                    elif playerTwoDead == False:
                        hero2.adjustHeading([0,1])
                elif event.key == 100:
                    if playerTwoDead == True:
                        turretComb.append(100)
                    elif playerTwoDead == False:
                        hero2.adjustHeading([1,0])                 
                elif event.key == 113: #q
                    world.enemeys.add(world.enemies.Real_looper(620,-50))
                    world.enemeys.add(world.powerUp('snake'))
                elif event.key == 101: #e
                    #world.enemeys.add(world.enemies.Test_plane(620,-50))
                    #world.enemeys.add(world.enemies.Test_plane2(700,-50))  
                    pass          
                else:
                    print(event.key)
            elif event.type == pygame.KEYUP:
                if event.key==276:
                    if playerOneDead == False:
                        hero.adjustHeading([1,0])
                    elif playerOneDead==True:
                        pass
                elif event.key==273:
                    if playerOneDead == False:
                        hero.adjustHeading([0,1])
                    elif playerOneDead==True:
                        pass                    
                elif event.key==275:
                    if playerOneDead == False:
                        hero.adjustHeading([-1,0])
                    elif playerOneDead==True:
                        pass                   
                elif event.key==274:
                    if playerOneDead == False:
                        hero.adjustHeading([0,-1])
                    elif playerOneDead==True:
                        pass                    
                elif event.key == 122:
                    if playerOneDead == False:
                        hero.setRoll(0)
                elif event.key == 99:
                    if playerOneDead == False:
                        hero.setRoll(0)
                elif event.key == 103:
                    if playerTwoDead == False:
                        hero2.setRoll(0)
                elif event.key == 106:
                    if playerTwoDead == False:
                        hero2.setRoll(0)                
                elif event.key == 120:
                    if playerOneDead == False:
                        hero.fireToggle(False)
                    elif playerOneDead==True:
                        hero2.fireTurret(False)
                elif event.key == 104:
                    if playerTwoDead == False:
                        hero2.fireToggle(False)
                    elif playerTwoDead == True:
                        hero2.fireTurret(False)
                elif event.key == 119:
                    if playerTwoDead == True:
                        pass
                    elif playerTwoDead == False:
                        hero2.adjustHeading([0,1])
                elif event.key == 97:
                    if playerTwoDead == True:
                        pass
                    elif playerTwoDead == False:
                        hero2.adjustHeading([1,0])
                elif event.key == 115:
                    if playerTwoDead == True:
                        pass
                    elif playerTwoDead == False:
                        hero2.adjustHeading([0,-1])
                elif event.key == 100:
                    if playerTwoDead == True:
                        pass
                    elif playerTwoDead == False:
                        hero2.adjustHeading([-1,0])                             

        if len(turretComb)>0:
            if 119 in turretComb and 97 in turretComb:
                hero.setTurretHeading([-1,1])
                her2.setTurretHeading([-1,1])
            elif 97 in turretComb  and 115 in turretComb:
                hero.setTurretHeading([-1,-1])
                hero2.setTurretHeading([-1,-1])
            elif 115 in turretComb and 100 in turretComb:
                hero.setTurretHeading([1,-1])
                hero2.setTurretHeading([1,-1])
            elif 100 in turretComb and 119 in turretComb:
                hero.setTurretHeading([1,1])
                hero2.setTurretHeading([1,1])
            elif 119 in turretComb:
                hero.setTurretHeading([0,1])
                hero2.setTurretHeading([0,1])
            elif 97 in turretComb:
                hero.setTurretHeading([-1,0])
                hero2.setTurretHeading([-1,0])
            elif 115 in turretComb:
                hero.setTurretHeading([0,-1])
                hero2.setTurretHeading([0,-1])
            elif 100 in turretComb:
                hero.setTurretHeading([1,0])
                hero2.setTurretHeading([1,0])
            else:
                hero.setTurretHeading([0,0])
        tim +=1
        if tim == 60:
            tim = 0
        if tim%10==0:
            turretComb = []
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
                elif action[0]=="ep":
                    for i in range(len(action)):
                        if i != 0:
                            world.enemeys.add(action[i])
                elif action[0] == "explosion":
                    print("explosion1")
                    world.explode(i)



        world.moveWorld()

        for i in world.enemeyattacks:
            i.update()
        for i in world.players:
            action = i.update(world.enemeys,world.enemeyattacks)
            if action != None:
                #return("respawn",(self.rect.center),self.name,self.side,self.spritesheetname)
                if action[0] == "respawn":
                    i.kill()
                    deadplayer[2] = action[2]#name
                    deadplayer[1] = action[3]#side
                    deadplayer[0] = action[4]#image
                    
                    if action[2] == "playerOne":
                        playerOneDead = True
                        hero2.COOP(True)
                    elif action[2] == "playerTwo":
                        playerTwoDead = True
                        hero.COOP(True)
                elif action[0] == "fire":
                    for i in action:
                        if i != "fire":
                            s = i
                            world.attacks.add(s)
                            pygame.mixer.music.load("projectile.wav")
                            pygame.mixer.music.play()
                elif action[0] == "explosion":
                    print("explosion1")
                    world.explode(i)
                elif action[0] == "revive":
                    if playerOneDead == True:
                        hero = world.player.player(i.rect.y+i.rect.height,i.rect.x+i.rect.width,deadplayer[0],deadplayer[1],deadplayer[2])
                        i.COOP(False)
                        playerOneDead = False
                        world.players.add(hero)
                    elif playerTwoDead == True:
                        hero2 = world.player.player(i.rect.y+i.rect.height,i.rect.x+i.rect.width,deadplayer[0],deadplayer[1],deadplayer[2])
                        playerTwoDead = False
                        i.COOP(False)
                        world.players.add(hero2)



        for i in world.attacks:
            i.update()
        for i in world.FX:
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
