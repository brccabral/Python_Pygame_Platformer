from tiles import AnimatedTile

class Enemy(AnimatedTile):
    def __init__(self, pos, size) -> None:
        super().__init__(pos, size, 'assets/graphics/enemy/run')
        self.rect.y += size - self.image.get_height()
