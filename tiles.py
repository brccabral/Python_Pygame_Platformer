import pygame

from support import resource_path

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, size) -> None:
        super().__init__()
        self.image = pygame.Surface((size, size))
        # self.image.fill('grey')
        self.rect = self.image.get_rect(topleft = pos)
    
    def update(self, x_shift):
        self.rect.x += x_shift

class StaticTile(Tile):
    def __init__(self, pos, size, surface: pygame.Surface) -> None:
        super().__init__(pos, size)
        self.image = surface

class Crate(StaticTile):
    def __init__(self, pos, size) -> None:
        super().__init__(pos, size, pygame.image.load(resource_path('assets/graphics/terrain/crate.png')).convert_alpha())
        offset_y = pos[1] + size
        self.rect = self.image.get_rect(bottomleft = (pos[0], offset_y))
