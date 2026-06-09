import pygame

import config as cfg


class StatusBar(pygame.sprite.Sprite):
    def __init__(self, groups: pygame.sprite.Group) -> None:
        super().__init__(groups)
        self.image = pygame.Surface(cfg.STATUS_BAR.size, pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        pygame.draw.rect(self.image, cfg.COLOR["STATUS_BG"], self.rect, border_radius=10)
        self.rect.topleft = cfg.STATUS_BAR.topleft
