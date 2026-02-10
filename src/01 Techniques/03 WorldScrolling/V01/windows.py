import config as cfg
import pygame


class WindowPlain:

    def __init__(self, tiles:pygame.sprite.Group, mobs:pygame.sprite.Group) -> None:
        self.tiles = tiles
        self.mobs = mobs
        self.window = pygame.Window(size=cfg.WINDOW.size)
        self.window.position = (0 * (cfg.WINDOW.width + 60), 
                                0 * (cfg.WINDOW.height) + 30)
        self.screen : pygame.Surface = self.window.get_surface()
        self.rect = self.screen.get_frect()
        self.window.title = f"Plain Window (size={self.rect.size})"
        self.clock = pygame.time.Clock()

    def draw(self):
        self.tiles.draw(self.screen)
        self.mobs.draw(self.screen)
        self.window.flip()

    def save(self):
        pygame.image.save(self.screen, "plain_image.png")


