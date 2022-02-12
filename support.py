from os import walk
from os.path import join
import sys
from typing import List
from csv import reader

from settings import tile_size

import pygame


def resource_path(relative):
    if hasattr(sys, "_MEIPASS"):
        return join(sys._MEIPASS, relative)
    return join(relative)


def import_folder(path) -> List[pygame.Surface]:
    path = resource_path(path)
    surface_list = []

    for _, __, img_files in walk(path):
        for image in img_files:
            full_path = join(path, image)
            image_surface = pygame.image.load(
                resource_path(full_path)).convert_alpha()
            surface_list.append(image_surface)

    return surface_list


def import_csv_layout(path):
    path = resource_path(path)
    terrain_map = []
    with open(path) as map:
        level = reader(map, delimiter=',')
        for row in level:
            terrain_map.append(list(row))
    return terrain_map


def import_cut_graphics(path):
    path = resource_path(path)
    surface = pygame.image.load(resource_path(path)).convert_alpha()
    tile_num_x = surface.get_width()//tile_size
    tile_num_y = surface.get_height()//tile_size

    cut_tiles = []

    for row in range(tile_num_y):
        for col in range(tile_num_x):
            x = col * tile_size
            y = row * tile_size
            new_surface = pygame.Surface(
                (tile_size, tile_size), flags=pygame.SRCALPHA)
            new_surface.blit(surface, (0, 0), pygame.Rect(
                x, y, tile_size, tile_size))
            cut_tiles.append(new_surface)

    return cut_tiles


if __name__ == '__main__':
    from main import main
    main()
