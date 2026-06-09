import pygame

import config as cfg


class TitleBar(pygame.sprite.Sprite):
    def __init__(self, groups: pygame.sprite.Group) -> None:
        super().__init__(groups)
        self.image = pygame.Surface(cfg.TITLE_BAR.size, pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        pygame.draw.rect(self.image, cfg.COLOR["TITLE_BG"], self.rect, border_radius=10)

        font = pygame.font.SysFont("Arial", 24, bold=True)
        title = "Four Connect" + (" " * 45) + "© Ralf Adams 2026"
        text_surface = font.render(title, True, cfg.COLOR["TITLE_TEXT"])
        text_rect = text_surface.get_rect(center=self.rect.center)
        self.image.blit(text_surface, text_rect)

        self.rect.topleft = cfg.TITLE_BAR.topleft
