import math

import pygame

# Intialize the pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600))

# Caption and Icon
pygame.display.set_caption("Battleship")

# values
MAPFROMLEFT = 30
MAPFROMUP = 30
DISTANCEBETWEENMAP = 20
SIZESHIP = 30
SIZEMAP = SIZESHIP * 10
        
class Map:
    squareImg = pygame.image.load('square.png')
    squareImgShipHit = pygame.image.load('square hit.png')
    squareImgMapHit = pygame.image.load('square map hit.png')
    squareImgReveal = pygame.image.load('squareReveal.png')

    # 0 map 1 img map hit 2 img ship hit 6 ship1 7 ship3 8 ship5
    def __init__(self, startX, startY):
        self.startX = startX
        self.startY = startY
        self.squareMap = [[0 for i in range(10)] for j in range(10)]
        self.squareReveal = [[0 for i in range(10)] for j in range(10)]

    def draw(self):
        tempy = self.startY
        tempx = self.startX
        for i in range(10):
            for j in range(10):
                if self.squareReveal[i][j] == 3:
                    screen.blit(self.squareImgReveal, (tempx, tempy))

                if self.squareMap[i][j] == 0 or self.squareMap[i][j] >= 6:
                    screen.blit(self.squareImg, (tempx, tempy))

                elif self.squareMap[i][j] == 1:
                    screen.blit(self.squareImgMapHit, (tempx, tempy))

                elif self.squareMap[i][j] == 2:
                    screen.blit(self.squareImgShipHit, (tempx, tempy))

                tempx += SIZESHIP

            tempx = self.startX
            tempy += SIZESHIP



    def mapHit(self, y, x):
        if self.squareMap[y][x] == 0:
            self.squareMap[y][x] = 1
            if self.squareReveal == 3:
                self.squareReveal = 0
            return True
        elif self.squareMap[y][x] >= 6:
            self.squareMap[y][x] = 2
            if self.squareReveal == 3:
                self.squareReveal = 0
            return True

        return False


mapPlayer = Map(MAPFROMLEFT, MAPFROMUP)
mapAI = Map(MAPFROMLEFT + SIZEMAP + DISTANCEBETWEENMAP, MAPFROMUP)
mapAI.squareMap[0][0] = 10

rotateSkill1 = 0
skill1Img = pygame.image.load('squareSkill1.png')
skill2Img = pygame.image.load('squareRadar.png')
class Actor:

    def __init__(self, mapUsed: Map):
        self.mapUsed = mapUsed

    def skill1(self, y, x, rotate):
        if rotate == 0:
            for i in range(10):
                self.mapUsed.mapHit(i, x)

        if rotate == 90:
            for i in range(10):
                self.mapUsed.mapHit(x, i)

    def skill2(self, centerx, centery):
        for i in range(centery, centery + 3):
            for j in range(centerx, centerx + 3):
                if self.mapUsed.squareMap[i][j] >= ship1.identifier:
                    self.mapUsed.squareReveal[i][j] = 3




class Ship:
    def __init__(self, x, y, width, height, imageName, identifier):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = pygame.image.load(imageName)
        self.imageName = imageName
        self.defaultX = x
        self.defaultY = y
        self.identifier = identifier
        self.inMap = False
        self.xMap = -1
        self.yMap = -1
        self.heightPerSquare = int(height / SIZESHIP)
        self.widthPerSquare = int(width / SIZESHIP)
        self.rotate = 0

    def draw(self):
        screen.blit(self.image, (self.x, self.y))
    def rotateShip(self, mapUsed):
        if self.rotate == 0:
            self.rotate = 90
            self.image = pygame.transform.rotate(self.image, 90)
            temp = self.width
            self.width = self.height
            self.height = temp

        else:
            self.rotate = 0
            self.image = pygame.image.load(self.imageName)
            temp = self.width
            self.width = self.height
            self.height = temp

        if self.inMap:
            for i in range(int(ship.yMap / 30) - 1, int(ship.yMap / 30) + self.heightPerSquare):
                for j in range(int(ship.xMap / 30) - 1, int(ship.xMap / 30) + self.widthPerSquare):
                    mapUsed.squareMap[i][j] = 0

    def autocorrectPlace(self, mapUsed: Map):
        temp = self.x + (SIZESHIP / 2) - 30
        hasilx = 0
        hasily = 0
        while temp >= 30:
            temp -= 30
            hasilx += 1

        temp = self.y + (SIZESHIP / 2) - 30
        while temp >= 30:
            temp -= 30
            hasily += 1

        # check collide between ship
        stateTemp = True
        for i in range(hasily, hasily + self.heightPerSquare):
            for j in range(hasilx, hasilx + self.widthPerSquare):
                if not (mapUsed.squareMap[i][j] == 0) or mapUsed.squareMap[i][j] == self.identifier:
                    stateTemp = False
                    break

        # if not collide or need repositioning
        if stateTemp:
            # if already in map before
            if self.inMap:
                for i in range(int(self.yMap / 30) - 1, int(self.yMap / 30) + self.heightPerSquare - 1):
                    for j in range(int(self.xMap / 30) - 1, int(self.xMap / 30) + self.widthPerSquare - 1):
                        mapUsed.squareMap[i][j] = 0

            self.x = (hasilx * 30) + 30
            self.y = (hasily * 30) + 30
            self.xMap = self.x
            self.yMap = self.y

            for i in range(hasily, hasily + self.heightPerSquare):
                for j in range(hasilx, hasilx + self.widthPerSquare):
                    mapUsed.squareMap[i][j] = self.identifier
            self.inMap = True

        if not stateTemp:
            if not self.inMap:
                self.x = self.defaultX
                self.y = self.defaultY

            if self.inMap:
                self.x = self.xMap
                self.y = self.yMap



# tempat AI pake method aja

# ships
ship1 = Ship(350, 300, 30, 30, 'ship1.png', 6)
ship3 = Ship(390, 300, 30, 90, 'ship3.png', 7)
ship5 = Ship(420, 300, 30, 150, 'ship5.png', 8)

# ship1 = Ship(30, 30, 30, 30, 'ship1.png', 1)
# ship3 = Ship(60, 30, 30, 90, 'ship3.png', 3)
# ship5 = Ship(90, 30, 30, 150, 'ship5.png', 5)

listShip = [ship1, ship3, ship5]

# start
start = pygame.image.load('start.png')
startPending = pygame.image.load('startPending.png')

# prev mouse
mouseX, mouseY = pygame.mouse.get_pos()

# var
dragDrop = 0
delayRotate = 0
skillPencet = 0
delaySkill1 = 0
delaySkill2 = 0
delayAnimasi = 0
delayRotateSkill1 = 0

# Game Loop
player = Actor(mapAI)
AI = Actor(mapPlayer)
gameStart = False
running = True
playerTurn = True
while running:
    if not gameStart:
        delayRotate += 1
    if gameStart:
        delaySkill1 += 1
        delayRotateSkill1 += 1
        delayRotateSkill1 += 1
        delayAnimasi += 1
        delaySkill2 += 1

    # RGB = Red, Green, Blue
    screen.fill((255, 255, 255))

    # quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if pygame.key.get_pressed()[pygame.K_ESCAPE]:
        running = False

    # render ship
    for ship in listShip:
        ship.draw()

    # render map
    mapPlayer.draw()

    if not gameStart:
        screen.blit(start, (660, 200))

        # drag and drop ship
        if pygame.mouse.get_pressed()[0]:
            mx, my = pygame.mouse.get_pos()
            if dragDrop != 0:
                match dragDrop:
                    case 1:
                        ship1.x += mx - mouseX
                        ship1.y += my - mouseY

                    case 3:
                        ship3.x += mx - mouseX
                        ship3.y += my - mouseY

                    case 5:
                        ship5.x += mx - mouseX
                        ship5.y += my - mouseY

            elif ship1.x < mx < ship1.x + ship1.width and ship1.y < my < ship1.y + ship1.height:
                dragDrop = 1

            elif ship3.x < mx < ship3.x + ship3.width and ship3.y < my < ship3.y + ship3.height:
                dragDrop = 3

            elif ship5.x < mx < ship5.x + ship5.width and ship5.y < my < ship5.y + ship5.height:
                dragDrop = 5

        else:  # correct placement if outside box
            dragDrop = 0
            for ship in listShip:
                if MAPFROMLEFT + SIZEMAP + 10 < ship.x + ship.width or ship.x < MAPFROMLEFT - 10 or MAPFROMUP + SIZEMAP + 10 < ship.y + ship.height or ship.y < MAPFROMUP - 10:
                    if not ship.inMap:
                        ship.x = ship.defaultX
                        ship.y = ship.defaultY
                        ship.inMap = False

                    if ship.inMap:
                        ship.x = ship.xMap
                        ship.y = ship.yMap

        # rotate ship
        if pygame.key.get_pressed()[pygame.K_LCTRL] and pygame.mouse.get_pressed()[0] and delayRotate >= 100:
            mx, my = pygame.mouse.get_pos()
            for ship in listShip:
                if ship.x < mx < ship.x + ship.width and ship.y < my < ship.y + ship.height:
                    ship.rotateShip(mapPlayer)

            dragDrop = 0
            delayRotate = 0

        # autocorrect place ship and put into map
        if dragDrop == 0:
            for ship in listShip:
                if MAPFROMLEFT + SIZEMAP > ship.x and ship.x + ship.width > MAPFROMLEFT and MAPFROMUP + SIZEMAP > ship.y and ship.y + ship.height > MAPFROMUP:
                    ship.autocorrectPlace(mapPlayer)

        # press start

        stateTemp = True
        for ship in listShip:
            if not ship.inMap:
                stateTemp = False


        if stateTemp:
            if pygame.key.get_pressed()[pygame.K_TAB]:
                gameStart = True

            if 660 < pygame.mouse.get_pos()[0] < 760 and 200 < pygame.mouse.get_pos()[1] < 230 and \
                    pygame.mouse.get_pressed()[0]:
                gameStart = True

    # game start ------------------------------------------------------------------------------------------------------
    else:
        screen.blit(startPending, (660, 200))

        # draw map AI
        mapAI.draw()

        # tempat AI output kalo ai nya taruh di atas di luar loop nya
        outputx = 0
        outputy = 0
        # atau kalo mau langsung di map player hit ini

        mx, my = pygame.mouse.get_pos()

        # map player hit (atau giliran ai)
        if pygame.mouse.get_pressed()[0] and not playerTurn:
            if MAPFROMLEFT + SIZEMAP > mx > MAPFROMLEFT and MAPFROMUP + SIZEMAP > my > MAPFROMUP:
                hasilx = outputx
                hasily = outputy


                # if squareMap[hasily][hasilx] == 0:
                #     squareMap[hasily][hasilx] = 1
                #     playerTurn = True
                # elif squareMap[hasily][hasilx] >= 6:
                #     squareMap[hasily][hasilx] = 2
                #     playerTurn = True
                playerTurn = mapPlayer.mapHit(hasily, hasilx)

        # bagian giliran player----------------------------------------------------------------------------------------

        # torpedo (skill baris) (kode nya harus di atas map AI hit)
        if pygame.key.get_pressed()[pygame.K_1] and playerTurn and delaySkill1 >= 100:
            if skillPencet == 1:
                skillPencet = 0
            else:
                skillPencet = 1
                if rotateSkill1 == 0 and mapAI.startX + SIZEMAP > mx > mapAI.startX:
                    hasilx = -1
                    tempx = mx
                    while tempx > mapAI.startX:
                        tempx -= SIZESHIP
                        hasilx += 1

                    if rotateSkill1 == 0:
                        for i in range(10):
                            screen.blit(skill1Img, (mapAI.startX + (hasilx * 30), mapAI.startY))
                            mapAI.startY += SIZESHIP

                    mapAI.startY = MAPFROMUP

                    if pygame.mouse.get_pressed()[0]:
                        player.skill1(0, hasilx, rotateSkill1)
                        playerTurn = False
                        skillPencet = 0

                # horizontal
                if rotateSkill1 == 90 and MAPFROMUP + SIZEMAP > my > MAPFROMUP:
                    hasily = -1
                    tempy = my
                    while tempy > mapAI.startY:
                        tempy -= SIZESHIP
                        hasily += 1

                    for i in range(10):
                        screen.blit(skill1Img, (mapAI.startX, mapAI.startY + (hasily * 30)))
                        mapAI.startX += SIZESHIP

                    mapAI.startX = MAPFROMLEFT + SIZEMAP + DISTANCEBETWEENMAP

                    if pygame.mouse.get_pressed()[0]:
                        player.skill1(hasily, 0, rotateSkill1)
                        playerTurn = False
                        skillPencet = 0

            delaySkill1 = 0

        if skillPencet == 1 and playerTurn:
            if pygame.key.get_pressed()[pygame.K_LCTRL] and delayRotateSkill1 >= 100:
                if rotateSkill1 == 90:
                    rotateSkill1 = 0
                else:
                    rotateSkill1 = 90
                delayRotateSkill1 = 0

            #vertical
            if rotateSkill1 == 0 and mapAI.startX + SIZEMAP > mx > mapAI.startX:
                hasilx = -1
                tempx = mx
                while tempx > mapAI.startX:
                    tempx -= SIZESHIP
                    hasilx += 1

                for i in range(10):
                    screen.blit(skill1Img, (mapAI.startX + (hasilx * 30), mapAI.startY))
                    mapAI.startY += SIZESHIP

                mapAI.startY = MAPFROMUP

                if pygame.mouse.get_pressed()[0]:
                    player.skill1(0, hasilx, rotateSkill1)
                    playerTurn = False
                    skillPencet = 0

            if rotateSkill1 == 90 and MAPFROMUP + SIZEMAP > my > MAPFROMUP:
                hasily = -1
                tempy = my
                while tempy > mapAI.startY:
                    tempy -= SIZESHIP
                    hasily += 1

                for i in range(10):
                    screen.blit(skill1Img, (mapAI.startX, mapAI.startY + (hasily * 30)))
                    mapAI.startX += SIZESHIP

                mapAI.startX = MAPFROMLEFT + SIZEMAP + DISTANCEBETWEENMAP

                if pygame.mouse.get_pressed()[0]:
                    player.skill1(hasily, 0, rotateSkill1)
                    playerTurn = False
                    skillPencet = 0


        # radar
        if pygame.key.get_pressed()[pygame.K_2] and playerTurn and delaySkill2 >= 100:
            if skillPencet == 2:
                skillPencet = 0
            else:
                skillPencet = 2
                if mapAI.startX + 30 < mx < mapAI.startX + SIZEMAP - 30 and mapAI.startY + 30 < my < mapAI.startY + SIZEMAP - 30:
                    hasily = -2
                    tempy = my
                    while tempy > mapAI.startY:
                        tempy -= SIZESHIP
                        hasily += 1
                    hasilx = -2
                    tempx = mx
                    while tempx > mapAI.startX:
                        tempx -= SIZESHIP
                        hasilx += 1

                    screen.blit(skill2Img, (mapAI.startX + hasilx * 30, mapAI.startY + hasily * 30))
                    if pygame.mouse.get_pressed()[0]:
                        player.skill2(hasilx, hasily)
                        playerTurn = False

            delaySkill2 = 0

        if skillPencet == 2 and playerTurn:
            if mapAI.startX + 30 < mx < mapAI.startX + SIZEMAP - 30 and mapAI.startY + 30 < my < mapAI.startY + SIZEMAP - 30:
                hasily = -2
                tempy = my
                while tempy > mapAI.startY:
                    tempy -= SIZESHIP
                    hasily += 1
                hasilx = -2
                tempx = mx
                while tempx > mapAI.startX:
                    tempx -= SIZESHIP
                    hasilx += 1

                screen.blit(skill2Img, (mapAI.startX + hasilx * 30, mapAI.startY + hasily * 30))
                if pygame.mouse.get_pressed()[0]:
                    player.skill2(hasilx, hasily)
                    playerTurn = False

        # map AI hit
        if pygame.mouse.get_pressed()[0] and playerTurn:
            if mapAI.startX + SIZEMAP > mx > mapAI.startX and MAPFROMUP + SIZEMAP > my > MAPFROMUP:
                hasilx = -1
                hasily = -1
                tempx = mx
                tempy = my
                while tempx > mapAI.startX:
                    tempx -= 30
                    hasilx += 1

                while tempy > MAPFROMUP:
                    tempy -= 30
                    hasily += 1

                playerTurn = not mapAI.mapHit(hasily, hasilx)


    mouseX, mouseY = pygame.mouse.get_pos()
    pygame.display.update()
