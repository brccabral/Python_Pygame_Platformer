from typing import List
import pygame
from tiles import AnimatedTile
from random import randint


class Enemy(AnimatedTile):
    def __init__(self, pos, size, groups: List[pygame.sprite.Group], constrains: pygame.sprite.Group) -> None:
        super().__init__(pos, size, 'assets/graphics/enemy/run', groups)
        self.rect.y += size - self.image.get_height()
        self.speed = randint(3, 6)
        self.constrains = constrains

    def move(self):
        self.rect.x += self.speed

    def reverse_image(self):
        if self.speed > 0:
            self.image = pygame.transform.flip(
                self.image, flip_x=True, flip_y=False)

    def constraint_collision(self):
        for sprite in self.constrains.sprites():
            if sprite.rect.colliderect(self.rect):
                self.reverse()
                # break avoids colliding twice when one constrain is right above the other
                break

    def run(self):
        self.animate()
        self.move()
        self.constraint_collision()
        self.reverse_image()

    def reverse(self):
        self.speed *= -1


if __name__ == '__main__':
    from main import main
    main()
