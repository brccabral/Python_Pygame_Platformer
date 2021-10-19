import pygame
from support import resource_path

class UI:
    def __init__(self, surface: pygame.Surface) -> None:
        # setup
        self.display_surface = surface

        # health
        self.health_bar = pygame.image.load(resource_path('assets/graphics/ui/health_bar.png')).convert_alpha()

        # coins
        self.coin = pygame.image.load(resource_path('assets/graphics/ui/coin.png')).convert_alpha()
    
    def show_health(self, current, full):
        self.display_surface.blit(self.health_bar, (20,10))

    def show_coins(self, amount):
        pass