import pygame

import config as cfg


class Playground(pygame.sprite.Sprite):
    def __init__(self, groups: pygame.sprite.Group) -> None:
        super().__init__(groups)
        self.image = pygame.Surface(cfg.PLAYGROUND.size, pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        pygame.draw.rect(self.image, cfg.COLOR["PLAYGROUND_BG"], self.rect, border_radius=10)
        for col in range(cfg.NOF_COLS):
            for row in range(cfg.NOF_ROWS):
                center = (cfg.COIN_RADIUS*(col * 2 + 1), cfg.COIN_RADIUS * (row * 2 + 1))
                pygame.draw.circle(self.image, cfg.COLOR["PLAYGROUND_HOLE"], center, cfg.COIN_RADIUS - 5)
        self.rect.topleft = cfg.PLAYGROUND.topleft

