#1 - Import library
import math
import random
import pygame
from pygame.locals import *
import time
import os
import sys
os.environ['SDL_VIDEO_CENTERED'] = '1' # center window
pygame.init()
#-----------------------------------Screen Scaner -------------------------------------#
resolutionArray = pygame.display.list_modes()
#2 - Initialize Values
pygame.mixer.init()

clock = pygame.time.Clock() # Initialize clock
clock.tick(30) # Set Start FPS

displayWithGame = resolutionArray[0][0] # Display width
displayHeightGame = resolutionArray[0][1] # Display height
fullScreen = 0 # 0 - no / 1 - yes
level = 1 # 1 - low  # 2 - medium  # 3 - hard

frameRate = 30 # 30 or 60

pygame.display.set_caption('Defend ShapirTown') # Window Name

# Resolution Length to display in launcher ----
if len(resolutionArray) >= 3:
    resolutionLen = 3
else:
    resolutionLen = len(resolutionArray)
#----------------------------------------------

# colors
orangeBackground = (245, 147, 66)
orangeAmmoEmpty = (255, 222, 176)
greenPlay = (51, 166, 82)
greenPlayActive = (85, 224, 123)
grayBought = (77, 77, 77)
white = (255, 255, 255)
black = (0, 0, 0)

lightGreen = (0,162,0)
lightGreenActive = (0,234,0)

lightRed = (162,0,0)
lightRedActive = (234,0,0)

lightYellow = (188, 199, 32)
lightYellowActive = (229, 245, 82)

lightGray = (160,160,160)
lightGrayActive = (192,192,192)
SuperLightGrayActive = (230,230,230)
#yes/noArray to fullScreen Label
fullScreenYesNoArray = ["Nie","Tak"]
#colorArray to LVL Label
levelColorArray = [[lightGreen,lightGreenActive],[lightYellow,lightYellowActive],[lightRed,lightRedActive]]
#nameArray to LVL Label
levelNameArray = ["Łatwy","Średni","Trudny"]
#positionArray to LVL Label
levelPositionArray = [[150,182],[268,180],[388,182]]
#positionArray to frameRate label
frameRatePositionArray = [['30 FPS',274],['60 FPS',390]]
#3 - Functions
#https://stackoverflow.com/questions/4183208/how-do-i-rotate-an-image-around-its-center-using-pygame
def blitRotate(surf, image, pos, originPos, angle):
    # calcaulate the axis aligned bounding box of the rotated image
    w, h = image.get_size()
    box = [pygame.math.Vector2(p) for p in [(0, 0), (w, 0), (w, -h), (0, -h)]]
    box_rotate = [p.rotate(angle) for p in box]
    min_box = (min(box_rotate, key=lambda p: p[0])[0], min(box_rotate, key=lambda p: p[1])[1])
    max_box = (max(box_rotate, key=lambda p: p[0])[0], max(box_rotate, key=lambda p: p[1])[1])
    # calculate the translation of the pivot
    pivot = pygame.math.Vector2(originPos[0], -originPos[1])
    pivot_rotate = pivot.rotate(angle)
    pivot_move = pivot_rotate - pivot
    # calculate the upper left origin of the rotated image
    origin = (pos[0] - originPos[0] + min_box[0] - pivot_move[0], pos[1] - originPos[1] - max_box[1] + pivot_move[1])
    # get a rotated image
    rotated_image = pygame.transform.rotate(image, angle)
    # rotate and blit the image
    surf.blit(rotated_image, origin)
#-------------------------------------------------------------------------------------------------------
# Show text on window, in set font, value of string, position x and y
def printTextOn(screen,font,string, x, y):
    string = str(string)
    text = font.render(string, True, black)
    textPosition = (x,y)
    screen.blit(text,textPosition)
def button(screen,color,colorActive,x,y,w,h,action=None,active=False):
    #Global
    global displayWithGame
    global displayHeightGame
    global fullScreen
    global level
    global frameRate
    global option
    #Hooks
    mousePosition = pygame.mouse.get_pos()  # to Mouse
    click = pygame.mouse.get_pressed() # to Click
    if active:
        pygame.draw.rect(screen, colorActive, (x, y, w, h))
    else:
        if x + w > mousePosition[0] > x and y + h > mousePosition[1] > y:
            pygame.draw.rect(screen, colorActive, (x, y, w, h))
            if click[0] == 1 and action != None:
                try:
                    if action[0] == 'fullscreen':
                        fullScreen = action[1]
                    elif action[0] == 'level':
                        level = action[1]
                    elif action[0] == 'frameRate':
                        frameRate = action[1] * 30
                except:
                    if action == 0 or action == 1 or action == 2:
                        displayWithGame = resolutionArray[action][0]
                        displayHeightGame = resolutionArray[action][1]

                    else:
                        action()
        else:
            pygame.draw.rect(screen, color, (x, y, w, h))
#4 - Main Loops
def launcher():
    font = pygame.font.Font(None, 24) # set Font
    #Initialize Launcher
    displayWidth, displayHeight = 500, 350 # Display Window 500x350
    gameScreen = pygame.display.set_mode((displayWidth, displayHeight)) # Hook to window
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)
        # Set  Background
        gameScreen.fill(orangeBackground)
        # Options Label
        printTextOn(gameScreen, font, 'Opcje:', 234, 32)
        # Resolution Label
        printTextOn(gameScreen, font, 'Rozdzielczość gry (aktualna):', 50, 54)
        # FullScreen Label
        printTextOn(gameScreen, font, 'FullScreen:', 50, 134)
        # Level Label
        printTextOn(gameScreen, font, 'Poziom:', 50, 180)
        # Frame Rate
        printTextOn(gameScreen, font, 'Ilosc klatek na sekunde:', 50, 222)
        mousePosition = pygame.mouse.get_pos()  # hook to mouse
        #Buttons
        # if X+Width > mousePosition[0] > X and Y+Height > mousePosition[1] > Y   =>   mouse is in button
        # Button ( hookToWindow,color,ActiveColor,x,y,width,height,actionName,Active?
        #Resolution
        #Actual:
        resolution = "%sx%s" % (displayWithGame, displayHeightGame)
        printTextOn(gameScreen, font, resolution, 300, 54)
        for i in range(resolutionLen):
            resolution = "%sx%s" % (resolutionArray[i][0], resolutionArray[i][1])
            resolutionX = 80+(i*120)
            button(gameScreen, lightGray,lightGrayActive, resolutionX, 84, 100, 24, i, False)
            printTextOn(gameScreen, font, resolution, 86 + (i * 120), 89)
        #FullScreen
        for i in range(2):
            if fullScreen == i:
                button(gameScreen,lightGray,SuperLightGrayActive, 174+(i*120),130,100,24,('fullscreen',i),True)
            else:
                button(gameScreen, lightGray, SuperLightGrayActive, 174 + (i * 120), 130, 100, 24, ('fullscreen', i),False)
            printTextOn(gameScreen, font,fullScreenYesNoArray[i],208+(i*120),135)
        #Level
        for i in range(1, 4):
            if level == i:
                button(gameScreen, levelColorArray[i-1][0], levelColorArray[i-1][1], 124+((i-1)*120), 178, 100, 24, ("level",i), True)
            else:
                button(gameScreen, levelColorArray[i-1][0], levelColorArray[i-1][1], 124 + ((i-1)*120), 178, 100, 24, ("level", i),False)
            printTextOn(gameScreen, font, levelNameArray[i-1], levelPositionArray[i-1][0], levelPositionArray[i-1][1])
        #Frame Rate
        for i in range(1,3):
            if frameRate == i*30:
                button(gameScreen, lightGray, SuperLightGrayActive, 250+((i-1)*116), 218, 100, 24, ('frameRate',i), True)
            else:
                button(gameScreen, lightGray, SuperLightGrayActive, 250+((i-1)*116), 218, 100, 24, ('frameRate',i), False)
            printTextOn(gameScreen, font, frameRatePositionArray[i-1][0], frameRatePositionArray[i-1][1], 222)
        #Play
        button(gameScreen,greenPlay,greenPlayActive, 200, 270, 100, 24, game, False)
        printTextOn(gameScreen, font, 'Graj', 234, 274)
        button(gameScreen, lightRed, lightRedActive, 200, 300, 100, 24, quit, False)
        printTextOn(gameScreen, font, 'Wyjdź', 228, 304)

        pygame.display.update()
        clock.tick(frameRate)
def game():
    #Initialize Game
    global displayHeightGame
    if fullScreen == 1:
        gameScreen = pygame.display.get_surface()
        flags = gameScreen.get_flags()
        bits = gameScreen.get_bitsize()
        pygame.display.quit()
        pygame.display.init()
        gameScreen = pygame.display.set_mode((displayWithGame, displayHeightGame), flags ^ FULLSCREEN, bits) #fullScreen
        yScale = round((displayHeightGame/1080),2)
    else:
        if displayHeightGame == resolutionArray[0][1]:
            displayHeightGame -= 120
        gameScreen = pygame.display.set_mode((displayWithGame, displayHeightGame)) #widnowMode
        yScale = round(((displayHeightGame)/1080), 2)
    xScale = round((displayWithGame/1920),2)
    font = pygame.font.Font(None, int(24*xScale)) # set Font
    shopFont = pygame.font.Font(None, int(72 * xScale))  # set Font for shop
    #CASTLE-------------------------------------------------
    xCastle = int(342*xScale)
    yCastle = int(800*yScale)
    castle = pygame.image.load("resources/images/TowerToGame.png") # 342x799
    castle = pygame.transform.scale(castle, (xCastle, yCastle))
    CastleRect = pygame.Rect(castle.get_rect())
    CastleRect.left = 0
    CastleRect.top = int(180 * yScale)
    #------------------------------------------------------#
    #MAP----------------------------------------------------
    map = pygame.image.load("resources/images/map.png") #1920x1080
    map = pygame.transform.scale(map, (displayWithGame, displayHeightGame))
    #------------------------------------------------------#
    #Cloud--------------------------------------------------
    xCloud = int(329 * xScale)
    yCloud = int(99 * yScale)
    cloud = pygame.image.load("resources/images/cloud.png") # 329x99
    cloud = pygame.transform.scale(cloud, (xCloud, yCloud))
    cloudsArray = [] # Clouds Array
    # -------------------------------------------------------
    #Player--------------------------------------------------
    xPlayer = int(97 * xScale)
    yPlayer = int(183 * yScale)
    player = pygame.image.load("resources/images/player.png")  # 97x183
    player = pygame.transform.scale(player, (xPlayer, yPlayer))
    #Shop-----------------------------------------------------
    shopSquare = pygame.image.load("resources/images/shop.png")  # 500x500
    shopSquare = pygame.transform.scale(shopSquare, (displayWithGame, displayHeightGame))
    #Efects --------------------------------------------------
    #Blood
    xBlood = int(40 * xScale)
    yBlood = int(40 * yScale)
    blood = pygame.image.load("resources/images/blood.png")  # 20x20
    blood = pygame.transform.scale(blood, (xBlood, yBlood))
    #Weapons -------------------------------------------------
    throwedWeapon = [] # Array of throwed weapons
    #FlyEnemySShot
    throwedByEnemy = [] # Array of throwed shoot by enemy
    #smallShuriken #0
    xSmallShuriken = int(46 * xScale)
    ySmallShuriken = int(49 * yScale)
    smallShuriken = pygame.image.load("resources/images/shuriken.png") #46x49
    smallShuriken = pygame.transform.scale(smallShuriken, (xSmallShuriken, ySmallShuriken))
    #x,y,image,damage
    smallShurikenArray = [xSmallShuriken,ySmallShuriken,smallShuriken,12,'smallShuriken']
    #lightningShuriken #1
    xlightningShuriken = int(46 * xScale)
    ylightningShuriken = int(49 * yScale)
    lightningShuriken = pygame.image.load("resources/images/lightningShuriken.png")  # 46x49
    lightningShuriken = pygame.transform.scale(lightningShuriken, (xlightningShuriken, ylightningShuriken))
    # x,y,image,damage
    lightningShurikenArray = [xlightningShuriken, ylightningShuriken, lightningShuriken, 24,'lightningShuriken']
    #ActualyWeapon
    actualyWeapon = [smallShurikenArray]
    #AllWeaponArray
    availableWeaponArray = [smallShurikenArray,lightningShurikenArray]
    #Bought Weapons
    boughtWeaponsArray = ['smallShuriken']
    def priceWeapon(name):
        switcher = {
                            #Price #Description
            'smallShuriken': [10,'Mały Shuriken'],
            'lightningShuriken': [500,"Elektryczny Shuriken"],
        }
        return switcher.get(name)
    #Enemy for keep resped mob
    enemyArray = []
    # Hoshigaki
    xHoshigaki = int(162 * xScale)
    yHoshigaki = int(227 * yScale)
    hoshigaki = [pygame.image.load("resources/images/hoshigaki.png"),pygame.image.load("resources/images/hoshigakiWalk.png")]  # 162x227
    hoshigaki = [pygame.transform.scale(hoshigaki[0], (xHoshigaki, yHoshigaki)),pygame.transform.scale(hoshigaki[1], (xHoshigaki, yHoshigaki))]
    #X,Y,Image1,Image2,WalkNumber,HP
    hoshigakiArray = [xHoshigaki,yHoshigaki,hoshigaki[0],hoshigaki[1],0,50*level,'hoshigaki']
    # Hidan
    xHidan = int(162 * xScale)
    yHidan = int(227 * yScale)
    hidan = [pygame.image.load("resources/images/hidan.png"),pygame.image.load("resources/images/hidanWalk.png")]  # 162x227
    hidan = [pygame.transform.scale(hidan[0], (xHidan, yHidan)),pygame.transform.scale(hidan[1], (xHidan, yHidan))]
    # X,Y,Image1,Image2,WalkNumber,HP
    hidanArray = [xHidan, yHidan, hidan[0], hidan[1], 0, 100*level,'hidan']
    # Deidara
    xDeidara = int(229 * xScale)
    yDeidara = int(220 * yScale)
    deidara = [pygame.image.load("resources/images/deidara.png"),pygame.image.load("resources/images/deidaraWalk.png")]
    deidara = [pygame.transform.scale(deidara[0], (xDeidara, yDeidara)),pygame.transform.scale(deidara[1], (xDeidara, yDeidara))]
    # X,Y,Image1,Image2,WalkNumber,HP
    deidaraArray = [xDeidara, yDeidara, deidara[0], deidara[1], 0, 150 * level,'deidara']
    # Deidara Boomb 87 x 68
    xDeidaraBoomb = int(87 * xScale)
    yDeidaraBoomb = int(68 * yScale)
    deidaraBoomb = pygame.image.load("resources/images/deidaraBomb.png")
    deidaraBoomb = pygame.transform.scale(deidaraBoomb, (xDeidaraBoomb, yDeidaraBoomb))
    deidaraBoombArray = [xDeidaraBoomb,yDeidaraBoomb,deidaraBoomb,2,'deidaraboomb']
    #BoomImage
    xBoom = int(69 * xScale)
    yBoom = int(69 * yScale)
    boom = pygame.image.load("resources/images/boom.png")
    boom = pygame.transform.scale(boom, (xBoom, yBoom))
    # Available enemy #
    availableEnemyArray = [hoshigakiArray,hidanArray,deidaraArray]
    #timer
    timer = 0
    #Helth Point
    maxHP = 100
    HP=100
    #Ammo
    setReloadTime = 1*level # 1 low , 2 medium , 3 hard
    maxAmmo = [10]
    ammo = 10
    ammoReload = False
    reloadTimer = False
    reloadStart = 0
    #Keyboard
    # R = 0, Q = 1
    keys = [False,False]
    #Waves
    waves = [1]
    #LEVELS
    def levelRender(waves,level,frameRate):
        switcher = {
            # Available enemy #
            #0 hoshigaki[50*lvl] #1 hidan[100*lvl] #2 deidara[150*lvl]
            #Waves: 0[How Many Type Mobs] 1[timeToResp] 2[Count Mobs] [3[Mob] 4[Many] 5[Mob] 6[Many]............
            1: [1, int((5*frameRate)/level), 4*level,0,4*level],
            2: [1, int((3*frameRate)/level), 7*level,0,7*level],
            3: [2, int((4*frameRate)/level), 8*level,0,4*level,1,4*level],
            4: [1,int((2*frameRate)/level), 10*level,0,10*level],
            5: [2, int((3*frameRate)/level), 11*level,2,1*level,1,10*level],
            6: [3, int((3*frameRate)/level), 17*level,0,5*level,2,2*level,1,10*level],
            7: [3, int((2*frameRate)/level), 19*level,0,5*level,2,4*level,1,10*level],
            8: [3, int((3*frameRate)/level), 17*level,2,1*level,1,15*level,2,1*level],
            9: [4, int((4*frameRate)/level), 23*level,2,1*level,0,10*level,2,2*level,1,10*level],
            10: [5, int((4*frameRate)/level), 27*level,2,1*level,0,10*level,2,2*level,1,10*level,2,4*level],
            11: [4, int((3*frameRate)/level), 30*level,2,3*level,1,12*level,2,3*level,1,12*level],
            12: [5, int((3*frameRate)/level), 42*level,2,4*level,1,15*level,2,4*level,1,15*level,2,4*level]
            #12: [0,0,0,0,0]
        }
        return switcher.get(waves)
    howManyType = [0] # Type Mobs
    countMob = [0] # Killed Mobs per Waves
    eachMob = [0] # Killed Mobs per Waves for Type
    shop = [False] # Finish Waves
    #Bonuses
          #Bonus DMG
    bonuses = [0]
    #Skils
          # Freez Enemys
    freezEnemysReload = 0
    freezEnemysWorks = 0
    xFreezEnemy = int(80 * xScale)
    yFreezEnemy = int(80 * yScale)
    freezEnemy = pygame.image.load("resources/images/freezEnemy.png") # 100x100
    freezEnemy = pygame.transform.scale(freezEnemy, (xFreezEnemy, yFreezEnemy))
    skills = {}
    #Moeney
    money = [0]
    def buttonInGame(gameScreen, color, x, y, w, h, action=None, typeQuery=None, value=None, cost=None):
        mousePosition = pygame.mouse.get_pos()  # to Mouse
        click = pygame.mouse.get_pressed()  # to Click
        if x + w > mousePosition[0] > x and y + h > mousePosition[1] > y:
            if click[0] == 1 and action != None:
                if typeQuery == 'skill':
                    if action not in skills:
                        if money[0] >= cost:
                            money[0] -= cost
                            skills[action] = value
                elif typeQuery == 'upgrade':
                    if action == 'dmg':
                        if money[0] >= cost:
                            money[0] -= cost
                            bonuses[0] += value
                            pygame.time.wait(100)
                    elif action == 'maxAmmo':
                        if money[0] >= cost:
                            money[0] -=cost
                            maxAmmo[0] += value
                            pygame.time.wait(100)
                elif typeQuery == 'weapon':
                    if value[4] not in boughtWeaponsArray:
                        boughtWeaponsArray.append(value[4])
                    if money[0] >= cost:
                        money[0] -= cost
                        actualyWeapon[0] = value
                elif typeQuery == 'finish':
                    waves[0] += 1
                    countMob[0] = 0
                    eachMob[0] = 0
                    howManyType[0] = 0
                    shop[0] = False
                elif typeQuery == 'fin':
                    action()
        pygame.draw.rect(gameScreen, color, (x, y, w, h))

    #If hp < 0
    fin = True;
    xLose = int(1920 * xScale)
    yLose = int(1080 * yScale)
    lose = pygame.image.load("resources/images/lose.png")
    lose = pygame.transform.scale(lose, (xLose, yLose))
    xWin = int(1920 * xScale)
    yWin = int(1080 * yScale)
    win = pygame.image.load("resources/images/win.png")
    win = pygame.transform.scale(win, (xWin, yWin))
    #Music
    hit = pygame.mixer.Sound("resources/audio/enemy.wav")
    explode = pygame.mixer.Sound("resources/audio/explode.wav")
    hit.set_volume(0.05)
    explode.set_volume(0.05)
    #pygame.mixer.music.load('resources/audio/')
    #pygame.mixer.music.play(-1, 0.0)
    #pygame.mixer.music.set_volume(0.10)
    while True:
        gameScreen.blit(map, (0, 0))
        gameScreen.blit(castle, (0, int(180 * yScale)))
        #---------------------------------------------------------------------------
        # Cloud Rendering -------------------------------
        if len(cloudsArray) == 0 or cloudsArray[0][2] == (displayWithGame - cloudsArray[0][0] - int(displayWithGame/5)):
            scaleCloud = random.randrange(6,11)/10
            positionCloud = random.randrange(20,61)
            cloudsArray.insert(0,[(int(xCloud*scaleCloud)),(int(yCloud*scaleCloud)),displayWithGame,positionCloud]) # xCloud yCloud xPositionCloud yPositionCloud
        for cloudObject in cloudsArray:
            cloudObject[2]-=1
            printCloud = pygame.transform.scale(cloud, (cloudObject[0], cloudObject[1]))
            gameScreen.blit(printCloud, (cloudObject[2], cloudObject[3]))
            if cloudObject[2] == -1* cloudObject[0]:
                cloudsArray.pop()
        #------------------------------------------------
        #HP BAR->
        button(gameScreen, lightRed, lightRed, int(20 * xScale), int(120 * yScale), int(300 * xScale), int(30 * yScale))
        button(gameScreen, lightGreen, lightGreen, int(20 * xScale), int(120 * yScale),int((300 * xScale) - (((300 * xScale) / maxHP) * (maxHP - HP))), int(30 * yScale))
        printTextOn(gameScreen, font, 'Życie: ', int(300 * xScale) - int(180 * xScale), int(124 * yScale))
        printTextOn(gameScreen, font, int(HP), int(300 * xScale) - int(114 * xScale), int(126 * yScale))
        #Ammo BAR->
        if ammoReload:
            button(gameScreen, orangeAmmoEmpty, orangeAmmoEmpty, int(20 * xScale), int(90 * yScale), int(300 * xScale),int(30 * yScale))
            button(gameScreen, lightYellow, lightYellow, int(20 * xScale), int(90 * yScale),int(0 + ((int(300 * xScale)/setReloadTime) * int(reloadStart/frameRate))), int(30 * yScale))

            printTextOn(gameScreen, font, 'Przeładowywanie(s):', int(300 * xScale) - int(240 * xScale), int(94 * yScale))
            printTextOn(gameScreen, font, setReloadTime-int(reloadStart/frameRate), int(300 * xScale) - int(60 * xScale), int(96 * yScale))
        else:
            button(gameScreen, orangeAmmoEmpty, orangeAmmoEmpty, int(20 * xScale), int(90 * yScale), int(300 * xScale), int(30 * yScale))
            button(gameScreen, lightYellow, lightYellow, int(20 * xScale), int(90 * yScale),int((300 * xScale) - (((300 * xScale) / maxAmmo[0]) * (maxAmmo[0] - ammo))), int(30 * yScale))
            printTextOn(gameScreen, font, 'Amunicja: ', int(300 * xScale) - int(180 * xScale), int(94 * yScale))
            printTextOn(gameScreen, font, ammo, int(300 * xScale) - int(94 * xScale), int(96 * yScale))
        #Money Bar INGAME ->
        printTextOn(gameScreen, font, 'Złoto: ', int(300 * xScale) - int(180 * xScale), int(64 * yScale))
        printTextOn(gameScreen, font, int(money[0]), int(300 * xScale) - int(94 * xScale), int(66 * yScale))
        # Player Rendering ------------------------------
        gameScreen.blit(player, (int(xCastle - (120 * xScale)), int(380 * yScale)))
        # Quit Render for fullScreen
        if fullScreen == 1:
            buttonInGame(gameScreen, lightRed, 0, displayHeightGame-int(60*yScale), 100, 60,quit, 'fin')
            printTextOn(gameScreen, font, 'Wyjdz', int(20 * xScale), displayHeightGame-int(34*yScale))
        # Skills Rendering
        if 'freezEnemy' in skills:
            if freezEnemysReload == 0:
                gameScreen.blit(freezEnemy, (int(88*xScale), int(360 * yScale)))
                printTextOn(gameScreen, font, 'Q', int(88*xScale), int(360 * yScale))
            else:
                gameScreen.blit(freezEnemy, (int(88 * xScale), int(360 * yScale)))
                printTextOn(gameScreen, font, 'Q', int(88 * xScale), int(360 * yScale))
                button(gameScreen, lightRed, lightRed, int(88 * xScale), int(360 * yScale), int(80 * xScale),int(80 * yScale) - int((int(80 * yScale)/(30*frameRate))*((30*frameRate)-freezEnemysReload ))) # X do poprawienia
        # Throw Rendering -------------------------------
        if len(throwedByEnemy) > 0:
            for shoot in throwedByEnemy:
                if freezEnemysWorks == 0:
                    velx = math.cos(shoot[0]) * 10
                    vely = math.sin(shoot[0]) * 10
                    shoot[1] += velx
                    shoot[2] += vely
                blitRotate(gameScreen, shoot[3][2], (shoot[1], shoot[2]), (shoot[3][0] // 2, shoot[3][1] // 2),shoot[4])
        if len(throwedWeapon) > 0:
            for shoot in throwedWeapon:
                # Line to, x,y, weapon[x,y,image,damage], angle
                velx = math.cos(shoot[0]) * 25
                vely = math.sin(shoot[0]) * 25
                shoot[1] += velx
                shoot[2] += vely
                blitRotate(gameScreen, shoot[3][2], (shoot[1], shoot[2]),(shoot[3][0] // 2, shoot[3][1] // 2), shoot[4])
                shoot[4] += (frameRate)
                if shoot[1] < -1 * shoot[3][0] or shoot[1] > displayWithGame + shoot[3][0] or shoot[2] < -1*shoot[3][1] or shoot[2] > displayWithGame + shoot[3][1]:
                    throwedWeapon.remove(shoot)
        # -----------------------------------------------
        # Enemy Rendering
        # adding
        # Waves: 0[How Many Type Mobs] 1[timeToResp] 2[Count Mobs] [3[Mob] 4[Many] 5[Mob] 6[Many]............
        actualy = levelRender(waves[0],level,frameRate)
        if countMob[0] != actualy[2]:
            if actualy[0] > howManyType[0]:
                if eachMob[0] != actualy[4+(howManyType[0]*2)]:
                    if timer % actualy[1] == 0:
                        # resp Mob
                        # x,y,image1,image2,walkNumber,health
                        if availableEnemyArray[actualy[3+(howManyType[0]*2)]][6] == 'deidara':
                            enemyArray.append(
                                [displayWithGame,
                                 int(130 * yScale),
                                 availableEnemyArray[actualy[3 + (howManyType[0] * 2)]][2],
                                 availableEnemyArray[actualy[3 + (howManyType[0] * 2)]][3],
                                 availableEnemyArray[actualy[3 + (howManyType[0] * 2)]][4],
                                 availableEnemyArray[actualy[3 + (howManyType[0] * 2)]][5] + (10 * waves[0]),
                                 'fly'
                                 ]
                            )
                        else:
                            enemyArray.append(
                                [displayWithGame,
                                 displayHeightGame - (int(338 * yScale)),
                                 availableEnemyArray[actualy[3+(howManyType[0]*2)]][2],availableEnemyArray[actualy[3+(howManyType[0]*2)]][3],
                                 availableEnemyArray[actualy[3+(howManyType[0]*2)]][4],availableEnemyArray[actualy[3+(howManyType[0]*2)]][5]+(10*waves[0]),
                                 'ground'
                                 ]
                            )
                        eachMob[0]+=1
                else:
                    eachMob[0] = 0
                    howManyType[0] += 1
        else:
            shop[0] = True
            while shop[0]:
                gameScreen.blit(shopSquare, (0, 0))
                printTextOn(gameScreen, shopFont, int(money[0]), displayWithGame-int(300*xScale), displayHeightGame-int(118*yScale))
                #- drawing Buttons -#
                #Skills
                if 'freezEnemy' not in skills:
                    buttonInGame(gameScreen, lightGreen, int(148*xScale),int(200*yScale) ,308, 60,'freezEnemy','skill',5*frameRate,250)
                    printTextOn(gameScreen, font, 'Zamrożenie przeciwników(250 Złota)', int(160 * xScale), int(224 * yScale))
                else:
                    buttonInGame(gameScreen, grayBought, int(148 * xScale), int(200 * yScale), 308, 60)
                    printTextOn(gameScreen, font, 'Zakupione: Zamrożenie przeciwników', int(160 * xScale),int(224 * yScale))
                #Upgrades
                #Bonus DMG
                buttonInGame(gameScreen, lightGreen, int(796 * xScale), int(200 * yScale), 308, 60, 'dmg','upgrade', 5, 160*((bonuses[0]/5)+1))
                printTextOn(gameScreen, font, 'Bonus do obrażeń +5, Koszt:  '+str(int(160*((bonuses[0]/5)+1))), int(814 * xScale),int(214 * yScale))
                printTextOn(gameScreen, font, 'Aktualna wartość dodatkowa: ['+str(bonuses[0])+']', int(814 * xScale), int(240 * yScale))
                #MaxAmmo
                buttonInGame(gameScreen, lightGreen, int(796 * xScale), int(300 * yScale), 308, 60, 'maxAmmo', 'upgrade', 1,50+(10*int(maxAmmo[0]-10)))
                printTextOn(gameScreen, font, 'Maksymalna amunicja +1, Koszt: ' + str(50+(10*int(maxAmmo[0]-10))),int(814 * xScale), int(314 * yScale))
                printTextOn(gameScreen, font, 'Maksymalna amunicja: [' + str(maxAmmo[0]) + ']',int(814 * xScale), int(340 * yScale))
                #Weapons
                for i in enumerate(availableWeaponArray):
                    thisWeapon = priceWeapon(i[1][4])
                    gameScreen.blit(i[1][2], (int(1400*xScale),int( (210*yScale)+(120*i[0]*yScale))))
                    if i[1][4] in boughtWeaponsArray:
                        #(gameScreen, color, x, y, w, h, action=None, typeQuery=None, value=Tablica broni, cost=None)
                        buttonInGame(gameScreen, grayBought, int(1500*xScale),int( (200*yScale)+(120*i[0]*yScale)),308,60,i[1][4],'weapon',i[1],0)
                        printTextOn(gameScreen, font, thisWeapon[1]+', Obrażenia['+str(i[1][3])+']', int(1514*xScale),int( (210*yScale)+(120*i[0]*yScale)))
                        if actualyWeapon[0][4] == i[1][4]:
                            printTextOn(gameScreen, font, 'Aktywna', int(1620*xScale),int( (242*yScale)+(120*i[0]*yScale)))
                        else:
                            printTextOn(gameScreen, font, 'Zmień', int(1620 * xScale),int((242 * yScale) + (120 * i[0] * yScale)))
                    else:
                        buttonInGame(gameScreen, lightGreen, int(1500 * xScale),int((200 * yScale) + (120 * i[0] * yScale)), 308, 60, i[1][4], 'weapon', i[1], thisWeapon[0])
                        printTextOn(gameScreen, font, thisWeapon[1]+', Obrażenia['+str(i[1][3])+']', int(1514 * xScale),int((210 * yScale) + (120 * i[0] * yScale)))
                        printTextOn(gameScreen, font, 'Koszt:  '+str(thisWeapon[0]), int(1620 * xScale),int((242 * yScale) + (120 * i[0] * yScale)))
                #Finish
                buttonInGame(gameScreen, grayBought, (displayWithGame//2) - int(140 * xScale), displayHeightGame - int(130 * yScale), 308, 60,'','finish')
                printTextOn(gameScreen, font, 'Następna fala', (displayWithGame//2) - int(40 * xScale),displayHeightGame - int(106 * yScale))
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit(0)
                pygame.display.update()
                clock.tick(frameRate)
            ammo = maxAmmo[0]
            if waves[0] == 13:
                while fin:
                    gameScreen.blit(win, (0, 0))
                    # Play Again
                    button
                    buttonInGame(gameScreen, lightGreen, int(400 * xScale), displayHeightGame - int(350 * yScale), 308,60, launcher, 'fin')
                    printTextOn(gameScreen, font, 'Tak', int(528 * xScale), displayHeightGame - int(330 * yScale))
                    buttonInGame(gameScreen, lightRed, int(1300 * xScale), displayHeightGame - int(350 * yScale), 308,60, quit, 'fin')
                    printTextOn(gameScreen, font, 'Nie', int(1452 * xScale), displayHeightGame - int(330 * yScale))
                    # Quit
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            exit(0)
                    pygame.display.update()
                    clock.tick(frameRate)
        #SHOP END--------------------------------------------------------------------------------------------
        # rendering
        for enemyObject in enemyArray:
            # Walk framerate -> first position -> 2x framrate -> second position
            if enemyObject[4] < frameRate:
                gameScreen.blit(enemyObject[2], (enemyObject[0], enemyObject[1]))
                enemyObject[4] += 1
            else:
                gameScreen.blit(enemyObject[3], (enemyObject[0], enemyObject[1]))
                enemyObject[4] += 1
                if enemyObject[4] == frameRate*2:
                    enemyObject[4] = 0
            # Render Shoot Fly mobs
            if timer%(frameRate*int(6/level)) == 0:
                if freezEnemysWorks == 0:
                    if enemyObject[6] == 'fly':
                        throwedByEnemy.append([
                            math.atan2(
                                                    #--#enemyObject[0] - int(468*yScale)
                                yCastle-int(displayHeightGame//2)-int(34*yScale),
                                xCastle-enemyObject[0]
                            )
                            ,enemyObject[0]+int(80*xScale)
                            ,enemyObject[1]+int(80*yScale)
                            ,deidaraBoombArray
                            ,360
                        ])
            #-----------------------------------------------------------------------
            #If mob isn't on castle, move / IF SKILL FREEZ ENEMY ACTIVE:
            #-----------------------------------------------------------#
            if enemyObject[6] == 'fly':
                if displayWithGame//2 != enemyObject[0]:
                    if freezEnemysWorks == 0:
                        enemyObject[0] -= 1
            else:
                if enemyObject[0]-1 > xCastle-int(55*xScale):
                    if freezEnemysWorks == 0:
                        enemyObject[0] -= 1
            #----------------------------
            enemyObjectRect = pygame.Rect(enemyObject[2].get_rect())
            enemyObjectRect.left = enemyObject[0]
            enemyObjectRect.top = enemyObject[1]
            #Colision Shoot vs Enemy
            for shoot in throwedWeapon:
                shootRect = pygame.Rect(shoot[3][2].get_rect())
                if enemyObject[6] == 'fly':
                    shootRect.left = int(shoot[1] - int(90 * xScale))
                    shootRect.top = int(shoot[2] - int(30 * yScale))
                else:
                    shootRect.left = int(shoot[1]-int(50*xScale))
                    shootRect.top = int(shoot[2]-int(50*yScale))
                if shootRect.colliderect(enemyObjectRect):
                    hit.play()
                    gameScreen.blit(blood, (int(shoot[1]), int(shoot[2])))
                    enemyObject[5] -= shoot[3][3]+bonuses[0]
                    throwedWeapon.remove(shoot)
                    if enemyObject[5] < 0:
                        enemyArray.remove(enemyObject)
                        countMob[0]+=1
                        money[0] += 20*level
            #Colision Enemy vs Castle
            if CastleRect.colliderect(enemyObjectRect):
                if freezEnemysWorks == 0:
                    HP-=1/frameRate
                    hit.play()
        #-------------------------------------------------------------------------------
        # Colision Enemy Shoot vs Player Shoot
        for enemyShoot in throwedByEnemy:
            enemyShootRect = pygame.Rect(enemyShoot[3][2].get_rect())
            enemyShootRect.left = int(enemyShoot[1])
            enemyShootRect.top = int(enemyShoot[2])
            for shoot in throwedWeapon:
                shootRect = pygame.Rect(shoot[3][2].get_rect())
                shootRect.left = int(shoot[1])
                shootRect.top = int(shoot[2])
                if enemyShootRect.colliderect(shootRect):
                    gameScreen.blit(boom, (int(shoot[1]), int(shoot[2])))
                    explode.play()
                    throwedByEnemy.remove(enemyShoot)
                    throwedWeapon.remove(shoot)
            #Colision with Castle
            if enemyShootRect.colliderect(CastleRect):
                throwedByEnemy.remove(enemyShoot)
                gameScreen.blit(boom, (int(enemyShoot[1]-int(26*xScale)), int(enemyShoot[2])-int(26*yScale)))
                explode.play()
                HP-= (deidaraBoombArray[3]*level)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if ammoReload == False:
                    if ammo > 0:
                        # Throwing Weapon
                        mousePosition = pygame.mouse.get_pos()
                        #Line to, x,y, weapon[x,y,image,damage], angle
                        throwedWeapon.insert(0,[
                            math.atan2(
                                mousePosition[1]-int(468 * yScale),
                                mousePosition[0]-int(xCastle - (66 * xScale))
                            )
                            ,int(xCastle - (66 * xScale)),
                            int(468 * yScale),
                            actualyWeapon[0],
                            0])
                        ammo -= 1
            #KEYBOARD-------------------------
            if event.type == pygame.KEYUP:
                if event.key == K_r:
                    keys[0] = False
                if event.key == K_q:
                    keys[1] = False
            if event.type == pygame.KEYDOWN:
                if event.key == K_r:
                    keys[0] = True
                if event.key == K_q:
                    keys[1] = True
            #---------------------------------
        #Weapon Reload--
        if keys[0]:
            ammoReload = True
            reloadTimer = True
        if reloadTimer:
            reloadStart+=1
            if reloadStart == setReloadTime*frameRate:
                reloadTimer = False
                ammoReload = False
                reloadStart = 0
                ammo = maxAmmo[0]
        # freezSkills:
        if keys[1]:
            if 'freezEnemy' in skills:
                if freezEnemysReload == 0:
                    freezEnemysReload = 30 * frameRate
                    freezEnemysWorks = skills['freezEnemy']
        # Freez Skill#
        if freezEnemysWorks != 0:
            freezEnemysWorks -= 1
        if freezEnemysReload != 0:
            freezEnemysReload -= 1
        #----------------
        #Aletr Ammo = 0
        if ammo == 0 and ammoReload == False:
            printTextOn(gameScreen, font, 'Kliknij [R] by przeładować', int(360 * xScale), int(94 * yScale))
        #----------------
        printTextOn(gameScreen, font, 'Fala:  '+str(waves[0]), int(120 * xScale),int(38 * yScale))
        timer+=1
        pygame.display.update()
        clock.tick(frameRate)
        if HP <= 0:
            while fin:
                gameScreen.blit(lose, (0, 0))
                #Play Again
                button
                buttonInGame(gameScreen, lightGreen, int(400* xScale), displayHeightGame - int(350 * yScale),308, 60, launcher, 'fin')
                printTextOn(gameScreen, font, 'Tak', int(528* xScale),displayHeightGame - int(330 * yScale))
                buttonInGame(gameScreen, lightRed, int(1300 * xScale), displayHeightGame - int(350 * yScale), 308, 60,quit, 'fin')
                printTextOn(gameScreen, font, 'Nie', int(1452* xScale),displayHeightGame - int(330 * yScale))
                #Quit
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit(0)
                pygame.display.update()
                clock.tick(frameRate)
launcher()
