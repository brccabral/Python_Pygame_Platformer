import pygame
from sys import exit
from overworld import Overworld
from settings import *

class Game:
    def __init__(self) -> None:
        self.overworld = Overworld()
    
    def run(self):
        self.overworld.run()

pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

game = Game()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    
    screen.fill('black')
    game.run()

    pygame.display.update()
    clock.tick(60)