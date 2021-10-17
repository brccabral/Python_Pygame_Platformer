import pygame
from decoration import Clouds, Sky, Water
from enemy import Enemy
from particles import ParticleEffect
from player import Player
from tiles import Coin, Crate, Palm, StaticTile, Tile
from settings import tile_size, screen_width, screen_height
from support import import_csv_layout, import_cut_graphics, resource_path
from typing import Callable, List
from game_data import levels

class Level:
    def __init__(self, current_level: int, surface: pygame.Surface, create_overworld: Callable) -> None:

        # general setup
        self.display_surface = surface
        self.current_level = current_level
        self.world_shift = 0
        self.current_x = 0

        # level setup
        level_data = levels[current_level]
        level_content = level_data['content'] # level title
        self.new_max_level = level_data['unlock']
        self.create_overworld = create_overworld

        # level display
        self.font = pygame.font.Font(None, 40)
        self.text_surface = self.font.render(level_content, True, 'White')
        self.text_rect = self.text_surface.get_rect(center = (screen_width//2, screen_height//2))

        # terrain setup
        terrain_layout = import_csv_layout(level_data['terrain'])
        self.terrain_sprites: pygame.sprite.Group = self.create_tile_group(terrain_layout, 'terrain')
        self.tiles = pygame.sprite.Group()
        # self.setup_level_X(level_data)

        # grass setup
        grass_layout = import_csv_layout(level_data['grass'])
        self.grass_sprites: pygame.sprite.Group = self.create_tile_group(grass_layout, 'grass')
        
        # crates setup
        crates_layout = import_csv_layout(level_data['crates'])
        self.crates_sprites: pygame.sprite.Group = self.create_tile_group(crates_layout, 'crates')
        
        # crates setup
        coins_layout = import_csv_layout(level_data['coins'])
        self.coins_sprites: pygame.sprite.Group = self.create_tile_group(coins_layout, 'coins')
        
        # foreground palms setup
        fg_palms_layout = import_csv_layout(level_data['fg_palms'])
        self.fg_palms_sprites: pygame.sprite.Group = self.create_tile_group(fg_palms_layout, 'fg_palms')
        
        # background palms setup
        bg_palms_layout = import_csv_layout(level_data['bg_palms'])
        self.bg_palms_sprites: pygame.sprite.Group = self.create_tile_group(bg_palms_layout, 'bg_palms')

        # enemy setup
        enemies_layout = import_csv_layout(level_data['enemies'])
        self.enemies_sprites: pygame.sprite.Group = self.create_tile_group(enemies_layout, 'enemies')

        # constraint
        constraints_layout = import_csv_layout(level_data['constraints'])
        self.constraints_sprites: pygame.sprite.Group = self.create_tile_group(constraints_layout, 'constraints')

        # player setup
        player_layout = import_csv_layout(level_data['player'])
        self.player = pygame.sprite.GroupSingle()
        self.goal = pygame.sprite.GroupSingle()
        self.player_setup(player_layout)
        

        # dust
        # it is single because we can't have jump and land at the same time
        self.dust_sprite = pygame.sprite.GroupSingle()
        self.player_on_ground = False

        # decoration
        self.sky = Sky(8)
        level_width = len(terrain_layout[0]) * tile_size
        self.water = Water(screen_height - 20, level_width)
        self.clouds = Clouds(400, level_width, 20)
    
    def player_setup(self, layout):
        for row_index, row in enumerate(layout):
            for column_index, cell in enumerate(row):
                x = column_index * tile_size
                y = row_index * tile_size
                if cell == '0':
                    sprite = Player((x,y), self.display_surface, self.create_jump_particles)
                    self.player.add(sprite)
                if cell == '1':
                    hat_surface = pygame.image.load(resource_path('assets/graphics/character/hat.png')).convert_alpha()
                    sprite = StaticTile((x,y), tile_size, hat_surface)
                    self.goal.add(sprite)

    def create_tile_group(self, layout: List, layout_type: str):
        sprite_group = pygame.sprite.Group()
        if layout_type == 'terrain':
            terrain_tile_list = import_cut_graphics(resource_path('assets/graphics/terrain/terrain_tiles.png'))
        if layout_type == 'grass':
            grass_tile_list = import_cut_graphics(resource_path('assets/graphics/decoration/grass/grass.png'))
        
        for row_index, row in enumerate(layout):
            for column_index, cell in enumerate(row):
                x = column_index * tile_size
                y = row_index * tile_size
                if cell != '-1':
                    if layout_type == 'terrain':
                        tile_surface = terrain_tile_list[int(cell)]
                        sprite = StaticTile((x,y), tile_size, tile_surface)
                    if layout_type == 'grass':
                        tile_surface = grass_tile_list[int(cell)]
                        sprite = StaticTile((x,y), tile_size, tile_surface)
                    if layout_type == 'crates':
                        sprite = Crate((x,y), tile_size)
                    if layout_type == 'coins':
                        if cell == '0':
                            sprite = Coin((x,y), tile_size, 'assets/graphics/coins/gold')
                        else:
                            sprite = Coin((x,y), tile_size, 'assets/graphics/coins/silver')
                    if layout_type == 'fg_palms':
                        if cell == '0': sprite = Palm((x,y), tile_size, 'assets/graphics/terrain/palm_small', 38)
                        if cell == '1': sprite = Palm((x,y), tile_size, 'assets/graphics/terrain/palm_large', 64)
                    if layout_type == 'bg_palms':
                        sprite = Palm((x,y), tile_size, 'assets/graphics/terrain/palm_bg', 64)
                    if layout_type == 'enemies':
                        sprite = Enemy((x,y), tile_size)
                    if layout_type == 'constraints':
                        sprite = Tile((x,y), tile_size)

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

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            # unlocks new level
            self.create_overworld(self.current_level, self.new_max_level)
        if keys[pygame.K_ESCAPE]:
            # keep new level unchanged
            self.create_overworld(self.current_level, 0)

    def run(self):
        self.input()
        self.sky.draw(self.display_surface)
        self.clouds.draw(self.display_surface, self.world_shift)
        self.display_surface.blit(self.text_surface, self.text_rect)

        # level tiles
        self.tiles.update(self.world_shift)
        self.tiles.draw(self.display_surface)
        self.bg_palms_sprites.update(self.world_shift)
        self.bg_palms_sprites.draw(self.display_surface)
        self.terrain_sprites.update(self.world_shift)
        self.terrain_sprites.draw(self.display_surface)
        self.enemies_sprites.update(self.world_shift)
        self.enemies_sprites.draw(self.display_surface)
        self.constraints_sprites.update(self.world_shift) # don't draw constraints
        self.enemy_constraint_collision()
        self.crates_sprites.update(self.world_shift)
        self.crates_sprites.draw(self.display_surface)
        self.grass_sprites.update(self.world_shift)
        self.grass_sprites.draw(self.display_surface)
        self.coins_sprites.update(self.world_shift)
        self.coins_sprites.draw(self.display_surface)
        self.fg_palms_sprites.update(self.world_shift)
        self.fg_palms_sprites.draw(self.display_surface)


        # player
        self.horizontal_movement_collision()
        self.get_player_on_ground() # this needs to be before vertical collision
        self.vertical_movement_collision()
        self.create_landing_dust() # this needs to be after vertical collision
        self.player.update()
        self.player.draw(self.display_surface)
        self.goal.update(self.world_shift)
        self.goal.draw(self.display_surface)

        # dust particles
        self.dust_sprite.update(self.world_shift)
        self.dust_sprite.draw(self.display_surface)

        self.water.draw(self.display_surface, self.world_shift)

        self.scroll_x()

    def horizontal_movement_collision(self):
        player: Player = self.player.sprite
        player.rect.x += player.direction.x * player.speed

        collidable_sprites = self.terrain_sprites.sprites() + self.crates_sprites.sprites() + self.fg_palms_sprites.sprites()
        for sprite in collidable_sprites:
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

        collidable_sprites = self.terrain_sprites.sprites() + self.crates_sprites.sprites() + self.fg_palms_sprites.sprites()
        for sprite in collidable_sprites:
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

    def enemy_constraint_collision(self):
        enemy: Enemy
        for enemy in self.enemies_sprites.sprites():
            if pygame.sprite.spritecollide(enemy, self.constraints_sprites, dokill=False):
                enemy.reverse()



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