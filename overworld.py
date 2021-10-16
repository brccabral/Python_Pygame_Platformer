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
        self.setup_icon()
    
    def setup_nodes(self):
        self.nodes = pygame.sprite.Group()
        for index, node_data in enumerate(levels.values()):
            if index <= self.max_level:
                node_sprite = Node(node_data['node_pos'], 'available')
            else:
                node_sprite = Node(node_data['node_pos'], 'locked')
            self.nodes.add(node_sprite)

    def setup_icon(self):
        self.icon = pygame.sprite.GroupSingle()
        icon_sprite = Icon(self.nodes.sprites()[self.current_level].rect.center)
        self.icon.add(icon_sprite)

    def draw_paths(self):
        points = [node['node_pos'] for index, node in enumerate(levels.values()) if index <= self.max_level]
        pygame.draw.lines(self.display_surface, 'red', False, points, 6)

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] and self.current_level < self.max_level:
            self.current_level += 1
        elif keys[pygame.K_LEFT] and self.current_level > 0:
            self.current_level -= 1

    def update_icon_pos(self):
        self.icon.sprite.rect.center = self.nodes.sprites()[self.current_level].rect.center

    def run(self):
        self.input()
        self.update_icon_pos()
        self.draw_paths()
        self.nodes.draw(self.display_surface)
        self.icon.draw(self.display_surface)



class Node(pygame.sprite.Sprite):
    def __init__(self, pos, status) -> None:
        super().__init__()
        self.image = pygame.Surface((100,80))
        if status == 'available':
            self.image.fill('red')
        else:
            self.image.fill('grey')
        self.rect = self.image.get_rect(center = pos)

class Icon(pygame.sprite.Sprite):
    '''
    Icon class is the user selection, the hat of the player
    '''
    def __init__(self, pos) -> None:
        super().__init__()
        self.image = pygame.Surface((20,20))
        self.image.fill('blue')
        self.rect = self.image.get_rect(center = pos)