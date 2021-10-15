import pygame
from sys import exit
from settings import *
from tiles import Tile

pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
test_tile = pygame.sprite.Group(Tile((100,100),200))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    
    screen.fill('black')
    test_tile.draw(screen)

    pygame.display.update()
    clock.tick(60)