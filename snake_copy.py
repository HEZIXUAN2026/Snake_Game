import pygame
import random
import sys

pygame.init()
pygame.font.init()

WIDTH,HEIGHT=600,600
GRID_SIZE=20
GRID_WIDTH=WIDTH//GRID_SIZE
GRID_HEIGHT=HEIGHT//GRID_SIZE
FPS=10

BLACK=(0,0,0)
WHITE=(255,255,255)
RED=(255,50,50)
GREEN=(50,200,50)
DARK_GREEN=(30,150,30)
GRAY=(40,40,40)

screen=pygame.display.set_mode((WIDTH,HEIGHT))
