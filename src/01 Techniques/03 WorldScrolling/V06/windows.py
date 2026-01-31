from typing import Union

import pygame
import config as cfg


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
        a = [r for r in self.mobs.sprites() if cfg.WINDOW.colliderect(r.rect)]
        for sprite in a:
            self.screen.blit(sprite.image, sprite.rect) 
        self.window.flip()

    def save(self):
        pygame.image.save(self.screen, "plain_image.png")


class WindowBirdEyeView:

    def __init__(self, tiles:pygame.sprite.Group, mobs:pygame.sprite.Group) -> None:
        self.tiles = tiles
        self.mobs = mobs

        self.zoom = cfg.ZOOM_BIRDEYE
        self.window = pygame.Window(size=cfg.WINDOW.size)
        self.window.position = (1 * (cfg.WINDOW.width + 60), 
                                0 * (cfg.WINDOW.height) + 30)
        self.screen : pygame.surface.Surface = self.window.get_surface()
        self.rect = self.screen.get_frect()
        self.window.title = f"Birdeye (zoom=({self.zoom.x:0.2f}, {self.zoom.y:0.2f})"
        self.clock = pygame.time.Clock()

    def draw(self, rects:list):
        for sprite in self.tiles:
            self.screen.blit(sprite.image_small, self.zoom_rect(sprite.rect))
        for sprite in self.mobs:
            self.screen.blit(sprite.image_small, self.zoom_rect(sprite.rect))
        if rects:       # Are rects to draw?
            for item in rects:
                pygame.draw.rect(self.screen, item["color"], self.zoom_rect(item["rect"]), 2)
        self.window.flip()

    def zoom_rect(self, rect: Union[pygame.rect.Rect, pygame.rect.FRect]) -> pygame.rect.FRect:
        x = rect.x * self.zoom.x
        y = rect.y * self.zoom.y
        w = rect.w * self.zoom.x
        h = rect.h * self.zoom.y
        return pygame.rect.FRect(x, y, w, h)

    def save(self):
        pygame.image.save(self.screen, "birdeye_image.png")


class WindowCenteredCamera:

    def __init__(self, player:pygame.sprite.Sprite, tiles:pygame.sprite.Group, mobs:pygame.sprite.Group) -> None:
        self.tiles = tiles
        self.mobs = mobs
        self.player = player
        self.offset = pygame.Vector2(0, 0) #
        self.window = pygame.Window(size=cfg.WINDOW.size)
        self.window.position = (2 * (cfg.WINDOW.width + 60), 
                                0 * (cfg.WINDOW.height) + 30)
        self.screen : pygame.surface.Surface = self.window.get_surface()
        self.rect = self.screen.get_frect()
        self.clock = pygame.time.Clock()

    def draw(self):
        self.screen.fill("Black")
        a = [r for r in self.tiles.sprites() if cfg.WINDOW.colliderect(self.world2camera(r.rect))]
        for sprite in a:
            self.screen.blit(sprite.image, self.world2camera(sprite.rect)) 
        a = [r for r in self.mobs.sprites() if cfg.WINDOW.colliderect(self.world2camera(r.rect))]
        for sprite in a:
            self.screen.blit(sprite.image, self.world2camera(sprite.rect))
        self.window.flip()

    def save(self):
        pygame.image.save(self.screen, "centered_image.png")

    def scroll(self) -> None:
        # Clamp left/top so we do not scroll past the world edges
        self.offset.x = max(0, self.player.rect.x - self.rect.width / 2)
        self.offset.y = max(0, self.player.rect.y - self.rect.height / 2)

        # Clamp right/bottom so we do not scroll past the world edges
        self.offset.x = min(cfg.WORLD.right - self.rect.width, self.offset.x)
        self.offset.y = min(cfg.WORLD.bottom - self.rect.height, self.offset.y)

        self.rect.topleft = self.offset

    def world2camera(self, rect: pygame.rect.FRect) -> pygame.rect.FRect:
        return pygame.rect.FRect(rect.topleft - self.offset, rect.size)
