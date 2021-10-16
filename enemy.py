import pygame
from tiles import AnimatedTile
from random import randint

class Enemy(AnimatedTile):
    def __init__(self, pos, size) -> None:
        super().__init__(pos, size, 'assets/graphics/enemy/run')
        self.rect.y += size - self.image.get_height()
        self.speed = randint(3,6)

    def move(self):
        self.rect.x += self.speed
    
    def reverse_image(self):
        if self.speed > 0:
            self.image = pygame.transform.flip(self.image, flip_x=True, flip_y=False)

    def update(self, x_shift):
        super().update(x_shift)
        self.animate()
        self.move()
        self.reverse_image()
    
    def reverse(self):
        self.speed *= -1