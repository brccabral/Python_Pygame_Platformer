from typing import Callable, List
import pygame
from particles import ParticleEffect
from support import import_folder, resource_path
from math import sin


class Player(pygame.sprite.Sprite):
    def __init__(self,
                 pos,
                 surface: pygame.Surface,
                 change_health: Callable,
                 groups: List[pygame.sprite.Group],
                 collisions_sprites: pygame.sprite.Group
                 ) -> None:
        super().__init__(groups)
        self.import_character_assets()
        self.frame_index = 0
        self.animation_speed = 0.15
        self.image = self.animations['idle'][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)
        self.display_surface = surface

        # player movement
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 8
        self.gravity = 1
        self.jump_speed = -25
        # separate sword pixels from collision rectangle
        self.collision_rect = pygame.Rect(
            self.rect.topleft, (50, self.rect.height))
        self.collisions_sprites = collisions_sprites

        # player status
        self.status = 'idle'
        self.facing_right = True
        self.on_floor = True

        # health management
        self.change_health = change_health
        self.invincible = False
        self.invincibility_duration = 500
        self.hurt_time = 0

        # dust particles
        self.import_dust_run_particles()
        self.dust_frame_index = 0
        self.dust_animation_speed = 0.15

        # audio
        self.jump_sound = pygame.mixer.Sound(
            resource_path('assets/audio/effects/jump.wav'))
        self.jump_sound.set_volume(0.5)
        self.hit_sound = pygame.mixer.Sound(
            resource_path('assets/audio/effects/hit.wav'))

    def import_character_assets(self):
        character_path = 'assets/graphics/character/'
        self.animations: dict[str, List[pygame.Surface]] = {
            'idle': [], 'run': [], 'jump': [], 'fall': []}

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    def import_dust_run_particles(self):
        self.dust_run_particles = import_folder(
            'assets/graphics/character/dust_particles/run')

    def animate(self):
        animation = self.animations[self.status]

        # loop over frame index
        self.frame_index += self.animation_speed
        if self.frame_index > len(animation):
            self.frame_index = 0

        image = animation[int(self.frame_index)]
        if self.facing_right:
            self.image = image
            self.rect.bottomleft = self.collision_rect.bottomleft
        else:
            flipped_image = pygame.transform.flip(image, True, False)
            self.image = flipped_image
            self.rect.bottomright = self.collision_rect.bottomright

        if self.invincible:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

        self.rect = self.image.get_rect(midbottom=(self.rect.midbottom))

    def run_dust_animation(self):
        if self.status == 'run' and self.on_floor:
            self.dust_frame_index += self.dust_animation_speed
            if self.dust_frame_index >= len(self.dust_run_particles):
                self.dust_frame_index = 0

            dust_particle = self.dust_run_particles[int(self.dust_frame_index)]

            if self.facing_right:
                pos = self.rect.bottomleft - pygame.math.Vector2(6, 10)
                self.display_surface.blit(dust_particle, pos)
            else:
                pos = self.rect.bottomright - pygame.math.Vector2(6, 10)
                flipped_dust_particle = pygame.transform.flip(
                    dust_particle, True, False)
                self.display_surface.blit(flipped_dust_particle, pos)

    def get_damage(self):
        if not self.invincible:
            self.change_health(-10)
            self.invincible = True
            self.hurt_time = pygame.time.get_ticks()
            self.hit_sound.play()

    def invincibility_timer(self):
        if self.invincible:
            current_time = pygame.time.get_ticks()
            if current_time - self.hurt_time >= self.invincibility_duration:
                self.invincible = False

    def wave_value(self):
        value = sin(pygame.time.get_ticks())
        if value >= 0:
            return 255
        else:
            return 0

    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.facing_right = True
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.facing_right = False
        else:
            self.direction.x = 0

        # player jumps only if on the ground
        if keys[pygame.K_SPACE] and self.on_floor:
            self.jump()

    def get_status(self):
        if self.direction.y < 0:
            self.status = 'jump'
        elif self.direction.y > self.gravity:
            self.status = 'fall'
        else:
            if self.direction.x != 0:
                self.status = 'run'
            else:
                self.status = 'idle'

    def apply_gravity(self):
        # contantly updates direction.y to get acceleration sensation
        self.direction.y += self.gravity
        # here we change the player position
        self.collision_rect.y += self.direction.y

    def jump(self):
        self.direction.y = self.jump_speed
        self.jump_sound.play()
        pos = self.rect.midbottom
        if self.facing_right:
            pos -= pygame.math.Vector2(15, 5)
        else:
            pos += pygame.math.Vector2(5, 5)
        ParticleEffect(pos, 'jump', self.groups())

    def horizontal_collisions(self):
        self.collision_rect.x += self.direction.x * self.speed
        for sprite in self.collisions_sprites.sprites():
            if sprite.rect.colliderect(self.collision_rect):
                if self.direction.x < 0:
                    self.collision_rect.left = sprite.rect.right
                if self.direction.x > 0:
                    self.collision_rect.right = sprite.rect.left

    def vertical_collisions(self):
        for sprite in self.collisions_sprites.sprites():
            if sprite.rect.colliderect(self.collision_rect):
                if self.direction.y > 0:
                    self.collision_rect.bottom = sprite.rect.top
                    self.direction.y = 0
                    self.on_floor = True
                if self.direction.y < 0:
                    self.collision_rect.top = sprite.rect.bottom
                    self.direction.y = 0
        if self.on_floor and self.direction.y != 0:
            self.on_floor = False

    def run(self):
        self.get_input()
        # self.get_status()
        self.animate()
        self.run_dust_animation()
        self.invincibility_timer()
        self.horizontal_collisions()
        self.apply_gravity()
        self.vertical_collisions()


if __name__ == '__main__':
    from main import main
    main()
