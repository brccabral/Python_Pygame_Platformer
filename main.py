import pygame
from sys import exit
from overworld import Overworld
from settings import *
from level import Level
from support import resource_path
from ui import UI

class Game:
    def __init__(self) -> None:
        self.max_level: int = 0
        self.overworld = Overworld(0, self.max_level, screen, self.create_level)
        self.status = 'overworld'
        self.max_health: int = 100
        self.cur_health: int = 100
        self.coins: int = 0

        # user interface
        self.ui = UI(screen)
    
    def create_level(self, current_level: int):
        self.level = Level(current_level, screen, self.create_overworld, self.change_coins)
        self.status = 'level'

    def create_overworld(self, current_level: int, new_max_level: int):
        # check if the next level is unlocked
        if new_max_level > self.max_level:
            self.max_level = new_max_level
        self.overworld = Overworld(current_level, self.max_level, screen, self.create_level)
        self.status = 'overworld'
    
    def change_coins(self, amount: int):
        self.coins += amount

    def run(self):
        if self.status == 'overworld':
            self.overworld.run()
        else:
            self.level.run()
            self.ui.show_health(self.cur_health, self.max_health)
            self.ui.show_coins(self.coins)

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