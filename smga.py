import pygame, sys, time, random
from pygame.locals import *

pygame.init()
pygame.font.init()
pygame.mixer.init() 
mainClock = pygame.time.Clock()

screenWidth = 800
screenHeight = 600
screen = pygame.display.set_mode((screenWidth, screenHeight), 0, 0)
pygame.display.set_caption('Super Mega Game of Awesome')
endScreen = pygame.Surface((screenWidth, screenHeight), pygame.SRCALPHA)

moveForward = False
moveBack = False

distDownHall = 20
hallLength = 1000
currPanelS = 0 
currPanelT = 0 

#Player Variables
health = 10
mana = 10
manaRegenerator = 0
healing = False
damageFlash = False 
fireballLaunch = False
fireballPos = 29
fireballImage = pygame.image.load('fireball.png')

#Misc Variables
level = 0
paused = False
pauseBox = 0
mousex = 0
mousey = 0
TNR20 = pygame.font.SysFont("TimesNewRoman", 20)
TNR30 = pygame.font.SysFont("TimesNewRoman", 30)
conditionFont = pygame.font.SysFont('DefaultFONTHORRAY!!!',25)
Castellar = pygame.font.SysFont('Castellar',40)
mainMenuIMG = pygame.image.load('MainMenu.png')
instructIMG = pygame.image.load('InstructionPage.png')
playButton = pygame.Rect(342,325,110,40)
instructionsButton = pygame.Rect(235,385,330,40)
creditsButton = pygame.Rect(305,505,180,40)
highScoreButton = pygame.Rect(260,445,300,40)
iBackButton = pygame.Rect(400,435,350,40)
mute = False
muteState = "False"
alpha = 0
slash = False
creditsPos = 0
levelingUp = 0
scroll = 0

#Enemy Variables
enemySpawn = False
spawnEnemies = True
enemyType = 0
enemyPos = 0
enemyMovement = 0
enemyAttack = 0
hammerLeftImage = pygame.image.load('hammerGoblinLeft.png')
hammerRightImage = pygame.image.load('hammerGoblinRight.png')
hammerStand = pygame.image.load('hammerGoblinStand.png')
hammerWindUp1 = pygame.image.load('hammerGoblinWindUp1.png')
hammerWindUp2 = pygame.image.load('hammerGoblinWindUp2.png')
hammerAttackImage = pygame.image.load('hammerGoblinAttack.png')

hammerLeftImageDmg = pygame.image.load('hammerGoblinLeftDmg.png')
hammerRightImageDmg = pygame.image.load('hammerGoblinRightDmg.png')
hammerStandDmg = pygame.image.load('hammerGoblinStandDmg.png')
hammerWindUp1Dmg = pygame.image.load('hammerGoblinWindUp1Dmg.png')
hammerWindUp2Dmg = pygame.image.load('hammerGoblinWindUp2Dmg.png')
hammerAttackImageDmg = pygame.image.load('hammerGoblinAttackDmg.png')

swordLeftImage = pygame.image.load('swordGoblinLeft.png')
swordRightImage = pygame.image.load('swordGoblinRight.png')
swordStand = pygame.image.load('swordGoblinStand.png')
swordWindUp = pygame.image.load('swordGoblinWindUp.png')
swordAttackImage = pygame.image.load('swordGoblinAttack.png')

swordLeftImageDmg = pygame.image.load('swordGoblinLeftDmg.png')
swordRightImageDmg = pygame.image.load('swordGoblinRightDmg.png')
swordStandDmg = pygame.image.load('swordGoblinStandDmg.png')
swordWindUpDmg = pygame.image.load('swordGoblinWindUpDmg.png')
swordAttackImageDmg = pygame.image.load('swordGoblinAttackDmg.png')

bowLeftImage = pygame.image.load('bowGoblinLeft.png')
bowRightImage = pygame.image.load('bowGoblinRight.png')
bowStand = pygame.image.load('bowGoblinStand.png')
bowWindUp1 = pygame.image.load('bowGoblinWindUp1.png')
bowWindUp2 = pygame.image.load('bowGoblinWindUp2.png')
bowAttackImage = pygame.image.load('bowGoblinAttack.png')

bowLeftImageDmg = pygame.image.load('bowGoblinLeftDmg.png')
bowRightImageDmg = pygame.image.load('bowGoblinRightDmg.png')
bowStandDmg = pygame.image.load('bowGoblinStandDmg.png')
bowWindUp1Dmg = pygame.image.load('bowGoblinWindUp1Dmg.png')
bowWindUp2Dmg = pygame.image.load('bowGoblinWindUp2Dmg.png')
bowAttackImageDmg = pygame.image.load('bowGoblinAttackDmg.png')

enemyLeft = False
enemyHealth = 0
attackWindUp = False
attackTimer = 0

#enemyDamageImage 
enemy = pygame.Rect(0,0,0,0)
       
#Walls
gwall1L = pygame.image.load('greywall1.png')
gwall2L = pygame.image.load('greywall2.png')
gwall1R = pygame.image.load('greywall1inverted.png')
gwall2R = pygame.image.load('greywall2inverted.png')
panelListL = [gwall1L,gwall2L,gwall1L]
panelListR= [gwall1R,gwall2R,gwall1R]
backWall = pygame.image.load('Back Wall.png')
wallLength = 98
wallHeight = 136

#Floor Ceiling Panels
floor1 = pygame.image.load('floor1.png')
floor2 = pygame.image.load('floor2.png')
ceiling = pygame.image.load('stoneCeiling.png')
ceiling2 = pygame.image.load('stoneCeiling2.png')
panelListT = [ceiling, ceiling2, ceiling]
panelListB = [floor1,floor2,floor1]

#Sounds
swordMiss = pygame.mixer.Sound('swordmiss.ogg')
swordCut = pygame.mixer.Sound('swordcut.ogg')
swordHit = pygame.mixer.Sound('swordhit.ogg')
swordBlocked = pygame.mixer.Sound('swordblocked.wav')
fireballLaunch1 = pygame.mixer.Sound('launchfireball1.wav')
fireballLaunch2 = pygame.mixer.Sound('launchfireball2.wav')
fireballImpact = pygame.mixer.Sound('fireballimpact.wav')
playerHurtNoise = pygame.mixer.Sound('hurt.wav')
enemyHurt = pygame.mixer.Sound('enemyhurt.ogg')
outOfMana = pygame.mixer.Sound('outofmana.wav')
heal = pygame.mixer.Sound('heal.ogg')
pygame.mixer.music.load('startmenumusic.mp3')
pygame.mixer.music.play(-1, 0.0)

def walls():
    totalX = 0 
    totalY = 0 
    panelNum = currPanelS
    panelMod = 0
    for i in range (27,0,-1):
        height = 600 - 4.0/3.0*(totalX)
        panelL = pygame.Rect(totalX, totalY, i, height)
        panelR = pygame.Rect(800 - (i + totalX),totalY,i,height)
        leftPanel = pygame.transform.scale(panelListL[panelNum],(panelL.width,panelL.height))
        rightPanel = pygame.transform.scale(panelListR[panelNum],(panelR.width,panelR.height))
        screen.blit(leftPanel,panelL)
        screen.blit(rightPanel,panelR)
        totalX += i
        totalY = 2.0/3.0*totalX
        totalY = int(round(totalY))
        if panelMod + currPanelS < len(panelListL)- 1:
            panelMod += 1
        else:
            panelMod -= len(panelListL)-1
        panelNum = currPanelS + panelMod
        
def floorCeiling():
    totalX = 0
    totalY = 0
    panelNum = currPanelT
    panelMod = 0
    for i in range (22,0,-1):
        width = 800 - 4.0/3.0*(totalY)
        panelT = pygame.Rect(totalY * 3/2, totalY, 800 - totalY*3, i)
        panelB = pygame.Rect(totalY * 3/2, 600 - (totalY + i), 800 - totalY*3, i)
        topPanel = pygame.transform.scale(panelListT[panelNum],(panelT.width,panelT.height))
        botPanel = pygame.transform.scale(panelListB[panelNum],(panelB.width,panelB.height))
        screen.blit(topPanel,panelT)
        screen.blit(botPanel,panelB)
        totalY += i
        totalX = 2.0/3.0*totalX
        totalX = int(round(totalY))
        if panelMod + currPanelT < len(panelListT)- 1:
            panelMod += 1
        else:
            panelMod -= len(panelListT)-1
        panelNum = currPanelT + panelMod

def music():
    if level == 0:
        pygame.mixer.music.load('startmenumusic.mp3')
        pygame.mixer.music.play(-1, 0.0)
    else:
        pygame.mixer.music.load('ingamemusic.mp3')
        pygame.mixer.music.play(-1, 0.0)

def enemyGen():
    global enemySpawn
    global enemyMovement
    global enemyPos
    global xModifier
    global enemy
    global enemyImage
    global enemyLeft
    global enemyHealth
    global enemyAttack
    global enemyType
    global health
    global damageFlash
    global distDownHall
    global currPanelS
    global currPanelT
    global fireBallPos
    global causeOfDeath
    generator = random.randint(1,25)
    if enemySpawn == False and generator == 15 and spawnEnemies:
        enemySpawn = True
        enemyType = random.randint(1,3)
        xModifier = random.randint(-10,10)
        enemy = pygame.Rect(400 + xModifier,400,1,1)
        if enemyType == 1: 
            enemyHealth = 5
        if enemyType == 2:
            enemyHealth = 3
        if enemyType == 3:
            enemyHealth = 3
    if enemySpawn == True:
        enemyMovement += 1
        if enemyMovement > 8 and enemyPos < 15 and enemyType == 3:
            enemyPos += 1
            enemyMovement = 0
            enemyLeft = not enemyLeft
        elif enemyMovement > 3 and enemyPos < 29 and enemyType == 2:
            enemyPos += 1
            enemyMovement = 0
            enemyLeft = not enemyLeft
            
        elif enemyMovement > 15 and enemyPos < 29 and enemyType == 1:
            enemyPos += 1
            enemyMovement = 0
            enemyLeft = not enemyLeft
            
        elif enemyPos >= 15 and enemyType == 3:
            enemyAttack += 1
            if enemyAttack < 5 and enemyAttack >= 0:
                enemyImage = bowStand
                enemy = pygame.Rect(400+xModifier - enemyPos**1.7/2,300,enemyPos**1.7,enemyPos**1.7)
                enemyScaledImage = pygame.transform.scale(enemyImage, (enemy.width, enemy.height))
                screen.blit(enemyScaledImage, enemy)
                return
            elif enemyAttack < 20 and enemyAttack >= 5:
                enemyImage = bowWindUp1
                enemy = pygame.Rect(400+xModifier - enemyPos**1.7/2,300,enemyPos**1.7,enemyPos**1.7)
                enemyScaledImage = pygame.transform.scale(enemyImage, (enemy.width, enemy.height))
                screen.blit(enemyScaledImage, enemy)
                return
            elif enemyAttack <= 30 and enemyAttack >= 20:
                enemyImage = bowWindUp2
                enemy = pygame.Rect(400+xModifier - enemyPos**1.7/2,300,enemyPos**1.7,enemyPos**1.7)
                enemyScaledImage = pygame.transform.scale(enemyImage, (enemy.width, enemy.height))
                screen.blit(enemyScaledImage, enemy)
                return
            elif enemyAttack <= 35:
                enemyImage = bowAttackImage
                enemy = pygame.Rect(400+xModifier - enemyPos**1.7/2,300,enemyPos**1.7,enemyPos**1.7)
                enemyScaledImage = pygame.transform.scale(enemyImage, (enemy.width, enemy.height))
                screen.blit(enemyScaledImage, enemy)
                if enemyAttack == 31:
                    health -= 1
                    if health < 1:
                        causeOfDeath = "crossbow goblin. \n"
                    if not mute:
                        playerHurtNoise.play()                    
                    damageFlash = True 
                    return
                if enemyAttack == 35:
                    enemyAttack = 0
                return
        elif enemyPos == 29 and (enemyType == 1 or enemyType == 2):
            enemyAttack += 1
            if enemyType == 1:
                if enemyAttack < 10 and enemyAttack >= 0:
                    enemyImage = hammerStand
                    enemy = pygame.Rect(400+xModifier - enemyPos**1.7/2,300,enemyPos**1.7,enemyPos**1.7)
                    enemyScaledImage = pygame.transform.scale(enemyImage, (enemy.width, enemy.height))
                    screen.blit(enemyScaledImage, enemy)
                    return
                elif enemyAttack < 20 and enemyAttack >= 10:
                    enemyImage = hammerWindUp1
                    enemy = pygame.Rect(400+xModifier - enemyPos**1.7/2,300,enemyPos**1.7,enemyPos**1.7)
                    enemyScaledImage = pygame.transform.scale(enemyImage, (enemy.width, enemy.height))
                    screen.blit(enemyScaledImage, enemy)
                    return
                elif enemyAttack < 28 and enemyAttack >= 20:
                    enemyImage = hammerWindUp2
                    enemy = pygame.Rect(400+xModifier - enemyPos**1.7/2,300,enemyPos**1.7,enemyPos**1.7)
                    enemyScaledImage = pygame.transform.scale(enemyImage, (enemy.width, enemy.height))
                    screen.blit(enemyScaledImage, enemy)
                    return
                elif enemyAttack >= 28 and enemyAttack <= 32:
                    enemyImage = hammerWindUp1
                    enemy = pygame.Rect(400+xModifier - enemyPos**1.7/2,300,enemyPos**1.7,enemyPos**1.7)
                    enemyScaledImage = pygame.transform.scale(enemyImage, (enemy.width, enemy.height))
                    screen.blit(enemyScaledImage, enemy)
                    return
                elif enemyAttack <= 40:
                    enemyImage = hammerAttackImage
                    enemy = pygame.Rect(400+xModifier - enemyPos**1.7/2,300,enemyPos**1.7,enemyPos**1.7)
                    enemyScaledImage = pygame.transform.scale(enemyImage, (enemy.width, enemy.height))
                    screen.blit(enemyScaledImage, enemy)
                    if enemyAttack == 33:
                        health -= 2
                        if health < 1:
                            causeOfDeath = "hammer goblin. \n"
                        if not mute:
                            playerHurtNoise.play()                    
                        damageFlash = True
                        if distDownHall % 10 == 0:
                            if currPanelS == 0:
                                currPanelS = len(panelListL)-1
                            else:
                                currPanelS -= 1  
                            if enemySpawn and enemyPos > -5:
                                enemyPos -=1
                            if fireballLaunch:
                                fireballPos -= 1
                            if currPanelT == 0:
                                currPanelT = len(panelListT)-1
                            else:
                                currPanelT -= 1  
                        return
                if enemyAttack == 40:
                    enemyAttack = 0
                return
            elif enemyType == 2:
                if enemyAttack < 5 and enemyAttack >= 0:
                    enemyImage = swordStand
                    enemy = pygame.Rect(400+xModifier - enemyPos**1.7/2,300,enemyPos**1.7,enemyPos**1.7)
                    enemyScaledImage = pygame.transform.scale(enemyImage, (enemy.width, enemy.height))
                    screen.blit(enemyScaledImage, enemy)
                    return
                elif enemyAttack <= 15 and enemyAttack >= 5:
                    enemyImage = swordWindUp
                    enemy = pygame.Rect(400+xModifier - enemyPos**1.7/2,300,enemyPos**1.7,enemyPos**1.7)
                    enemyScaledImage = pygame.transform.scale(enemyImage, (enemy.width, enemy.height))
                    screen.blit(enemyScaledImage, enemy)
                    return
                elif enemyAttack <= 20:
                    enemyImage = swordAttackImage
                    enemy = pygame.Rect(400+xModifier - enemyPos**1.7/2,300,enemyPos**1.7,enemyPos**1.7)
                    enemyScaledImage = pygame.transform.scale(enemyImage, (enemy.width, enemy.height))
                    screen.blit(enemyScaledImage, enemy)
                    if enemyAttack == 16:
                        health -= 1 
                        if health < 1:
                            causeOfDeath = "sword goblin. \n"
                        if not mute:
                            playerHurtNoise.play()                   
                        damageFlash = True 
                        return
                if enemyAttack == 20:
                    enemyAttack = 0
                return
                
        if enemyPos > 0:
            enemyAttack = 0
            if enemyLeft == True:
                if enemyType == 1:
                    enemyImage = hammerLeftImage
                elif enemyType == 2:
                    enemyImage = swordLeftImage
                elif enemyType == 3:
                    enemyImage = bowLeftImage
            else:
                if enemyType == 1:
                    enemyImage = hammerRightImage
                elif enemyType == 2:
                    enemyImage = swordRightImage
                elif enemyType == 3:
                    enemyImage = bowRightImage
            enemy = pygame.Rect(400+xModifier - enemyPos**1.7/2,300,enemyPos**1.7,enemyPos**1.7)
            enemyScaledImage = pygame.transform.scale(enemyImage, (enemy.width, enemy.height))
            screen.blit(enemyScaledImage, enemy)

def magic():
    global fireballLaunch
    global fireballPos
    global enemySpawn
    global enemyPos
    global enemyHealth
    global mana
    global manaRegenerator
    if mana < 10:
        manaRegenerator += 1
        if manaRegenerator == 250:
            mana += 1
            manaRegenerator = 0
    if fireballLaunch == True:
        fireballPos -= 1
        if fireballPos < 1:
            fireballLaunch = False
            fireballPos = 29
            return
        fireballLength = fireballPos ** 1.4
        fireball = pygame.Rect(xFireball - fireballLength/2,yFireball - fireballLength/2,fireballLength,fireballLength)
        fireballScaledImage = pygame.transform.scale(fireballImage, (fireball.width, fireball.height))
        screen.blit(fireballScaledImage, fireball)
        if fireballPos < enemyPos and fireball.colliderect(enemy) and enemySpawn:
            if not mute:
                fireballImpact.play()
                enemyHurt.play()
            enemyHealth -= 1
            if enemyHealth <= 0:
                    enemySpawn = False
                    enemyPos = 0
            fireballLaunch = False
            fireballPos = 29
            enemyDamageUpdate()
            
def swordSlash():
    global attackWindUp
    global attackTimer
    global enemyHealth
    global enemyPos
    global enemySpawn
    global enemyType
    slashPosition = random.randint(1,4)
    if attackWindUp == False:
        attackWindUp = True
        if slashPosition == 1:
            pygame.draw.line(screen, (255,255,255), (mousex - 100, mousey - 150), (mousex + 50, mousey + 150), 10)
        if slashPosition == 2:
            pygame.draw.line(screen, (255,255,255), (mousex + 100, mousey - 150), (mousex - 50, mousey + 150), 10)
        if slashPosition == 3:
            pygame.draw.line(screen, (255,255,255), (mousex, mousey - 150), (mousex, mousey + 150), 10)
        if slashPosition == 4:
            pygame.draw.line(screen, (255,255,255), (mousex - 150, mousey), (mousex + 150, mousey), 10)
        if not mute:
            if enemySpawn and (enemy.collidepoint(mousex,mousey) and ((enemyAttack > 10 and enemyType == 1) or (enemyAttack > 5 and enemyType == 2))) or (enemyType == 3 and enemyPos == 29):
                swordCut.play()
                enemyHurt.play()
            elif enemy.collidepoint(mousex,mousey) and enemyPos == 29:
                swordBlocked.play()
            else:
                swordMiss.play()
        attackTimer = pygame.time.get_ticks()
        if (enemy.collidepoint(mousex,mousey) and ((enemyAttack > 10 and enemyType == 1) or (enemyAttack > 5 and enemyType == 2))): 
            enemyHealth -= 1
            enemyDamageUpdate()
            if enemyHealth <= 0:
                enemySpawn = False
                enemyPos = 0 
        elif enemy.collidepoint(mousex,mousey) and enemyType == 3 and enemyPos == 29: 
            enemyHealth -= 1
            enemyDamageUpdate()
            if enemyHealth <= 0:
                enemySpawn = False
                enemyPos = 0 
                
def enemyDamageUpdate():
    if enemyType == 1 and enemySpawn:
        if enemyAttack < 10 and enemyAttack >= 0 and enemyPos == 29:
            enemyImage = hammerStandDmg
            enemyScaledImage = pygame.transform.scale(enemyImage, (enemy.width, enemy.height))
            screen.blit(enemyScaledImage, enemy)
            return
        elif enemyAttack < 20 and enemyAttack >= 10:
            enemyImage = hammerWindUp1Dmg
            enemyScaledImage = pygame.transform.scale(enemyImage, (enemy.width, enemy.height))
            screen.blit(enemyScaledImage, enemy)
            return
        elif enemyAttack < 30 and enemyAttack >= 20:
            enemyImage = hammerWindUp2Dmg
            enemyScaledImage = pygame.transform.scale(enemyImage, (enemy.width, enemy.height))
            screen.blit(enemyScaledImage, enemy)
            return
        elif enemyAttack <= 35 and enemyPos == 29:
            enemyImage = hammerAttackImageDmg
            enemyScaledImage = pygame.transform.scale(enemyImage, (enemy.width, enemy.height))
            screen.blit(enemyScaledImage, enemy)
            return
        else: 
            if enemyLeft == True:
                enemyImage = hammerLeftImageDmg
            else:
                enemyImage = hammerRightImageDmg
            enemyScaledImage = pygame.transform.scale(enemyImage, (enemy.width, enemy.height))
            screen.blit(enemyScaledImage, enemy)
            return
    if enemyType == 2 and enemySpawn:
        if enemyAttack < 5 and enemyAttack >= 0 and enemyPos == 29:
            enemyImage = swordStandDmg
            enemyScaledImage = pygame.transform.scale(enemyImage, (enemy.width, enemy.height))
            screen.blit(enemyScaledImage, enemy)
            return
        elif enemyAttack < 15 and enemyAttack >= 5:
            enemyImage = swordWindUpDmg
            enemyScaledImage = pygame.transform.scale(enemyImage, (enemy.width, enemy.height))
            screen.blit(enemyScaledImage, enemy)
            return
        elif enemyAttack < 20 and enemyPos == 29:
            enemyImage = swordAttackImageDmg
            enemyScaledImage = pygame.transform.scale(enemyImage, (enemy.width, enemy.height))
            screen.blit(enemyScaledImage, enemy)
            return
        else:
            if enemyLeft == True:
                enemyImage = swordLeftImageDmg
            else:
                enemyImage = swordRightImageDmg
            enemyScaledImage = pygame.transform.scale(enemyImage, (enemy.width, enemy.height))
            screen.blit(enemyScaledImage, enemy)
            return
    if enemyType == 3 and enemySpawn:
        if enemyAttack < 5 and enemyAttack >= 0 and enemyPos >= 15:
            enemyImage = bowStandDmg
            enemyScaledImage = pygame.transform.scale(enemyImage, (enemy.width, enemy.height))
            screen.blit(enemyScaledImage, enemy)
            return
        elif enemyAttack < 20 and enemyAttack >= 5:
            enemyImage = bowWindUp1Dmg
            enemyScaledImage = pygame.transform.scale(enemyImage, (enemy.width, enemy.height))
            screen.blit(enemyScaledImage, enemy)
            return
        elif enemyAttack <= 30 and enemyAttack >= 20:
            enemyImage = bowWindUp2Dmg
            enemyScaledImage = pygame.transform.scale(enemyImage, (enemy.width, enemy.height))
            screen.blit(enemyScaledImage, enemy)
            return
        elif enemyAttack <= 35 and enemyPos >= 15:
            enemyImage = bowAttackImageDmg
            enemyScaledImage = pygame.transform.scale(enemyImage, (enemy.width, enemy.height))
            screen.blit(enemyScaledImage, enemy)
            return
        else:
            if enemyLeft == True:
                enemyImage = bowLeftImageDmg
            else:
                enemyImage = bowRightImageDmg
            enemyScaledImage = pygame.transform.scale(enemyImage, (enemy.width, enemy.height))
            screen.blit(enemyScaledImage, enemy)
            return

def drawLevel():
    global wallLength
    global wallHeight
    global level
    screen.fill([50,50,50])
    floorCeiling()     
    walls()
    if distDownHall > hallLength - 103 and distDownHall < hallLength:
        wallLength = (distDownHall - (hallLength - 98))
        wallHeight = (distDownHall - (hallLength - 98)) * 1.3877
        wallLength = int(wallLength)
        wallHeight = int(wallHeight)
    if distDownHall > hallLength - 98:
        bwScaledImage =  pygame.transform.scale(backWall,(wallLength,wallHeight))
        screen.blit(bwScaledImage, (399-wallLength/2,299-wallHeight/2))
    if distDownHall > hallLength:
        level += 0.5  

def drawPauseMenu():
    global pauseBox
    if pauseBox < screenWidth/5:
        pauseBox += screenWidth/150
    pygame.draw.rect(screen,[0,0,0],[[0,0],[pauseBox,screenHeight]],0)
    pauseTitle = "Menu"
    muteText = "Mute: "+muteState
    screen.blit(TNR20.render(pauseTitle, 1, (255,255,255)), (pauseBox - screenWidth/10 - 25, 50))
    screen.blit(TNR20.render(muteText, 1, (255,255,255)), muteButton)
    
def drawInstructions():
    screen.blit(instructIMG,(0,0))
    if iBackButton.collidepoint(mousex,mousey):
        screen.blit(Castellar.render("Back to Menu", 1, (255,255,255)), iBackButton)
    else:
        screen.blit(Castellar.render("Back to Menu", 1, (0,0,0)), iBackButton)
        
def drawCredits():  
    global creditsPos
    screen.fill([0,38,255])
    if creditsPos < 1000:
        creditsPos += 2
    s1 = "                      Credits"
    s2 = "    ICS 201 Summative Assignment"
    s3 = "             Teodor  Agavriloai"
    s4 = "              Christopher Guay "
    s5 = "                  Richard Liu"
    screen.blit(TNR30.render(s1, 1, (0,0,0)), (170,600 - creditsPos))
    screen.blit(TNR30.render(s2, 1, (0,0,0)), (170,700 - creditsPos))
    screen.blit(TNR30.render(s3, 1, (0,0,0)), (170,800 - creditsPos))
    screen.blit(TNR30.render(s4, 1, (0,0,0)), (170,850 - creditsPos))
    screen.blit(TNR30.render(s5, 1, (0,0,0)), (170,900 - creditsPos))
    screen.blit(TNR30.render("Click to Return to Main Menu", 1, (0,0,0)), (210,1500 - creditsPos))

def drawHighScores():
    screen.fill([0,38,255])
    scores = open('scores.txt', 'r')
    spacing = 0
    lines = [line.strip() for line in open('highscores.txt')]
    try:
        highScore = str(int(float(max(lines))))
    except:
        pass
    screen.blit(TNR30.render("Click to Return to Main Menu  |", 1, (255,255,255)), (40, 60))
    try:
        screen.blit(TNR30.render("High Score: Level " + highScore, 1 , (255,255,255)), (450, 60))
    except:
        pass
    for line in scores:
        line = line.strip("\n")
        spacing += 50
        yPos = 150 + spacing + scroll
        if yPos > 100:
            screen.blit(TNR20.render(line, 1, (255,255,255)), (40, yPos))
    scores.close()

def drawMainMenu():
    screen.blit(mainMenuIMG,(0,0))
    if playButton.collidepoint(mousex,mousey):
        screen.blit(Castellar.render("Play", 1, (255,255,255)), playButton)
    else:
        screen.blit(Castellar.render("Play", 1, (0,0,0)), playButton)
    if instructionsButton.collidepoint(mousex,mousey):
        screen.blit(Castellar.render("Instructions", 1, (255,255,255)), instructionsButton)
    else:
        screen.blit(Castellar.render("Instructions", 1, (0,0,0)), instructionsButton)
    if creditsButton.collidepoint(mousex,mousey):
        screen.blit(Castellar.render("Credits", 1, (255,255,255)), creditsButton)
    else:
        screen.blit(Castellar.render("Credits", 1, (0,0,0)), creditsButton)
    if highScoreButton.collidepoint(mousex,mousey):
        screen.blit(Castellar.render("Highscores", 1, (255,255,255)), highScoreButton)
    else:
        screen.blit(Castellar.render("Highscores", 1, (0,0,0)), highScoreButton)
        
def condition():
    global healing
    global damageFlash
    global levelingUp
    if healing == True:
        screen.fill([255,255,200])
        healing = False
    if damageFlash == True:
        screen.fill([255,0,0])
        damageFlash = False
    pygame.draw.polygon(screen, [0,0,0], [[74,549],[176,549],[176,566],[74,566] ])
    pygame.draw.polygon(screen, [255,0,0], [[75,550],[75 + 10 * health,550],[75 + 10 * health,565],[75,565]])
    screen.blit(conditionFont.render("Health: " +str(health), 1,(255,255,255)),(82,550))
    pygame.draw.polygon(screen, [0,0,0], [[674,549],[776,549],[776,566],[674,566] ])
    pygame.draw.polygon(screen, [0,0,255], [[675,550],[675 + 10 * mana,550],[675 + 10 * mana,565],[675,565]])
    screen.blit(conditionFont.render("Mana: "+ str(mana) , 1,(255,255,255)),(687,550))
    if enemySpawn == True and (enemyType == 2 or enemyType == 3):
        pygame.draw.polygon(screen, [0,0,0],[[324,24],[476,24],[476,41],[324,41]])
        pygame.draw.polygon(screen, [150,0,150],[[325,25],[325 + 50 * enemyHealth,25],[325 + 50 * enemyHealth,40],[325,40]])
        screen.blit(conditionFont.render("Enemy Health: " + str(enemyHealth), 1, (255,255,255)),(330,25))
    elif enemySpawn == True and enemyType == 1:
        pygame.draw.polygon(screen, [0,0,0],[[324,24],[476,24],[476,41],[324,41]])
        pygame.draw.polygon(screen, [150,0,150],[[325,25],[325 + 30 * enemyHealth,25],[325 + 30 * enemyHealth,40],[325,40]])
        screen.blit(conditionFont.render("Enemy Health: " + str(enemyHealth), 1, (255,255,255)),(330,25))
    if levelingUp > 0:
        screen.blit(conditionFont.render("Level " + str(int(level)), 1, (255,255,255)),(375,275))
        levelingUp += 1
        if levelingUp == 100:
            levelingUp = 0
            
def nextLevel():
    global health
    global mana
    global distDownHall
    global hallLength
    global level
    global alpha
    global enemySpawn
    global enemyHealth
    global enemyPos
    global fireballLaunch
    global fireballPos
    global levelingUp
    mana = 10
    distDownHall = 20
    hallLength = random.randint(800,1500)
    if level != 1:
        level += 0.5
    alpha = 0
    enemySpawn = False
    enemyPos = 0
    fireballLaunch = False
    fireballPos = 29
    levelingUp = 1
    drawLevel()
    
def movePlayer():
    global moveForward
    global moveBack
    global distDownHall
    global linePos
    global currPanelS
    global currPanelT
    global enemyPos
    global fireballPos
    if moveForward and enemyPos < 29:
        distDownHall += 5
    elif enemyPos == 29:
        moveForward = False
    if moveBack and distDownHall >= 0:
        distDownHall -= 5
    elif distDownHall <= 0:
        moveBack = False       
    
    if moveForward:    
        if distDownHall % 10 == 0:
            if enemySpawn: #Enemies
                enemyPos += 1
            if fireballLaunch: #Fireball
                fireballPos += 1
            if currPanelS == len(panelListL)-1: #Side Panels
                currPanelS = 0
            else:
                currPanelS += 1
            if currPanelT == len(panelListT)-1: #Top and Bottom Panels
                currPanelT = 0
            else:
                currPanelT += 1
    
    elif moveBack:    
        if distDownHall % 10 == 0: 
            if enemySpawn and enemyPos > -5: #Enemies
                enemyPos -=1
            if fireballLaunch: #Fireball
                fireballPos -= 1
            if currPanelS == 0: #Side Panels
                currPanelS = len(panelListL)-1
            else:
                currPanelS -= 1 
            if currPanelT == 0: #Top and Bottom Panels
                currPanelT = len(panelListT)-1
            else:
                currPanelT -= 1 
                
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN: #Key Downs
            if event.key == K_ESCAPE:
                if level > 0:
                    if paused:
                        paused = False
                        pauseBox = 0
                        pygame.display.set_caption("Super Mega Game of Awesome")
                    elif not paused:
                        paused = True
                        pygame.display.set_caption("Super Mega Game of Awesome: Paused")
            if event.key == K_m:
                if mute:
                    mute = False
                    muteState = "False"
                    pygame.mixer.music.play(-1, 0.0)
                elif not mute:
                    mute = True
                    muteState = "True"
                    pygame.mixer.music.stop()
            if event.key == K_w:
                moveForward = True
                moveBack = False
            if event.key == K_s:
                moveBack = True
                moveForward = False
            if event.key == K_q:
                if mana > 1 and health < 10:
                    mana -= 2
                    health += 1
                    healing = True
                    if mute == False:
                        heal.play()
                else:
                    if mute == False:
                        outOfMana.play()
        if event.type == KEYUP:#Key Ups
            if event.key == K_w:
                moveForward = False
            if event.key == K_s:
                moveBack = False
        if event.type == MOUSEMOTION:#Mouse Movements
            mousex = event.pos[0]
            mousey = event.pos[1]                  
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1: #Left Click
                if level != 0 and not paused:
                    slash = True
                if paused and muteButton.collidepoint(mousex,mousey):
                    if mute:
                        mute = False
                        muteState = "False"
                        pygame.mixer.music.play(-1, 0.0)
                    elif not mute:
                        mute = True
                        muteState = "True"
                        pygame.mixer.music.stop()
                if level == 0 and playButton.collidepoint(mousex,mousey):
                    level = 1
                    music()
                    nextLevel()
                    levelingUp = 1 
                if level == 0 and instructionsButton.collidepoint(mousex,mousey):
                    level = -1
                if level == 0 and creditsButton.collidepoint(mousex,mousey):
                    level = -2
                if level == 0 and highScoreButton.collidepoint(mousex,mousey):
                    level = -3
                elif level == -2 and pygame.mouse.get_pressed:
                    creditsPos = 0
                    level = 0
                elif level == -3 and pygame.mouse.get_pressed:
                    level = 0
                if level == -1 and iBackButton.collidepoint(mousex, mousey):
                    level = 0
            if event.button == 3: #Right Click
                if level != 0 and not paused and not fireballLaunch: 
                    if mana != 0:
                        fireballLaunch = True
                        fireballSound = random.randint(1,2)
                        if not mute:
                            if fireballSound == 1:
                                fireballLaunch1.play()
                            else:
                                fireballLaunch2.play()
                        mana -= 1
                    else:
                        if not mute:
                            outOfMana.play()
                        
                    xFireball = mousex
                    yFireball = mousey
            if event.button == 4:
                scroll -= 50
            if event.button == 5:
                scroll += 50

    if paused:
        muteButton = pygame.Rect(pauseBox - screenWidth/25 * 4, 100, screenWidth/25 * 4, 30)
        drawPauseMenu()
    else:
        if level == 0: #Main Menu
            drawMainMenu()
        elif level == -1:
            drawInstructions()
        elif level == -2:
            drawCredits()
        elif level == -3:
            drawHighScores()
        elif level % 0.5 == 0 and level % 1 != 0:
            if alpha < 150:    
                alpha += 1
            endScreen.fill((0,0,0,alpha))    
            screen.blit(endScreen,(0,0))
            if alpha >= 150:
                nextLevel()
        elif health < 1:
            health = 10
            scores = open('scores.txt', "a")
            scores.write("On " + time.strftime("%c") + " you made it to Level " + str(int(level)) + " before being slain by a " + causeOfDeath)
            scores.close()
            highScores = open('highscores.txt', "a")
            highScores.write(str(level) + "\n")
            highScores.close()
            level = 0
            music()
        else:           
            drawLevel()
            movePlayer()
            if distDownHall > hallLength - 98:
                spawnEnemies = False
            else:
                spawnEnemies = True
            enemyGen()
            magic()
            if pygame.time.get_ticks() - attackTimer > 500: #Sword Slash Cooldown
                attackWindUp = False
            if slash == True:
                swordSlash()
                slash = False
            condition()
            
    pygame.display.flip()
    mainClock.tick(30)