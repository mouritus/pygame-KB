import pygame

# Intialize the pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600))

# Caption and Icon
pygame.display.set_caption("Battleship")

# 0 map 1 img map hit 2 img ship hit 3 ship1 4 ship3 5 ship5
squareMap = [[0 for i in range(10)] for j in range(10)]
squareMap[1][2] = 10
squareMapAI = [[0 for i in range(10)] for j in range(10)]

# map draw
squareImg = pygame.image.load('square.png')
squareImgShipHit = pygame.image.load('square hit.png')
squareImgMapHit = pygame.image.load('square map hit.png')

MAPFROMLEFT = 30
MAPFROMUP = 30


class Ship:
    rotate = 0
    defaultX = 0
    defaultY = 0

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

    def rotateImg(self):
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


# ships
sizeShip = 30
SIZEMAP = sizeShip * 10
ship1 = Ship(350, 300, 30, 30, 'ship1.png', 3)
ship3 = Ship(390, 300, 30, 90, 'ship3.png', 4)
ship5 = Ship(420, 300, 30, 150, 'ship5.png', 5)

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

# Game Loop
gameStart = False
running = True
playerTurn = True
while running:
    delayRotate += 1

    # RGB = Red, Green, Blue
    screen.fill((255, 255, 255))

    # quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if pygame.key.get_pressed()[pygame.K_ESCAPE]:
        running = False

    if pygame.key.get_pressed()[pygame.K_TAB]:
        gameStart = True

    # render ship
    screen.blit(ship5.image, (ship5.x, ship5.y))
    screen.blit(ship3.image, (ship3.x, ship3.y))
    screen.blit(ship1.image, (ship1.x, ship1.y))

    # render map
    square1Y = MAPFROMUP
    square1X = MAPFROMLEFT
    for i in range(10):
        for j in range(10):
            if squareMap[i][j] == 0 or squareMap[i][j] >= 3:
                screen.blit(squareImg, (square1X, square1Y))
                square1X += sizeShip

            elif squareMap[i][j] == 1:
                screen.blit(squareImgMapHit, (square1X, square1Y))
                square1X += sizeShip

            elif squareMap[i][j] == 2:
                screen.blit(squareImgShipHit, (square1X, square1Y))
                square1X += sizeShip

        square1Y += sizeShip
        square1X = MAPFROMLEFT

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
                    shipHeight = int(ship.height / 30)
                    shipWidth = int(ship.width / 30)

                    ship.rotateImg()
                    if ship.inMap:
                        for i in range(int(ship.yMap / 30) - 1, int(ship.yMap / 30) + shipHeight):
                            for j in range(int(ship.xMap / 30) - 1, int(ship.xMap / 30) + shipWidth):
                                squareMap[i][j] = 0
                    #
                    #     for i in range(int(ship.yMap / 30), int(ship.yMap / 30) + ship.height):
                    #         for j in range(int(ship.xMap / 30), int(ship.xMap / 30) + ship.width):

            dragDrop = 0
            delayRotate = 0

        # autocorrect place ship and put into map
        if dragDrop == 0:
            for ship in listShip:
                # if in map
                if MAPFROMLEFT + SIZEMAP > ship.x and ship.x + ship.width > MAPFROMLEFT and MAPFROMUP + SIZEMAP > ship.y and ship.y + ship.height > MAPFROMUP:
                    temp = ship.x + (sizeShip / 2) - 30
                    hasilx = 0
                    hasily = 0
                    while temp >= 30:
                        temp -= 30
                        hasilx += 1

                    temp = ship.y + (sizeShip / 2) - 30
                    while temp >= 30:
                        temp -= 30
                        hasily += 1

                    # check collide between ship
                    stateTemp = True
                    for i in range(hasily, hasily + int(ship.height / 30)):
                        for j in range(hasilx, hasilx + int(ship.width / 30)):
                            if not (squareMap[i][j] == 0) or squareMap[i][j] == ship.identifier:
                                print(squareMap[i][j])
                                stateTemp = False

                    # if not collide or need repositioning
                    if stateTemp:
                        # if already in map before
                        if ship.inMap:
                            for i in range(int(ship.yMap / 30), int(ship.yMap / 30) + int(ship.height / 30)):
                                for j in range(int(ship.xMap / 30), int(ship.xMap / 30) + int(ship.width / 30)):
                                    squareMap[i][j] = 0

                        ship.x = (hasilx * 30) + 30
                        ship.y = (hasily * 30) + 30
                        print(hasily, hasilx)
                        ship.xMap = ship.x
                        ship.yMap = ship.y

                        for i in range(hasily, hasily + int(ship.height / 30)):
                            for j in range(hasilx, hasilx + int(ship.width / 30)):
                                squareMap[i][j] = ship.identifier

                        ship.inMap = True

                    if not stateTemp:
                        if not ship.inMap:
                            ship.x = ship.defaultX
                            ship.y = ship.defaultY

                        if ship.inMap:
                            ship.x = ship.xMap
                            ship.y = ship.yMap



        # press start
        if 660 < pygame.mouse.get_pos()[0] < 760 and 200 < pygame.mouse.get_pos()[1] < 230 and \
                pygame.mouse.get_pressed()[0]:
            gameStart = True
            # for ship in listShip:
            #     temp = ship.x - 30
            #     hasilx = 0
            #     hasily = 0
            #     while temp >= 30:
            #         temp -= 30
            #         hasilx += 1
            #
            #     temp = ship.y + (sizeShip / 2) - 30
            #     while temp >= 30:
            #         temp -= 30
            #         hasily += 1
            #
            #     for i in range(hasily, hasily + int(ship.height / 30)):
            #         for j in range(hasilx, hasilx + int(ship.width / 30)):
            #             squareMap[i][j] = ship.identifier

    # game start ------------------------------------------------------------------------------------------------------
    else:
        screen.blit(startPending, (660, 200))

        # draw map AI
        squareAI1Y = 30
        squareAI1X = MAPFROMLEFT + SIZEMAP + 20
        for i in range(10):
            for j in range(10):
                if squareMapAI[i][j] == 0 or squareMap[i][j] >= 3:
                    screen.blit(squareImg, (squareAI1X, squareAI1Y))
                    squareAI1X += sizeShip

                elif squareMapAI[i][j] == 1:
                    screen.blit(squareImgMapHit, (squareAI1X, squareAI1Y))
                    squareAI1X += sizeShip

                elif squareMapAI[i][j] == 2:
                    screen.blit(squareImgShipHit, (squareAI1X, squareAI1Y))
                    squareAI1X += sizeShip

            squareAI1Y += sizeShip
            squareAI1X = MAPFROMLEFT + SIZEMAP + 20

        squareAI1X = MAPFROMLEFT + SIZEMAP + 20

        # map player hit
        if pygame.mouse.get_pressed()[0] and not playerTurn:
            mx, my = pygame.mouse.get_pos()
            if MAPFROMLEFT + SIZEMAP > mx > MAPFROMLEFT and MAPFROMUP + SIZEMAP > my > MAPFROMUP:
                hasilx = -1
                hasily = -1
                while mx > MAPFROMLEFT:
                    mx -= 30
                    hasilx += 1

                while my > MAPFROMUP:
                    my -= 30
                    hasily += 1

                if squareMap[hasily][hasilx] == 0:
                    squareMap[hasily][hasilx] = 1
                    playerTurn = True
                elif squareMap[hasily][hasilx] >= 3:
                    squareMap[hasily][hasilx] = 2
                    playerTurn = True

        # map AI hit
        if pygame.mouse.get_pressed()[0] and playerTurn:
            mx, my = pygame.mouse.get_pos()
            if squareAI1X + SIZEMAP > mx > squareAI1X and MAPFROMUP + SIZEMAP > my > MAPFROMUP:
                hasilx = -1
                hasily = -1
                while mx > squareAI1X:
                    mx -= 30
                    hasilx += 1

                while my > MAPFROMUP:
                    my -= 30
                    hasily += 1

                if squareMapAI[hasily][hasilx] == 0:
                    squareMapAI[hasily][hasilx] = 1
                    playerTurn = False
                elif squareMapAI[hasily][hasilx] >= 3:
                    squareMapAI[hasily][hasilx] = 2
                    playerTurn = False

        # # Collision
        # collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        # if collision:
        #     explosionSound = mixer.Sound("explosion.wav")
        #     explosionSound.play()
        #     bulletY = 480
        #     bullet_state = "ready"
        #     score_value += 1
        #     enemyX[i] = random.randint(0, 736)
        #     enemyY[i] = random.randint(50, 150)


    mouseX, mouseY = pygame.mouse.get_pos()
    pygame.display.update()
