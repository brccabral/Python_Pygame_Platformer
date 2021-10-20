from typing import Callable
import pygame
from game_data import levels
from support import import_folder, resource_path
from decoration import Sky

class Overworld:
    def __init__(self, start_level: int, max_level: int, surface: pygame.Surface, create_level: Callable) -> None:
        
        # setup
        self.display_surface = surface
        self.max_level = max_level
        self.current_level = start_level
        self.create_level = create_level

        # movement logic
        self.move_direction = pygame.math.Vector2(0,0)
        self.speed = 8
        self.moving = False

        # sprites
        self.icon = pygame.sprite.GroupSingle()
        self.setup_nodes()
        self.setup_icon()
        self.sky = Sky(8, 'overworld')

        # time
        self.start_time = pygame.time.get_ticks()
        self.allow_input = False
        self.timer_duration = 500

    def setup_nodes(self):
        self.nodes = pygame.sprite.Group()
        for index, node_data in enumerate(levels.values()):
            if index <= self.max_level:
                node_sprite = Node(node_data['node_pos'], 'available', self.speed, node_data['node_graphics'])
            else:
                node_sprite = Node(node_data['node_pos'], 'locked', self.speed, node_data['node_graphics'])
            self.nodes.add(node_sprite)

    def setup_icon(self):
        icon_sprite = Icon(self.nodes.sprites()[self.current_level].rect.center)
        self.icon.add(icon_sprite)

    def draw_paths(self):
        if self.max_level > 0:
            points = [node['node_pos'] for index, node in enumerate(levels.values()) if index <= self.max_level]
            pygame.draw.lines(self.display_surface, '#a04f45', False, points, 6)
        points = [node['node_pos'] for index, node in enumerate(levels.values()) if index >= self.max_level]
        if len(points) > 0:
            pygame.draw.lines(self.display_surface, 'black', False, points, 6)

    def input(self):
        keys = pygame.key.get_pressed()
        if not self.moving and self.allow_input:
            if keys[pygame.K_RIGHT] and self.current_level < self.max_level:
                self.move_direction = self.get_movement_data(1)
                self.current_level += 1
                self.moving = True
            elif keys[pygame.K_LEFT] and self.current_level > 0:
                self.move_direction = self.get_movement_data(-1)
                self.current_level -= 1
                self.moving = True
            elif keys[pygame.K_SPACE]:
                self.create_level(self.current_level)

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

    def input_timer(self):
        if not self.allow_input:
            current_time = pygame.time.get_ticks()
            if current_time - self.start_time >= self.timer_duration:
                self.allow_input = True

    def run(self):
        self.input_timer()
        self.input()
        self.sky.draw(self.display_surface)
        self.icon.update()
        self.update_icon_pos()
        self.draw_paths()
        self.nodes.update()
        self.nodes.draw(self.display_surface)
        self.icon.draw(self.display_surface)



class Node(pygame.sprite.Sprite):
    def __init__(self, pos, status, icon_speed, path) -> None:
        # icon_speed is used to detect the stop point
        super().__init__()
        self.frames = import_folder(path)
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.status = status
        
        self.rect = self.image.get_rect(center = pos)
        
        # stop point
        self.detection_zone = pygame.Rect(self.rect.centerx - (icon_speed//2), self.rect.centery - (icon_speed//2), icon_speed, icon_speed)

    def animate(self):
        self.frame_index += 0.15
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]
    
    def update(self) -> None:
        super().update()
        if self.status == 'available':
            self.animate()
        else:
            tint_surface = self.image.copy()
            tint_surface.fill('black', None, pygame.BLEND_RGB_MULT)
            self.image.blit(tint_surface, (0,0))

class Icon(pygame.sprite.Sprite):
    '''
    Icon class is the user selection, the hat of the player
    '''
    def __init__(self, pos) -> None:
        super().__init__()
        self.pos = pos
        self.image = pygame.image.load(resource_path('assets/graphics/overworld/hat.png')).convert_alpha()
        self.rect = self.image.get_rect(center = pos)
    
    def update(self):
        self.rect.center = self.pos