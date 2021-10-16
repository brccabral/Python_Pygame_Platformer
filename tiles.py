import pygame

from support import resource_path, import_folder

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

class AnimatedTile(Tile):
    def __init__(self, pos, size, path) -> None:
        super().__init__(pos, size)
        self.frames = import_folder(path)
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
    
    def animate(self):
        self.frame_index += 0.15
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]
    
    def update(self, x_shift):
        super().update(x_shift)
        self.animate()

class Coin(AnimatedTile):
    def __init__(self, pos, size, path) -> None:
        super().__init__(pos, size, path)
        cx = pos[0] + size // 2
        cy = pos[1] + size // 2
        self.rect = self.image.get_rect(center = (cx, cy))

class Palm(AnimatedTile):
    def __init__(self, pos, size, path) -> None:
        super().__init__(pos, size, path)