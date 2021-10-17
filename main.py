import pygame
from sys import exit
from overworld import Overworld
from settings import *
from level import Level

class Game:
    def __init__(self) -> None:
        self.max_level = 3
        self.overworld = Overworld(0, self.max_level, screen, self.create_level)
        self.status = 'overworld'
    
    def create_level(self, current_level):
        self.level = Level(current_level, screen)
        self.status = 'level'
    
    def run(self):
        if self.status == 'overworld':
            self.overworld.run()
        else:
            self.level.run()

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