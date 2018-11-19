import pygame, sys
import random
from pygame.locals import *

class Boid:
    def __init__(self):
        self.pos = self.setPos()
    def setPos(self):
        print(pygame.mouse.get_pos())
        return pygame.mouse.get_pos()
    def getPos(self):
        return self.pos
    def computeVelocity():
        pass
pygame.init()
fpsClock = pygame.time.Clock()

#Constants
BOID = 0
number_of_boids = 0
BOIDS = []
#Defining textures
textures = {
            BOID : pygame.image.load("textures/boid.png")

           }
#Defining colours
BLACK = (0, 0, 0)
BROWN = (153, 76, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)

TITLESIZE = 40
MAPWIDTH = 24
MAPHEIGHT = 18

DISPLAYSURF = pygame.display.set_mode((MAPWIDTH * TITLESIZE, MAPHEIGHT*TITLESIZE))
pygame.display.set_caption('2d Minecraft')

while True:
    DISPLAYSURF.fill(BLACK)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if pygame.mouse.get_pressed()[0]:
            boid = Boid()
            boid.pos = boid.getPos()
            BOIDS.append(list(boid.getPos()))
            number_of_boids += 1
    for i in BOIDS:
        DISPLAYSURF.blit(textures[BOID], i)
    for i in BOIDS:
        i[0] += random.randint(1, 10)
        i[1] += random.randint(1, 10)

    pygame.display.update()
    fpsClock.tick(24)
