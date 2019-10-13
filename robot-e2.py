import pygame

from enum import Flag
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

xPlayerStart = 20 * 32
yPlayerStart = 20 * 32

pygame.init()

gameDisplay = pygame.display.set_mode((WScreenSize, HScreenSize))
pygame.display.set_caption('Robot-E')

clock = pygame.time.Clock()

crashed = False

tmxdata = load_pygame("map/world.tmx")

worldWidth = tmxdata.width
worldHeight = tmxdata.height
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
xEnemy = 0
yEnemy = 0
enemyExists = False

while not crashed:	
    for x in range(0, worldWidth):
        for y in range(0, worldHeight):		
            image = tmxdata.get_tile_image(x, y, 0)
            gameDisplay.blit(image, (x*tileWidth+xPlayer, y*tileHeight+yPlayer))

    gameDisplay.blit(playerImage, (xScreenCenter, yScreenCenter))

    if playerMoveDirection & Direction.Up == Direction.Up:
        yPlayer += speedPlayer
    if playerMoveDirection & Direction.Down == Direction.Down:
        yPlayer -= speedPlayer
    if playerMoveDirection & Direction.Left == Direction.Left:
        xPlayer += speedPlayer
    if playerMoveDirection & Direction.Right == Direction.Right:
        xPlayer -= speedPlayer

    if playerFires:
        xPlayerFire -= fireSpeed
        playerFireTtl -= fireSpeed
        gameDisplay.blit(playerShot, (xPlayerFire - xPlayer, yPlayerFire - yPlayer))
        if playerFireTtl <= 0:
            playerFires = False

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
                xPlayerFire = xPlayer + xScreenCenter
                yPlayerFire = yPlayer + yScreenCenter
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
    clock.tick(60)