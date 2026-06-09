import pygame

import config as cfg


class Coin(pygame.sprite.Sprite):
    def __init__(self, player: int, groups: pygame.sprite.Group) -> None:
        super().__init__(groups)
        self.rect = pygame.FRect(0, 0, cfg.COIN_RADIUS * 2, cfg.COIN_RADIUS * 2)
        self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.color = cfg.COLOR[f"PLAYER{player}"]
        self.player = player
        pygame.draw.circle(self.image, self.color, self.rect.center, cfg.COIN_RADIUS)
        self.rect.bottom = cfg.PLAYGROUND.top - cfg.MARGIN
        self.rect.centerx = cfg.PLAYGROUND.centerx
        self.colrow = (-1, -1)

    def draw(self, screen) -> None:
        col , row = self.colrow
        self.rect.center= (cfg.COIN_RADIUS*(col * 2 + 1) + cfg.MARGIN, cfg.COIN_RADIUS * (row * 2 + 1) + cfg.PLAYGROUND.top)
        screen.blit(self.image, self.rect)
