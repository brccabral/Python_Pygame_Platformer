import pygame
from game_data import levels

class Overworld:
    def __init__(self, start_level: int, max_level: int, surface: pygame.Surface) -> None:
        
        # setup
        self.display_surface = surface
        self.max_level = max_level
        self.current_level = start_level

        # sprites
        self.setup_nodes()
    
    def setup_nodes(self):
        self.nodes = pygame.sprite.Group()
        for node_data in levels.values():
            node_sprite = Node(node_data['node_pos'])
            self.nodes.add(node_sprite)

    def run(self):
        self.nodes.draw(self.display_surface)

class Node(pygame.sprite.Sprite):
    def __init__(self, pos) -> None:
        super().__init__()
        self.image = pygame.Surface((100,80))
        self.image.fill('red')
        self.rect = self.image.get_rect(center = pos)