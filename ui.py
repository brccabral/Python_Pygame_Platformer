import pygame
from support import resource_path


class UI:
    def __init__(self, surface: pygame.Surface) -> None:
        # setup
        self.display_surface = surface

        # health
        self.health_bar = pygame.image.load(resource_path(
            'assets/graphics/ui/health_bar.png')).convert_alpha()
        self.health_bar_topleft = (54, 39)
        self.bar_max_width = 152
        self.bar_height = 4

        # coins
        self.coin = pygame.image.load(resource_path(
            'assets/graphics/ui/coin.png')).convert_alpha()
        self.coin_rect = self.coin.get_rect(topleft=(50, 61))
        self.font = pygame.font.Font(resource_path(
            'assets/graphics/ui/ARCADEPI.TTF'), 30)

    def show_health(self, current, full):
        # the health bar image is the background
        self.display_surface.blit(self.health_bar, (20, 10))
        # the actual health indicator is just a red rectangle on top of the health bar
        current_health_ratio = current/full
        current_bar_width = self.bar_max_width * current_health_ratio
        health_bar_rect = pygame.Rect(
            self.health_bar_topleft, (current_bar_width, self.bar_height))
        pygame.draw.rect(self.display_surface, '#dc4949', health_bar_rect)

    def show_coins(self, amount):
        self.display_surface.blit(self.coin, self.coin_rect)
        coin_amount_surface = self.font.render(str(amount), False, '#33323d')
        coin_amount_rect = coin_amount_surface.get_rect(
            midleft=(self.coin_rect.right + 4, self.coin_rect.centery))
        self.display_surface.blit(coin_amount_surface, coin_amount_rect)


if __name__ == '__main__':
    from main import main
    main()
