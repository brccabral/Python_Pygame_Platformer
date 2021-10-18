import pygame
from support import import_folder, resource_path
from settings import vertical_tile_number, tile_size, screen_width
from tiles import AnimatedTile, StaticTile
from random import choice, randint

class Sky:
    def  __init__(self, horizon, style = 'level') -> None:
        self.top = pygame.image.load(resource_path('assets/graphics/decoration/sky/sky_top.png')).convert()
        self.bottom = pygame.image.load(resource_path('assets/graphics/decoration/sky/sky_bottom.png')).convert()
        self.middle = pygame.image.load(resource_path('assets/graphics/decoration/sky/sky_middle.png')).convert()
        self.horizon = horizon

        self.style = style
        if self.style == 'overworld':
            palm_surfaces = import_folder('assets/graphics/overworld/palms')
            self.palms = []
            for surface in [choice(palm_surfaces) for _ in range(10)]:
                x = randint(0, screen_width)
                y = self.horizon*tile_size + randint(50,100)
                rect = surface.get_rect(midbottom = (x,y))
                self.palms.append((surface, rect))

            cloud_surfaces = import_folder('assets/graphics/overworld/clouds')
            self.clouds = []
            for surface in [choice(cloud_surfaces) for _ in range(10)]:
                x = randint(0, screen_width)
                y = randint(0, self.horizon*tile_size - 100)
                rect = surface.get_rect(midbottom = (x,y))
                self.clouds.append((surface, rect))
        
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
        
        if self.style == 'overworld':
            for palm_surf, palm_rect in self.palms:
                surface.blit(palm_surf, palm_rect)
            for cloud_surf, cloud_rect in self.clouds:
                surface.blit(cloud_surf, cloud_rect)

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
