import pygame
from pygame import sprite
from support import import_folder, resource_path
from settings import vertical_tile_number, tile_size, screen_width
from tiles import AnimatedTile, StaticTile
from random import choice, randint

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
            if row < self.horizon:
                surface.blit(self.top, (0,y))
            elif row == self.horizon:
                surface.blit(self.middle, (0,y))
            else:
                surface.blit(self.bottom, (0,y))

class Water:
    # the water needs to stretch more than the level width
    # both to the left and to the right
    def __init__(self, top, level_width) -> None:
        water_start = -screen_width
        water_tile_width = 192
        tile_x_amount = (level_width + screen_width) // water_tile_width
        self.water_sprites = pygame.sprite.Group()

        for tile in range(tile_x_amount):
            x = tile * water_tile_width+ water_start
            y = top
            sprite = AnimatedTile((x,y), water_tile_width, 'assets/graphics/decoration/water')
            self.water_sprites.add(sprite)
    
    def draw(self, surface, shift):
        self.water_sprites.update(shift)
        self.water_sprites.draw(surface)

class Clouds:
    def __init__(self, horizon, level_width, cloud_number) -> None:
        cloud_surface_list = import_folder('assets/graphics/decoration/clouds')
        min_x = -screen_width
        max_x = level_width + screen_width
        min_y = 0
        max_y = horizon
        self.could_sprites = pygame.sprite.Group()

        for cloud in range(cloud_number):
            cloud_surface = choice(cloud_surface_list)
            x = randint(min_x, max_x)
            y = randint(min_y, max_y)
            sprite = StaticTile((x,y), 0, cloud_surface)
            self.could_sprites.add(sprite)
    
    def draw(self, surface, shift):
        self.could_sprites.update(shift)
        self.could_sprites.draw(surface)
