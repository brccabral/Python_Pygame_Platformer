import pygame
from game_data import levels

class Overworld:
    def __init__(self, start_level: int, max_level: int, surface: pygame.Surface) -> None:
        
        # setup
        self.display_surface = surface
        self.max_level = max_level
        self.current_level = start_level

        # movement logic
        self.move_direction = pygame.math.Vector2(0,0)
        self.speed = 8
        self.moving = False

        # sprites
        self.icon = pygame.sprite.GroupSingle()
        self.setup_nodes()
        self.setup_icon()

    
    def setup_nodes(self):
        self.nodes = pygame.sprite.Group()
        for index, node_data in enumerate(levels.values()):
            if index <= self.max_level:
                node_sprite = Node(node_data['node_pos'], 'available', self.speed)
            else:
                node_sprite = Node(node_data['node_pos'], 'locked', self.speed)
            self.nodes.add(node_sprite)

    def setup_icon(self):
        icon_sprite = Icon(self.nodes.sprites()[self.current_level].rect.center)
        self.icon.add(icon_sprite)

    def draw_paths(self):
        points = [node['node_pos'] for index, node in enumerate(levels.values()) if index <= self.max_level]
        pygame.draw.lines(self.display_surface, 'red', False, points, 6)

    def input(self):
        keys = pygame.key.get_pressed()
        if not self.moving:
            if keys[pygame.K_RIGHT] and self.current_level < self.max_level:
                self.move_direction = self.get_movement_data(1)
                self.current_level += 1
                self.moving = True
            elif keys[pygame.K_LEFT] and self.current_level > 0:
                self.move_direction = self.get_movement_data(-1)
                self.current_level -= 1
                self.moving = True

    def get_movement_data(self, target: int) -> pygame.math.Vector2:
        start = pygame.math.Vector2(self.nodes.sprites()[self.current_level].rect.center)
        end = pygame.math.Vector2(self.nodes.sprites()[self.current_level + target].rect.center)

        return (end - start).normalize()

    def update_icon_pos(self):
        if self.moving:
            sprite: Icon = self.icon.sprite
            sprite.pos += self.move_direction * self.speed
            target_node: Node = self.nodes.sprites()[self.current_level]
            if target_node.detection_zone.collidepoint(sprite.pos):
                self.moving = False
                self.move_direction = pygame.math.Vector2(0,0)

    def run(self):
        self.input()
        self.icon.update()
        self.update_icon_pos()
        self.draw_paths()
        self.nodes.draw(self.display_surface)
        self.icon.draw(self.display_surface)



class Node(pygame.sprite.Sprite):
    def __init__(self, pos, status, icon_speed) -> None:
        # icon_speed is used to detect the stop point
        super().__init__()
        self.image = pygame.Surface((100,80))
        if status == 'available':
            self.image.fill('red')
        else:
            self.image.fill('grey')
        self.rect = self.image.get_rect(center = pos)
        
        # stop point
        self.detection_zone = pygame.Rect(self.rect.centerx - (icon_speed//2), self.rect.centery - (icon_speed//2), icon_speed, icon_speed)

class Icon(pygame.sprite.Sprite):
    '''
    Icon class is the user selection, the hat of the player
    '''
    def __init__(self, pos) -> None:
        super().__init__()
        self.pos = pos
        self.image = pygame.Surface((20,20))
        self.image.fill('blue')
        self.rect = self.image.get_rect(center = pos)
    
    def update(self):
        self.rect.center = self.pos