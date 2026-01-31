
import config as cfg
import pygame


class WindowPlain:

    def __init__(self, tiles:pygame.sprite.Group, mobs:pygame.sprite.Group) -> None:
        self.tiles = tiles
        self.mobs = mobs
        self.window = pygame.Window(size=cfg.WINDOW.size)
        self.window.position = (0 * (cfg.WINDOW.width + 60), 
                                0 * (cfg.WINDOW.height) + 30)
        self.screen : pygame.surface.Surface = self.window.get_surface()
        self.rect = self.screen.get_frect()
        self.window.title = f"Plain Window (size={self.rect.size})"
        self.clock = pygame.time.Clock()

    def draw(self):
        self.screen.fill("Black")
        a = [r for r in self.tiles.sprites() if cfg.WINDOW.colliderect(r.rect)]
        for sprite in a:
            self.screen.blit(sprite.image, sprite.rect) 
        #self.tiles.draw(self.screen_plain)
        a = [r for r in self.mobs.sprites() if cfg.WINDOW.colliderect(r.rect)]
        for sprite in a:
            self.screen.blit(sprite.image, sprite.rect) 
        #self.mobs.draw(self.screen_plain)
        self.window.flip()

    def save(self):
        pygame.image.save(self.screen, "plain_image.png")


class WindowBirdEyeView:

    def __init__(self, world_screen:pygame.surface.Surface) -> None:
        self.world_screen = world_screen
        zx = cfg.WINDOW.width / cfg.WORLD.width
        zy = cfg.WINDOW.height / cfg.WORLD.height
        self.zoom = pygame.Vector2(zx, zy)
        self.window = pygame.Window(size=cfg.WINDOW.size)
        self.window.position = (1 * (cfg.WINDOW.width + 60), 
                                0 * (cfg.WINDOW.height) + 30)
        self.screen : pygame.surface.Surface = self.window.get_surface()
        self.rect = self.screen.get_frect()
        self.window.title = f"Birdeye (zoom=({self.zoom.x:0.2f}, {self.zoom.y:0.2f})"

    def draw(self):
        image = pygame.transform.scale_by(self.world_screen, self.zoom) #§\label{windowsv0301}§
        self.screen.blit(image)
        self.window.flip()

    def save(self):
        pygame.image.save(self.screen, "birdeye_image.png")
