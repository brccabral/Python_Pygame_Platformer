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
        self.max_health: int = 100
        self.cur_health: int = 100
        self.coins: int = 0
        self.screen = pygame.display.get_surface()

        # user interface
        self.ui = UI(self.screen)
        # audio
        self.level_bg_music = pygame.mixer.Sound(resource_path('assets/audio/level_music.wav'))
        self.level_bg_music.set_volume(0.1)
        self.overworld_bg_music = pygame.mixer.Sound(resource_path('assets/audio/overworld_music.wav'))
        self.overworld_bg_music.set_volume(0.1)

        # overworld setup
        self.overworld = Overworld(0, self.max_level, self.screen, self.create_level)
        self.status = 'overworld'
        self.overworld_bg_music.play(loops=-1)
    
    def create_level(self, current_level: int):
        self.level = Level(current_level, self.screen, self.create_overworld, self.change_coins, self.change_health)
        self.status = 'level'
        self.overworld_bg_music.stop()
        self.level_bg_music.play(loops=-1)

    def create_overworld(self, current_level: int, new_max_level: int):
        # check if the next level is unlocked
        if new_max_level > self.max_level:
            self.max_level = new_max_level
        self.overworld = Overworld(current_level, self.max_level, self.screen, self.create_level)
        self.status = 'overworld'
        self.level_bg_music.stop()
        self.overworld_bg_music.play(loops=-1)
    
    def change_coins(self, amount: int):
        self.coins += amount

    def change_health(self, amount: int):
        self.cur_health += amount

    def check_game_over(self):
        if self.cur_health <= 0:
            self.coins = 0
            self.cur_health = 100
            self.max_level = 0
            self.overworld = Overworld(0, self.max_level, self.screen, self.create_level)
            self.status = 'overworld'
            self.level_bg_music.stop()
            self.overworld_bg_music.play(loops=-1)

    def run(self):
        if self.status == 'overworld':
            self.overworld.run()
        else:
            self.level.run()
            self.ui.show_health(self.cur_health, self.max_health)
            self.ui.show_coins(self.coins)
            self.check_game_over()

def main():
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

if __name__ == '__main__':
    main()
