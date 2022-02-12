from typing import List
import pygame
from support import import_folder, resource_path
from settings import VERTICAL_TILE_NUMBER, TILE_SIZE, SCREEN_WIDTH
from tiles import AnimatedTile, StaticTile
from random import choice, randint


class Sky:
    def __init__(self, horizon, style='level') -> None:
        self.top = pygame.image.load(resource_path(
            'assets/graphics/decoration/sky/sky_top.png')).convert()
        self.bottom = pygame.image.load(resource_path(
            'assets/graphics/decoration/sky/sky_bottom.png')).convert()
        self.middle = pygame.image.load(resource_path(
            'assets/graphics/decoration/sky/sky_middle.png')).convert()
        self.horizon = horizon

        self.style = style
        if self.style == 'overworld':
            palm_surfaces = import_folder('assets/graphics/overworld/palms')
            self.palms = []
            for surface in [choice(palm_surfaces) for _ in range(10)]:
                x = randint(0, SCREEN_WIDTH)
                y = self.horizon*TILE_SIZE + randint(50, 100)
                rect = surface.get_rect(midbottom=(x, y))
                self.palms.append((surface, rect))

            cloud_surfaces = import_folder('assets/graphics/overworld/clouds')
            self.clouds = []
            for surface in [choice(cloud_surfaces) for _ in range(10)]:
                x = randint(0, SCREEN_WIDTH)
                y = randint(0, self.horizon*TILE_SIZE - 100)
                rect = surface.get_rect(midbottom=(x, y))
                self.clouds.append((surface, rect))

        # stretch
        self.top = pygame.transform.scale(self.top, (SCREEN_WIDTH, TILE_SIZE))
        self.bottom = pygame.transform.scale(
            self.bottom, (SCREEN_WIDTH, TILE_SIZE))
        self.middle = pygame.transform.scale(
            self.middle, (SCREEN_WIDTH, TILE_SIZE))

    def draw(self, surface: pygame.Surface):
        for row in range(VERTICAL_TILE_NUMBER):
            y = row * TILE_SIZE
            if row < self.horizon:
                surface.blit(self.top, (0, y))
            elif row == self.horizon:
                surface.blit(self.middle, (0, y))
            else:
                surface.blit(self.bottom, (0, y))

        if self.style == 'overworld':
            for palm_surf, palm_rect in self.palms:
                surface.blit(palm_surf, palm_rect)
            for cloud_surf, cloud_rect in self.clouds:
                surface.blit(cloud_surf, cloud_rect)


class Water:
    # the water needs to stretch more than the level width
    # both to the left and to the right
    def __init__(self, top, level_width, groups: List[pygame.sprite.Group]) -> None:
        water_start = -SCREEN_WIDTH
        water_tile_width = 192
        tile_x_amount = (level_width + SCREEN_WIDTH) // water_tile_width

        for tile in range(tile_x_amount):
            x = tile * water_tile_width + water_start
            y = top
            sprite = AnimatedTile((x, y), water_tile_width,
                                  'assets/graphics/decoration/water', groups)


class Clouds:
    def __init__(self, horizon, level_width, cloud_number, groups: List[pygame.sprite.Group]) -> None:
        cloud_surface_list = import_folder('assets/graphics/decoration/clouds')
        min_x = -SCREEN_WIDTH
        max_x = level_width + SCREEN_WIDTH
        min_y = 0
        max_y = horizon

        for _ in range(cloud_number):
            cloud_surface = choice(cloud_surface_list)
            x = randint(min_x, max_x)
            y = randint(min_y, max_y)
            StaticTile((x, y), 0, cloud_surface, groups)


if __name__ == '__main__':
    from main import main
    main()
