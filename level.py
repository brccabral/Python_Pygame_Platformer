import pygame
from particles import ParticleEffect
from player import Player
from tiles import StaticTile, Tile
from settings import tile_size, screen_width
from support import import_csv_layout, import_cut_graphics
from typing import List

class Level:
    def __init__(self, level_data, surface: pygame.Surface) -> None:

        # general setup
        self.display_surface = surface
        self.world_shift = 0
        self.current_x = 0

        # terrain setup
        terrain_layout = import_csv_layout(level_data['terrain'])
        self.terrain_sprites: pygame.sprite.Group = self.create_tile_group(terrain_layout, 'terrain')
        self.tiles = pygame.sprite.Group()
        # self.setup_level_X(level_data)

        # grass setup
        grass_layout = import_csv_layout(level_data['grass'])
        self.grass_sprites: pygame.sprite.Group = self.create_tile_group(grass_layout, 'grass')

        # player setup
        self.player = pygame.sprite.GroupSingle()
        player_sprite: Player = Player((642,180), self.display_surface, self.create_jump_particles)
        self.player.add(player_sprite)

        # dust
        # it is single because we can't have jump and land at the same time
        self.dust_sprite = pygame.sprite.GroupSingle()
        self.player_on_ground = False
    
    def create_tile_group(self, layout: List, layout_type: str):
        sprite_group = pygame.sprite.Group()
        if layout_type == 'terrain':
            terrain_tile_list = import_cut_graphics('assets/graphics/terrain/terrain_tiles.png')
        if layout_type == 'grass':
            grass_tile_list = import_cut_graphics('assets/graphics/decoration/grass/grass.png')
        for row_index, row in enumerate(layout):
            for column_index, cell in enumerate(row):
                x = column_index * tile_size
                y = row_index * tile_size
                if cell != '-1':
                    if layout_type == 'terrain':
                        tile_surface = terrain_tile_list[int(cell)]
                    if layout_type == 'grass':
                        tile_surface = grass_tile_list[int(cell)]
                    sprite = StaticTile((x,y), tile_size, tile_surface)
                    sprite_group.add(sprite)
        return sprite_group

    def setup_level_X(self, layout):

        for row_index, row in enumerate(layout):
            for column_index, cell in enumerate(row):
                x = column_index * tile_size
                y = row_index * tile_size
                if cell == 'X':
                    tile = Tile((x,y), tile_size)
                    self.tiles.add(tile)
                if cell == 'P':
                    self.player.sprite.rect.bottomleft = (x,y)

    def scroll_x(self):
        player: Player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x

        if player_x < screen_width//4 and direction_x < 0:
            self.world_shift = 8
            player.speed = 0
        elif player_x > screen_width-(screen_width//4) and direction_x > 0:
            self.world_shift = -8
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = 8

    def run(self):
        # level tiles
        self.tiles.update(self.world_shift)
        self.tiles.draw(self.display_surface)
        self.terrain_sprites.update(self.world_shift)
        self.terrain_sprites.draw(self.display_surface)
        self.grass_sprites.update(self.world_shift)
        self.grass_sprites.draw(self.display_surface)

        # player
        self.horizontal_movement_collision()
        self.get_player_on_ground() # this needs to be before vertical collision
        self.vertical_movement_collision()
        self.create_landing_dust() # this needs to be after vertical collision
        self.player.update()
        self.player.draw(self.display_surface)

        # dust particles
        self.dust_sprite.update(self.world_shift)
        self.dust_sprite.draw(self.display_surface)

        self.scroll_x()

    def horizontal_movement_collision(self):
        player: Player = self.player.sprite
        player.rect.x += player.direction.x * player.speed

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                    player.on_right = True
                    self.current_x = sprite.rect.right
                    player.direction.x = 0
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left
                    player.on_left = True
                    self.current_x = sprite.rect.left
                    player.direction.x = 0
        
        # avoid image offset pixels due to different image sizes for the animation
        if player.on_left and (player.rect.left < self.current_x or player.direction.x >= 0):
            player.on_left = False
        if player.on_right and(player.rect.right > self.current_x or player.direction.x <= 0):
            player.on_right = False
    
    def vertical_movement_collision(self):
        player: Player = self.player.sprite
        player.apply_gravity()

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    # if player touches ceiling, stops player's jump
                    player.direction.y = 0
                    player.on_ceiling = True
                elif player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    # prevent from crossing the tile if player keeps standing on it
                    player.direction.y = 0
                    player.on_ground = True

        if player.on_ground and (player.direction.y < 0 or player.direction.y > player.gravity):
            player.on_ground = False
        if player.on_ceiling and player.direction.y > 0:
            player.on_ceiling = False

    def create_jump_particles(self, pos):
        if self.player.sprite.facing_right:
            pos -= pygame.math.Vector2(15,5)
        else:
            pos += pygame.math.Vector2(-5,5)
        jump_particle_sprite = ParticleEffect(pos, 'jump')
        self.dust_sprite.add(jump_particle_sprite)

    def get_player_on_ground(self):
        # save the on_ground state before the vertical collision
        # if there is a collision after, it means the player
        # was on the air
        self.player_on_ground = self.player.sprite.on_ground
    
    def create_landing_dust(self):
        # check if player was on the air before the vertical collision
        if not self.player_on_ground and self.player.sprite.on_ground and not self.dust_sprite.sprites():
            if self.player.sprite.facing_right:
                offset = pygame.math.Vector2(10,15)
            else:
                offset = pygame.math.Vector2(-10,15)
            fall_dust_particle = ParticleEffect(self.player.sprite.rect.midbottom - offset, 'land')
            self.dust_sprite.add(fall_dust_particle)