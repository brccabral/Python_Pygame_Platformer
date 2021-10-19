import pygame
from sys import exit
from overworld import Overworld
from settings import *
from level import Level
from support import resource_path

class Game:
    def __init__(self) -> None:
        self.max_level = 0
        self.overworld = Overworld(0, self.max_level, screen, self.create_level)
        self.status = 'overworld'
        self.max_health = 100
        self.cur_health = 100
        self.coin = 0
    
    def create_level(self, current_level):
        self.level = Level(current_level, screen, self.create_overworld)
        self.status = 'level'

    def create_overworld(self, current_level, new_max_level):
        # check if the next level is unlocked
        if new_max_level > self.max_level:
            self.max_level = new_max_level
        self.overworld = Overworld(current_level, self.max_level, screen, self.create_level)
        self.status = 'overworld'
    
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
    
    game.run()

    pygame.display.update()
    clock.tick(60)