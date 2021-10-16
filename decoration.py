import pygame
from support import resource_path
from settings import vertical_tile_number, tile_size, screen_width

class Sky:
    def  __init__(self, horizon) -> None:
        self.top = pygame.image.load(resource_path('assets/graphics/decoration/sky/sky_top.png')).convert()
        self.bottom = pygame.image.load(resource_path('assets/graphics/decoration/sky/sky_bottom.png')).convert()
        self.middle = pygame.image.load(resource_path('assets/graphics/decoration/sky/sky_middle.png')).convert()
        self.horizon = horizon
        
        # stretch
        self.top = pygame.transform.scale(self.top, (screen_width, tile_size))
        self.bottom = pygame.transform.scale(self.bottom, (screen_width, tile_size))
        self.middle = pygame.transform.scale(self.middle, (screen_width, tile_size))

    def draw(self, surface: pygame.Surface):
        for row in range(vertical_tile_number):
            y = row * tile_size
            surface.blit(self.top, (0,y))