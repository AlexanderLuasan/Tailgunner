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



world.fx.smokeINIT()
fullexit=False

def singlePlaneLevel(twoPlayers = False,twoPlanes = False):
    count=0
    score = 0
    scorecount = world.levelText("score: "+str(score),(100,100),40,(198,124,49),1000)
    world.FX.add(scorecount)
    other = True
    done=False
    tim = 0
    turretComb = []
    currentlevel=0
    levelprogress = 100
    roundprogress = 100
    #game states
    canRevive = twoPlanes
    deadplayer = ["","","",""]
    #setup one player
    hero = world.player.player(100,C.screenSize[1],"FinalSprite","left","playerOne")
    world.players.add(hero)
    playerOneDead = False
    for i in hero.getHud():
        world.huds.add(i)
        
    #playertwo setup
    if twoPlanes==True:
        hero2 = world.player.player(100,C.screenSize[1],"FinalSprite","right","playerTwo")
        world.players.add(hero2)
        playerTwoDead = False
    elif twoPlayers==True:
        playerTwoDead = True
        hero.COOP(True)
    else:
        playerTwoDead = False
    
    
    if twoPlanes == True:
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
                        turretComb.append(97)
                elif event.key==273:
                    if playerOneDead == False:
                        hero.adjustHeading([0,-1])
                    elif playerOneDead==True:
                        turretComb.append(119)              
                elif event.key==275:
                    if playerOneDead == False:
                        hero.adjustHeading([1,0])
                    elif playerOneDead==True:
                        turretComb.append(100)         
                elif event.key==274:
                    if playerOneDead == False:
                        hero.adjustHeading([0,1])
                    elif playerOneDead==True:
                        turretComb.append(115)                    
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
                    world.spawn()
                elif event.key == 101: #e
                    world.enemeys.add(world.bosses.bigPlane(500,30))

                    pass          
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
                        if playerTwoDead == False and twoPlanes == True:
                            hero2.fireToggle(False)
                        elif playerTwoDead == True:
                            hero.fireTurret(False)
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
                if twoPlanes == True:
                    hero2.setTurretHeading([-1,1])
            elif 97 in turretComb  and 115 in turretComb:
                hero.setTurretHeading([-1,-1])
                if twoPlanes == True:
                    hero2.setTurretHeading([-1,-1])
            elif 115 in turretComb and 100 in turretComb:
                hero.setTurretHeading([1,-1])
                if twoPlanes == True:
                    hero2.setTurretHeading([1,-1])
            elif 100 in turretComb and 119 in turretComb:
                hero.setTurretHeading([1,1])
                if twoPlanes == True:
                    hero2.setTurretHeading([1,1])
            elif 119 in turretComb:
                hero.setTurretHeading([0,1])
                if twoPlanes == True:
                    hero2.setTurretHeading([0,1])
            elif 97 in turretComb:
                hero.setTurretHeading([-1,0])
                if twoPlanes == True:
                    hero2.setTurretHeading([-1,0])
            elif 115 in turretComb:
                hero.setTurretHeading([0,-1])
                if twoPlanes == True:
                    hero2.setTurretHeading([0,-1])
            elif 100 in turretComb:
                hero.setTurretHeading([1,0])
                if twoPlanes == True:
                    hero2.setTurretHeading([1,0])
            else:
                hero.setTurretHeading([0,0])
                if twoPlanes == True:
                    hero2.setTurretHeading([0,0])                
        tim +=1
        if tim == 60:
            tim = 0
        if tim%10==0:
            turretComb = []
        #peeter
        #updater fucntions
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
                    try:
                        world.explode(i,action[1]=="cheap")
                    except:
                        world.explode(i)
                    try:
                        i.die()
                    except:
                        i.kill()
                    scorecount.kill()
                    score+=1
                    scorecount = world.levelText("score: "+str(score),(100,100),40,(198,124,49),1000)
                    world.FX.add(scorecount)
                        
                        
        #level and difficulty modulation
        
        roundprogress+=1  
        if roundprogress>60*5:#5seconds
            roundprogress=0
            levelprogress+=1
            if levelprogress>10:
                currentlevel+=1
                levelprogress=0
                if currentlevel == 5:
                    world.FX.add(world.levelText("Boss Level",(C.screenSize[0]/2,C.screenSize[1]/3),40,(198,124,49),180))
                    world.enemeys.add(world.bosses.bigPlane(500,-500))
                    
                else:
                    world.FX.add(world.levelText("level "+str(currentlevel),(C.screenSize[0]/2,C.screenSize[1]/3),40,(198,124,49),180))
            else:
                if currentlevel<5:
                    world.spawn(currentlevel-5)
                
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
                    if twoPlanes==True:
                        if action[2] == "playerOne" and playerTwoDead==True:
                            return "game over"
                        elif action[2] == "playerTwo" and playerOneDead==True:
                            return "game over"
                        if action[2] == "playerOne":
                            playerOneDead = True
                            hero2.COOP(True)
                        elif action[2] == "playerTwo":
                            playerTwoDead = True
                            hero.COOP(True)
                    else:
                        return "game over"
                elif action[0] == "fire":
                    for i in action:
                        if i != "fire":
                            s = i
                            world.attacks.add(s)
                            pygame.mixer.music.load("projectile.wav")
                            pygame.mixer.music.play()
                elif action[0] == "explosion":
                    world.explode(i)
                elif action[0] == "revive":
                    try:
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
                    except:
                        pass
        for i in world.attacks:
            i.update()
        for i in world.FX:
            i.update()
        if len(world.FX) == 0 and playerOneDead == True and playerTwoDead == True:
            return('gameover')
        if other==True:
            world.drawall()
            other=False
        else:
            other=True
        clock.tick(60)


def startpage():
    first=True
    optionposition = 0
    selector = world.arrow(10,180)
    world.FX.add(selector)
    Title = world.levelText("Tailgunner",(C.screenSize[0]/2,C.screenSize[1]/6),60,(198,124,49),180)
    world.FX.add(Title)
    SinglePlayer = world.levelText("SinglePlayer",(C.screenSize[0]/2,C.screenSize[1]/3),40,(198,124,49),180)
    world.FX.add(SinglePlayer)
    coop = world.levelText("COOP",(C.screenSize[0]/2,C.screenSize[1]/3+100),40,(198,124,49),180)
    world.FX.add(coop)  
    
    TwoPlayers = world.levelText("TwoPlayers",(C.screenSize[0]/2,C.screenSize[1]/3+200),40,(198,124,49),180)
    world.FX.add(TwoPlayers)        
    Exit = world.levelText("Exit",(C.screenSize[0]/2,C.screenSize[1]/3+300),40,(198,124,49),180)
    world.FX.add(Exit)
    options = [SinglePlayer,coop,TwoPlayers,Exit]    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                fullexit = True  
                return "exit"
            if event.type == pygame.KEYDOWN:
                if event.key==273:
                    optionposition-=1
                    if optionposition<0:
                        optionposition=len(options)-1
                elif event.key==274:
                    optionposition+=1
                    if optionposition>len(options)-1:
                        optionposition=0  
                elif event.key == 120:
                    #return the results
                    if optionposition==0:
                        return "one"
                    elif optionposition==3:
                        return "exit"
                    elif optionposition==1:
                        return "coop"
                    elif optionposition==2:
                        return "two"                       
                    
                    
                else:
                    pass

            
        #move selector
        pos = [options[optionposition].rect.left,options[optionposition].rect.center[1]]
        selector.setpos(pos[0],pos[1])
        
        s=world.drawall()
        world.moveWorld()
        
#orginization


choice = startpage()


if choice == "one":
    singlePlaneLevel(twoPlayers = False,twoPlanes = False)
elif choice == "coop":
    singlePlaneLevel(twoPlayers = True,twoPlanes = False)
elif choice == "two":
    singlePlaneLevel(twoPlayers = False,twoPlanes = True)
elif choice == "exit":
    pass
print("done")
pygame.quit()
