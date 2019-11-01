import pygame

from enum import Flag
from random import randrange
from pytmx import load_pygame

class Direction(Flag):
    No = 0
    Up = 1
    Down = 2
    Left = 4
    Right = 8

WScreenSize = 1024
HScreenSize = 768

xScreenCenter = WScreenSize / 2
yScreenCenter = HScreenSize / 2

xPlayerStart = 100
yPlayerStart = 100

pygame.init()

gameDisplay = pygame.display.set_mode((WScreenSize, HScreenSize))
pygame.display.set_caption('Robot-E')

clock = pygame.time.Clock()

crashed = False

tmxdata = load_pygame("map/world.tmx")

worldWidthFields = tmxdata.width
worldHeightFields = tmxdata.height
print("World: " + str(worldWidthFields))
print("Height: " + str(worldHeightFields))

tileWidth = tmxdata.tilewidth
tileHeight = tmxdata.tileheight

playerImage = pygame.image.load('Blutsaugtroll.png')
playerShot = pygame.image.load('feuerball.png')

xPlayer = xPlayerStart
yPlayer = yPlayerStart
speedPlayer = 3
playerMoveDirection = Direction.No

playerFires = False
xPlayerFire = 0
yPlayerFire = 0
playerFireTtl = 0

fireSpeed = 10
fireDist = 500

enemyImage = pygame.image.load('Bombengoblin.png')
enemyShot = pygame.image.load('moewenball.png')
xEnemy = 100
yEnemy = 100
xEnemyTarget = 0
yEnemyTarget = 0

while not crashed:	
    # Draw Scene
    for x in range(0, worldWidthFields):
        for y in range(0, worldHeightFields):		
            image = tmxdata.get_tile_image(x, y, 0)
            gameDisplay.blit(image, (x*tileWidth+xPlayer-xScreenCenter, y*tileHeight+yPlayer-yScreenCenter))

    gameDisplay.blit(playerImage, (xScreenCenter, yScreenCenter))
    gameDisplay.blit(enemyImage, (xScreenCenter + xPlayer - xEnemy, yScreenCenter + yPlayer - yEnemy))


    # Move player
    if playerMoveDirection & Direction.Up == Direction.Up:
        yPlayer += speedPlayer
    if playerMoveDirection & Direction.Down == Direction.Down:
        yPlayer -= speedPlayer
    if playerMoveDirection & Direction.Left == Direction.Left:
        xPlayer += speedPlayer
    if playerMoveDirection & Direction.Right == Direction.Right:
        xPlayer -= speedPlayer

    # Move player shot
    if playerFires:
        xPlayerFire -= fireSpeed
        playerFireTtl -= fireSpeed
        gameDisplay.blit(playerShot, (xScreenCenter + xPlayer - xPlayerFire, yScreenCenter + yPlayer - yPlayerFire))
        if playerFireTtl <= 0:
            playerFires = False

    # Move enemy
    if xEnemyTarget == 0:
        xEnemyTarget = xEnemy + randrange(100) - 50
        yEnemyTarget = yEnemy + randrange(100) - 50
    else:
        if xEnemyTarget == xEnemy and yEnemyTarget == yEnemy:
            xEnemyTarget = 0
            yEnemyTarget = 0
        else:
            if xEnemyTarget < xEnemy:
                xEnemy -= 1
            elif xEnemyTarget > xEnemy:
                xEnemy +=1
            if yEnemyTarget < yEnemy:
                yEnemy -=1
            elif yEnemyTarget > yEnemy:
                yEnemy +=1
                


    # Process input events
    events = pygame.event.get()

    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerMoveDirection |= Direction.Left
            elif event.key == pygame.K_RIGHT:
                playerMoveDirection |= Direction.Right
            elif event.key == pygame.K_UP:
                playerMoveDirection |= Direction.Up
            elif event.key == pygame.K_DOWN:
                playerMoveDirection |= Direction.Down
            elif event.key == pygame.K_SPACE:
                playerFires = True
                xPlayerFire = xPlayer
                yPlayerFire = yPlayer
                playerFireTtl = fireDist
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                playerMoveDirection &= ~Direction.Left
            if event.key == pygame.K_RIGHT:
                playerMoveDirection &= ~Direction.Right                
            if event.key == pygame.K_UP:
                playerMoveDirection &= ~Direction.Up                
            if event.key == pygame.K_DOWN:
                playerMoveDirection &= ~Direction.Down

        if event.type == pygame.QUIT:
            crashed = True

    pygame.display.update()
    clock.tick(20)