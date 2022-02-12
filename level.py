import pygame
from decoration import Clouds, Sky, Water
from enemy import Enemy
from player import Player
from tiles import Coin, Crate, Palm, StaticTile, Tile
from settings import TILE_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT, CAMERA_BORDERS
from support import import_csv_layout, import_cut_graphics, resource_path
from typing import Callable, List
from game_data import levels


class Level:
    def __init__(self, current_level: int, surface: pygame.Surface, create_overworld: Callable, change_coins: Callable, change_health: Callable) -> None:

        # general setup
        self.display_surface = surface
        self.current_level = current_level
        self.world_shift = 0

        # sprite group setup
        # sprites in this group will be diplayed, other won't
        self.visible_sprites = CameraGroup()
        # sprites in this group will be updated, others will remain static
        self.active_sprites = ActiveGroup()
        # sprites in this group will collide with player
        self.collision_sprites = pygame.sprite.Group()
        # sprites in this group will constrain enemies
        self.enemy_constrains = pygame.sprite.Group()

        # level setup
        level_data = levels[current_level]
        level_content = level_data['content']  # level title
        self.new_max_level = level_data['unlock']
        self.create_overworld = create_overworld

        # level display
        self.font = pygame.font.Font(None, 40)
        self.text_surface = self.font.render(level_content, True, 'White')
        self.text_rect = self.text_surface.get_rect(
            center=(SCREEN_WIDTH//2, 20))

        # anything in background need to be added first
        # terrain_layout is needed to calculate decoration positions
        terrain_layout = import_csv_layout(level_data['terrain'])

        # decoration
        self.sky = Sky(8)
        level_width = len(terrain_layout[0]) * TILE_SIZE
        self.water = Water(SCREEN_HEIGHT - 20, level_width,
                           [self.visible_sprites])
        self.clouds = Clouds(400, level_width, 20, [self.visible_sprites])

        # background palms setup
        bg_palms_layout = import_csv_layout(level_data['bg_palms'])
        self.create_tile_group(bg_palms_layout, 'bg_palms')

        # terrain setup
        self.create_tile_group(terrain_layout, 'terrain')

        # grass setup
        grass_layout = import_csv_layout(level_data['grass'])
        self.create_tile_group(grass_layout, 'grass')

        # crates setup
        crates_layout = import_csv_layout(level_data['crates'])
        self.create_tile_group(crates_layout, 'crates')

        # crates setup
        coins_layout = import_csv_layout(level_data['coins'])
        self.coins_sprites = self.create_tile_group(coins_layout, 'coins')

        # foreground palms setup
        fg_palms_layout = import_csv_layout(level_data['fg_palms'])
        self.create_tile_group(fg_palms_layout, 'fg_palms')

        # enemy setup
        enemies_layout = import_csv_layout(level_data['enemies'])
        self.enemies_sprites = self.create_tile_group(
            enemies_layout, 'enemies')

        # constraint
        constraints_layout = import_csv_layout(level_data['constraints'])
        self.create_tile_group(constraints_layout, 'constraints')

        # player setup
        player_layout = import_csv_layout(level_data['player'])
        self.goal = self.create_tile_group(
            player_layout, 'player', change_health)

        # ui
        self.change_coins = change_coins
        # audio
        self.coin_sound = pygame.mixer.Sound(
            resource_path('assets/audio/effects/coin.wav'))
        # self.stomp_sound = pygame.mixer.Sound(
        #     resource_path('assets/audio/effects/stomp.wav'))

    def create_tile_group(self, layout: List, layout_type: str, change_health: Callable = None):
        sprite_group = pygame.sprite.Group()
        if layout_type == 'terrain':
            terrain_tile_list = import_cut_graphics(
                resource_path('assets/graphics/terrain/terrain_tiles.png'))
        if layout_type == 'grass':
            grass_tile_list = import_cut_graphics(resource_path(
                'assets/graphics/decoration/grass/grass.png'))

        for row_index, row in enumerate(layout):
            for column_index, cell in enumerate(row):
                x = column_index * TILE_SIZE
                y = row_index * TILE_SIZE
                if cell != '-1':
                    if layout_type == 'terrain':
                        tile_surface = terrain_tile_list[int(cell)]
                        StaticTile((x, y), TILE_SIZE, tile_surface, [
                                   self.visible_sprites, self.collision_sprites])
                    if layout_type == 'grass':
                        tile_surface = grass_tile_list[int(cell)]
                        StaticTile((x, y), TILE_SIZE, tile_surface,
                                   [self.visible_sprites])
                    if layout_type == 'crates':
                        Crate((x, y), TILE_SIZE, [
                              self.visible_sprites, self.collision_sprites])
                    if layout_type == 'coins':
                        if cell == '0':
                            sprite = Coin((x, y), TILE_SIZE, 'assets/graphics/coins/gold',
                                          5, [self.visible_sprites])
                        else:
                            sprite = Coin(
                                (x, y), TILE_SIZE, 'assets/graphics/coins/silver', 1, [self.visible_sprites])
                        sprite_group.add(sprite)
                    if layout_type == 'fg_palms':
                        if cell == '0':
                            Palm((x, y), TILE_SIZE, 'assets/graphics/terrain/palm_small',
                                 38, [self.visible_sprites, self.collision_sprites])
                        if cell == '1':
                            Palm((x, y), TILE_SIZE, 'assets/graphics/terrain/palm_large',
                                 64, [self.visible_sprites, self.collision_sprites])
                    if layout_type == 'bg_palms':
                        Palm((x, y), TILE_SIZE, 'assets/graphics/terrain/palm_bg',
                             64, [self.visible_sprites])
                    if layout_type == 'enemies':
                        sprite = Enemy((x, y), TILE_SIZE, [
                                       self.visible_sprites, self.active_sprites], self.enemy_constrains)
                        sprite_group.add(sprite)
                    if layout_type == 'constraints':
                        Tile((x, y), TILE_SIZE, [self.enemy_constrains])
                    if layout_type == 'player':
                        if cell == '0':
                            self.player = Player((x, y),
                                                 self.display_surface,
                                                 change_health,
                                                 [self.visible_sprites,
                                                     self.active_sprites],
                                                 self.collision_sprites,
                                                 self.enemies_sprites
                                                 )
                        if cell == '1':
                            hat_surface = pygame.image.load(resource_path(
                                'assets/graphics/character/hat.png')).convert_alpha()
                            sprite = StaticTile((x, y), TILE_SIZE, hat_surface, [
                                self.visible_sprites])
                            sprite_group.add(sprite)
        return sprite_group

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
        self.display_surface.blit(self.text_surface, self.text_rect)

        # player
        self.check_coin_collisions()

        self.active_sprites.run()
        self.visible_sprites.custom_draw(self.player)

        self.check_death()
        self.check_win()

    def check_death(self):
        if self.player.rect.top > SCREEN_HEIGHT:
            self.create_overworld(self.current_level, 0)

    def check_win(self):
        if pygame.sprite.spritecollide(self.player, self.goal, False):
            self.create_overworld(self.current_level, self.new_max_level)

    def check_coin_collisions(self):
        collided_coins: List[Coin] = pygame.sprite.spritecollide(
            self.player, self.coins_sprites, True)
        if collided_coins:
            self.coin_sound.play()
            for coin in collided_coins:
                self.change_coins(coin.value)


class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2(100, 300)

        # center camera setup
        # camera follows Player always
        # Player always on the center

        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2

        # box camera
        # camera moves if Player reaches border of screen

        camera_left = CAMERA_BORDERS['left']
        camera_top = CAMERA_BORDERS['top']
        camera_width = self.display_surface.get_size(
        )[0] - (camera_left + CAMERA_BORDERS['right'])
        camera_height = self.display_surface.get_size(
        )[1] - (camera_top + CAMERA_BORDERS['bottom'])

        self.camera_rect = pygame.Rect(
            camera_left, camera_top, camera_width, camera_height)

    def offset_from_player(self, player: Player):
        # player offset
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

    def offset_from_level(self, player: Player):

        # camera offset
        if player.rect.left < self.camera_rect.left:
            self.camera_rect.left = player.rect.left
        if player.rect.right > self.camera_rect.right:
            self.camera_rect.right = player.rect.right
        if player.rect.top < self.camera_rect.top:
            self.camera_rect.top = player.rect.top
        if player.rect.bottom > self.camera_rect.bottom:
            self.camera_rect.bottom = player.rect.bottom
        self.offset = pygame.math.Vector2(
            self.camera_rect.left - CAMERA_BORDERS['left'],
            self.camera_rect.top - CAMERA_BORDERS['top'])

    def custom_draw(self, player: Player):

        # self.offset_from_player(player)
        self.offset_from_level(player)

        for sprite in self.sprites():
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)


class ActiveGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

    def run(self):
        for sprite in self.sprites():
            sprite.run()


if __name__ == '__main__':
    from main import main
    main()
