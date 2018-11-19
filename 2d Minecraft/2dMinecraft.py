import pygame, sys
import random
from pygame.locals import *

pygame.init()
fpsClock = pygame.time.Clock()
#Defining colours
BLACK = (0, 0, 0)
BROWN = (153, 76, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)

#Zombie constants
ZOMBIE_DIST = 3
zombieNotDead = True
#Cloud position variable
cloudx = -200
cloudy = 0
#Defining resources
DIRT = 0
GRASS = 1
WATER = 2
COAL = 3
LAVA = 4
WOOD = 5
STONE = 6
DIAMOND = 7
CLOUD = 8
ZOMBIE = 9
HEART = 10
FOOD = 11

#Setting up the player
PLAYER = pygame.image.load('sprites/player.png')
playerPos = [0, 0]
playerHealth = 5
playerFood = 10
amountOfFood = 0
#Colour to resource dictionary
textures = {
            DIRT:  pygame.image.load('sprites/dirt.png'),
            GRASS: pygame.image.load('sprites/grass.png'),
            WATER: pygame.image.load('sprites/water.png'),
            COAL: pygame.image.load('sprites/coal.png'),
            LAVA: pygame.image.load('sprites/lava.png'),
            WOOD: pygame.image.load('sprites/wood.png'),
            STONE: pygame.image.load('sprites/stone.png'),
            DIAMOND: pygame.image.load('sprites/diamond.png'),
            CLOUD: pygame.image.load('sprites/cloud.png'),
            ZOMBIE:pygame.image.load('sprites/zombie.png'),
            HEART:pygame.image.load('sprites/heart.png'),
            FOOD:pygame.image.load('sprites/food.png')
}

#Defining the inventory
inventory = {
            DIRT :    0,
            GRASS :   0,
            WATER :   0,
            COAL :    0,
            STONE :   0,
            DIAMOND : 0,
            WOOD :    0,
            LAVA :    0
}

#Inventory constants
controls = {
            DIRT: 49,
            GRASS: 50,
            WATER: 51,
            COAL : 52,
            LAVA : 53,
            WOOD: 54,
            STONE: 55,
            DIAMOND: 56,
            FOOD: 57
}
#Crafting rules
craft = {
        GRASS : {DIRT : 2},
        LAVA  : {WATER: 2, COAL : 2},
        DIAMOND : {DIRT: 100},
        COAL : {STONE : 2, LAVA: 2},
        WOOD: {LAVA : 2, STONE:2},
        FOOD: {GRASS : 5, DIRT: 5}
}
#Game Dims
#DEFAULT TILE SIZE = 40
TITLESIZE = 40
MAPWIDTH = 24
MAPHEIGHT = 18

#Tilemap
resources = [DIRT, GRASS, WATER, COAL, WOOD, LAVA, STONE, DIAMOND]
tilemap = [[GRASS for w in range(MAPWIDTH)]for h in range(MAPHEIGHT)]

for rw in range(MAPHEIGHT):
    for cl in range(MAPWIDTH):
        randomNumber = random.randint(0, 50)

        if randomNumber >= 23 and randomNumber <= 25:
            tile = COAL
        elif randomNumber >= 25 and randomNumber <= 27:
            tile = LAVA
        elif randomNumber >=3 and randomNumber <= 7:
            tile = DIRT
        elif randomNumber >= 8 and randomNumber <= 14:
            tile = WATER
        elif randomNumber >= 15 and randomNumber <= 18:
            tile = STONE
        elif randomNumber >= 19 and randomNumber <= 22:
            tile = WOOD
        elif randomNumber == 0:
            tile = DIAMOND
        else:
            tile = GRASS
        tilemap[rw][cl] = tile

DISPLAYSURF = pygame.display.set_mode((MAPWIDTH * TITLESIZE, MAPHEIGHT*TITLESIZE + 100))
pygame.display.set_caption('2d Minecraft')
fonts = pygame.font.get_fonts()

INVFONT = pygame.font.Font("comici.ttf",20)
while True:
    DISPLAYSURF.fill(BLACK)

    for event in pygame.event.get():

        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if (event.key == K_RIGHT) and playerPos[0] < MAPWIDTH - 1:
                playerPos[0] += 1
            if (event.key == K_LEFT and playerPos[0] >= 1):
                playerPos[0] -= 1
            if (event.key == K_UP and playerPos[1] >= 1):
                playerPos[1] -= 1
            if (event.key == K_DOWN) and playerPos[1] < MAPHEIGHT -1:
                playerPos[1] +=1
            if event.key == K_SPACE:
                currentTile = tilemap[playerPos[1]][playerPos[0]]
                inventory[currentTile] += 1

                tilemap[playerPos[1]][playerPos[0]] = DIRT
            for key in controls:
                if (event.key == controls[key]):
                    if pygame.mouse.get_pressed()[0]:
                        if key in craft:
                            canBeMade = True
                            for i in craft[key]:
                                if craft[key][i] > inventory[i]:
                                    canBeMade = False
                                    break
                                if canBeMade:
                                    for i in craft[key]:
                                        inventory[i] -= craft[key][i]
                                        inventory[key] += 1
                    else :
                        currentTile = tilemap[playerPos[1]][playerPos[0]]
                        if inventory[key] > 0:
                            inventory[key] -= 1
                            inventory[currentTile] += 1
                            tilemap[playerPos[1]][playerPos[0]] = key
    for row in range(MAPHEIGHT):
        for column in range(MAPWIDTH):
            DISPLAYSURF.blit(textures[tilemap[row][column]], (column*TITLESIZE, row*TITLESIZE))
    DISPLAYSURF.blit(PLAYER, (playerPos[0] * TITLESIZE, playerPos[1] * TITLESIZE))
    hpos = 0
    placePosition = 10
    for item in resources:
        DISPLAYSURF.blit(textures[item], (placePosition, MAPHEIGHT * TITLESIZE + 20))
        placePosition += 30
        textObj = INVFONT.render(str(inventory[item]), True, WHITE, BLACK)
        DISPLAYSURF.blit(textObj, (placePosition, MAPHEIGHT * TITLESIZE + 20))
        placePosition += 50
        hpos = placePosition
    DISPLAYSURF.blit(textures[FOOD], (hpos, MAPHEIGHT * TITLESIZE + 20))
    textObj = INVFONT.render(str(amountOfFood), True, WHITE, BLACK)
    DISPLAYSURF.blit(textObj, (hpos, MAPHEIGHT * TITLESIZE + 20))
    hpos += 50
    fpos = hpos
    for i in range(0, playerFood):
        DISPLAYSURF.blit(textures[FOOD], (fpos, MAPHEIGHT * TITLESIZE+ 40))
        fpos += 20
    for i in range(0, playerHealth):
        DISPLAYSURF.blit(textures[HEART], (hpos, MAPHEIGHT * TITLESIZE+ 20))
        hpos += 20
                    
    DISPLAYSURF.blit(textures[CLOUD].convert_alpha(), (cloudx, cloudy))

    cloudx += 1
    if cloudx > MAPWIDTH * TITLESIZE:
        cloudy = random.randint(0, MAPHEIGHT * TITLESIZE)
        cloudx = -200
    cloudx2 = cloudx - 200
    cloudy2 = cloudy - 200
    zombiePos = [playerPos[0] - ZOMBIE_DIST, playerPos[1] - ZOMBIE_DIST]
    DISPLAYSURF.blit(textures[CLOUD].convert_alpha(), (cloudx2, cloudy2))
    DISPLAYSURF.blit(textures[ZOMBIE], ((playerPos[0] - ZOMBIE_DIST) * TITLESIZE, (playerPos[1] - ZOMBIE_DIST) * TITLESIZE))
    try:
        zombieBlock = tilemap[zombiePos[0]][zombiePos[1]]
    except:
        print("ERROR")
    #print(resources[zombieBlock])
    #print(zombieBlock)
    currentTile = tilemap[playerPos[1]][playerPos[0]]
    print(currentTile)
    if zombieBlock == 4:
        #print(resources[zombieBlock])
        #print("LAVA")
        ZOMBIE_DIST = 5
        zombieNotDead = False
        
    if zombiePos[0] == playerPos[0] and zombiePos[1] == playerPos[1]:
        ZOMBIE_DIST = 5
        playerHealth -= 1
        
    if playerHealth == 0 or playerFood == 0:
        pygame.quit()
        sys.exit()
    chance = random.randint(0, 100)
    if chance == 5:
        ZOMBIE_DIST -= 1
    hungerLoss = random.randint(1, 100)
    if hungerLoss == 100:
        playerFood -= 1
    pygame.display.update()
    fpsClock.tick(24)
