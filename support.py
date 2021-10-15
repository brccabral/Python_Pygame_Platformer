from os import walk
from os.path import join
import sys

import pygame

def resource_path(relative):
    if hasattr(sys, "_MEIPASS"):
        return join(sys._MEIPASS, relative)
    return join(relative)

def import_folder(path):
    surface_list = []
    
    for _,__,img_files in walk(path):
        for image in img_files:
            full_path = join(path, image)
            image_surface = pygame.image.load(resource_path(full_path)).convert_alpha()
            surface_list.append(image_surface)
    
    return surface_list

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((5, 5))
    print(import_folder('assets/graphics/character/run'))