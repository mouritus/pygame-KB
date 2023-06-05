import pygame

# Intialize the pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600))

# Caption and Icon
pygame.display.set_caption("Battleship")

# 0 map 1 img map hit 2 img ship hit 3 ship1 4 ship3 5 ship5
square = [[0 for i in range(10)] for j in range(10)]

# map draw
squareImg = pygame.image.load('square.png')
squareImgShipHit = pygame.image.load('square hit.png')
squareImgMapHit = pygame.image.load('square map hit.png')

square1X = 30
square1Y = 30


class Ship:
    rotate = 0

    def __init__(self, x, y, width, height, imageName):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = pygame.image.load(imageName)
        self.imageName = imageName

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
# ship1 = Ship(400, 300, 30, 30, 'ship1.png')
# ship3 = Ship(500, 300, 30, 90, 'ship3.png')
# ship5 = Ship(600, 300, 30, 150, 'ship5.png')

ship1 = Ship(30, 30, 30, 30, 'ship1.png')
ship3 = Ship(60, 30, 30, 90, 'ship3.png')
ship5 = Ship(90, 30, 30, 150, 'ship5.png')


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
while running:
    delayRotate += 1

    # RGB = Red, Green, Blue
    screen.fill((255, 255, 255))

    # quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # render ship
    screen.blit(ship5.image, (ship5.x, ship5.y))
    screen.blit(ship3.image, (ship3.x, ship3.y))
    screen.blit(ship1.image, (ship1.x, ship1.y))

    # render map
    size = 30
    for i in range(10):
        for j in range(10):
            match square[i][j]:
                case 0 | 3 | 4 | 5:
                    screen.blit(squareImg, (square1X, square1Y))
                    square1Y += size

                case 1:
                    screen.blit(squareImgMapHit, (square1X, square1Y))
                    square1Y += size

                case 2:
                    screen.blit(squareImgShipHit, (square1X, square1Y))
                    square1Y += size

        square1Y = size
        square1X += size
    square1Y = 30
    square1X = 30

    if not gameStart:
        screen.blit(start, (600, 200))
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
        else:
            dragDrop = 0

        # rotate ship
        if pygame.key.get_pressed()[pygame.K_LCTRL] and pygame.mouse.get_pressed()[0] and delayRotate >= 100:
            mx, my = pygame.mouse.get_pos()
            if ship3.x < mx < ship3.x + ship3.width and ship3.y < my < ship3.y + ship3.height:
                ship3.rotateImg()

            elif ship5.x < mx < ship5.x + ship5.width and ship5.y < my < ship5.y + ship5.height:
                ship5.rotateImg()

            dragDrop = 0
            delayRotate = 0

        # autocorrect place ship
        if dragDrop == 0:
            for ship in (ship1, ship3, ship5):
                if 330 > ship.x and ship.x + ship.width > 30 and 330 > ship.y and ship.y + ship.height > 30:
                    temp = ship.x + (size / 2) - 30
                    hasilx = 0
                    hasily = 0
                    while temp > 30:
                        temp -= 30
                        hasilx += 1

                    temp = ship.y + (size / 2) - 30
                    while temp > 30:
                        temp -= 30
                        hasily += 1

                    ship.x = (hasilx * 30) + 30
                    ship.y = (hasily * 30) + 30

        # press start
        if 600 < pygame.mouse.get_pos()[0] < 700 and 200 < pygame.mouse.get_pos()[1] < 230 and pygame.mouse.get_pressed()[0]:
            square[int((ship1.x - 30) / 30)][int((ship1.y - 30) / 30)] = 3
            iter = 0
            for ship in (ship3, ship5):
                temp = ship.x - 30
                hasilx = 0
                hasily = 0
                while temp >= 30:
                    temp -= 30
                    hasilx += 1

                temp = ship.y + (size / 2) - 30
                while temp >= 30:
                    temp -= 30
                    hasily += 1

                for i in range(hasily, hasily + int(ship.height / 30)):
                    for j in range(hasilx, hasilx + int(ship.width / 30)):
                        square[i][j] = iter + 4
                iter += 1
                print(hasilx, int(ship.width / 30))
            gameStart = True

            for i in range(10):
                print(square[i])

    # game start ------------------------------------------------------------------------------------------------------
    else:
        screen.blit(startPending, (600, 200))
        # map hit
        if pygame.mouse.get_pressed()[0]:
            mx, my = pygame.mouse.get_pos()
            mx -= 30
            my -= 30
            if 300 > mx > 0 and 300 > my > 0:
                hasilx = 0
                hasily = 0
                while mx > 30:
                    mx -= 30
                    hasilx += 1

                while my > 30:
                    my -= 30
                    hasily += 1

                square[hasilx][hasily] = 1

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
