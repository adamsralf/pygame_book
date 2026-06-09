import pygame

import config as cfg


class Letters(pygame.sprite.Sprite):
    def __init__(self, groups: pygame.sprite.Group) -> None:
        super().__init__(groups)
        self.image = pygame.Surface(cfg.LETTER_BAR.size, pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        font = pygame.font.SysFont("Arial", 20, bold=True)
        for col in range(cfg.NOF_COLS):
            text_surface = font.render(chr(65 + col), True, cfg.COLOR["LETTER_TEXT"])
            text_rect = text_surface.get_rect()
            text_rect.centerx = cfg.COIN_RADIUS * (col * 2 + 1)
            self.image.blit(text_surface, text_rect)
        self.rect.topleft = cfg.LETTER_BAR.topleft
