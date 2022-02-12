from typing import List
import pygame

from support import resource_path, import_folder


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, size, groups: List[pygame.sprite.Group]) -> None:
        super().__init__(groups)
        self.image = pygame.Surface((size, size))
        # self.image.fill('grey')
        self.rect = self.image.get_rect(topleft=pos)


class StaticTile(Tile):
    def __init__(self, pos, size, surface: pygame.Surface, groups: List[pygame.sprite.Group]) -> None:
        super().__init__(pos, size, groups)
        self.image = surface


class Crate(StaticTile):
    def __init__(self, pos, size, groups: List[pygame.sprite.Group]) -> None:
        super().__init__(pos, size, pygame.image.load(resource_path(
            'assets/graphics/terrain/crate.png')).convert_alpha(), groups)
        offset_y = pos[1] + size
        self.rect = self.image.get_rect(bottomleft=(pos[0], offset_y))


class AnimatedTile(Tile):
    def __init__(self, pos, size, path, groups: List[pygame.sprite.Group]) -> None:
        super().__init__(pos, size, groups)
        self.frames = import_folder(path)
        self.frame_index = 0
        self.image = self.frames[self.frame_index]

    def animate(self):
        self.frame_index += 0.15
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def update(self):
        self.animate()


class Coin(AnimatedTile):
    def __init__(self, pos, size, path, value, groups: List[pygame.sprite.Group]) -> None:
        super().__init__(pos, size, path, groups)
        cx = pos[0] + size // 2
        cy = pos[1] + size // 2
        self.rect = self.image.get_rect(center=(cx, cy))
        self.value = value


class Palm(AnimatedTile):
    def __init__(self, pos, size, path, offset, groups: List[pygame.sprite.Group]) -> None:
        super().__init__(pos, size, path, groups)
        offset_y = pos[1] - offset
        self.rect.topleft = (pos[0], offset_y)


if __name__ == '__main__':
    from main import main
    main()
