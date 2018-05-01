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
#player1

print(len(world.huds))
fullexit=False

def singlePlaneLevel(name,lives):
    count=0
    other = True
    done=False
    lives = lives
    tim = 0
    turretComb = []
    hero = world.player.player(100,C.screenSize[1],"FinalSprite",[64,64])
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
                elif event.key == 32:
                    hero.fireTurret(True)
                elif event.key == 119:
                    turretComb.append(119)
                elif event.key == 97:
                    turretComb.append(97)
                elif event.key == 115:
                    turretComb.append(115)
                elif event.key == 100:
                    turretComb.append(100)
                elif event.key == 113: #q
                    world.enemeys.add(world.enemies.Real_looper(620,-50))
                elif event.key == 101: #e
                    world.enemeys.add(world.enemies.Test_plane(620,-50))
                    world.enemeys.add(world.enemies.Test_plane2(700,-50))
                elif event.key == 113:
                    world.enemeys.add(world.enemies.SpinPlane(-50,200))
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
                elif event.key == 32:
                    hero.fireTurret(False)                

        if len(turretComb)>0:

            if 119 in turretComb and 97 in turretComb:
                hero.setTurretHeading([-1,1])
            elif 97 in turretComb  and 115 in turretComb:
                hero.setTurretHeading([-1,-1])
            elif 115 in turretComb and 100 in turretComb:
                hero.setTurretHeading([1,-1])
            elif 100 in turretComb and 119 in turretComb:
                hero.setTurretHeading([1,1])
            elif 119 in turretComb:
                hero.setTurretHeading([0,1])
            elif 97 in turretComb:
                hero.setTurretHeading([-1,0])
            elif 115 in turretComb:
                hero.setTurretHeading([0,-1])
            elif 100 in turretComb:
                hero.setTurretHeading([1,0])
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
                if action[0]=="ep":
                    for i in range(len(action)):
                        if i != 0:
                            world.enemeys.add(action[i])



        world.moveWorld()

        for i in world.enemeyattacks:
            i.update()
        for i in world.players:
            action = i.update(world.enemeys,world.enemeyattacks)

            if action != None:
                if action[0] == "respawn":
                    i.kill()
                    hero = world.player.player(action[1][0]-68/2,C.screenSize[1],"FinalSprite",[68,68])
                    world.players.add(hero)
                    for i in hero.getHud():
                        world.huds.add(i)
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
