from typing import Union

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
        w = self.camera2world(cfg.WINDOW)
        a = [r for r in self.tiles.sprites() if w.colliderect(r.rect)]
        for sprite in a:
            self.screen.blit(sprite.image, self.world2camera(sprite.rect)) 
        a = [r for r in self.mobs.sprites() if w.colliderect(r.rect)]
        for sprite in a:
            self.screen.blit(sprite.image, self.world2camera(sprite.rect))
        self.window.flip()

    def save(self):
        pygame.image.save(self.screen, "centered_image.png")

    def scroll(self) -> None:
        self.offset.x = max(0, self.player.rect.x - self.rect.width / 2)
        self.offset.y = max(0, self.player.rect.y - self.rect.height / 2)
        self.offset.x = min(cfg.WORLD.right - self.rect.width, self.offset.x)
        self.offset.y = min(cfg.WORLD.bottom - self.rect.height, self.offset.y)

        self.rect.topleft = self.offset

    def world2camera(self, rect: pygame.rect.FRect) -> pygame.rect.FRect:
        return pygame.rect.FRect(rect.topleft - self.offset, rect.size)

    def camera2world(self, rect: pygame.rect.FRect) -> pygame.rect.FRect:
        return pygame.rect.FRect(rect.topleft + self.offset, rect.size)


class WindowPagewise:

    def __init__(self, player:pygame.sprite.Sprite, tiles:pygame.sprite.Group, mobs:pygame.sprite.Group, padding:int = 1) -> None:
        self.tiles = tiles
        self.mobs = mobs
        self.player = player
        self.offset = pygame.Vector2(0, 0) 
        self.window = pygame.Window(size=cfg.WINDOW.size)
        self.window.position = (0 * (cfg.WINDOW.width + 60), 
                                1 * (cfg.WINDOW.height) + 30)
        self.screen : pygame.surface.Surface = self.window.get_surface()
        self.rect = self.screen.get_frect()
        self.clock = pygame.time.Clock()
        self.inner_rect = pygame.rect.FRect(
            cfg.WINDOW.left + padding * player.rect.width,
            cfg.WINDOW.top + padding * player.rect.height,
            cfg.WINDOW.width - padding * 2 * player.rect.width,
            cfg.WINDOW.height - padding * 2 * player.rect.height,
        )

    def draw(self):
        self.screen.fill("Black")
        w = self.camera2world(cfg.WINDOW)
        a = [r for r in self.tiles.sprites() if w.colliderect(r.rect)]
        for sprite in a:
            self.screen.blit(sprite.image, self.world2camera(sprite.rect)) 
        a = [r for r in self.mobs.sprites() if w.colliderect(r.rect)]
        for sprite in a:
            self.screen.blit(sprite.image, self.world2camera(sprite.rect))
        self.window.flip()

    def save(self):
        pygame.image.save(self.screen, "pagewise_image.png")

    def scroll(self) -> None:
        player_in_view = self.world2camera(self.player.rect)
        if not player_in_view.colliderect(self.inner_rect):     # nicht mehr innerhalb?§\label{camerav0801}§
            self.offset.x = max(0, self.player.rect.x - cfg.WINDOW.centerx)
            self.offset.y = max(0, self.player.rect.y - cfg.WINDOW.centery)
            self.offset.x = min(cfg.WORLD.right - cfg.WINDOW.width, self.offset.x)
            self.offset.y = min(cfg.WORLD.bottom - cfg.WINDOW.height, self.offset.y)
        self.rect.topleft = self.offset

    def world2camera(self, rect: pygame.rect.FRect) -> pygame.rect.FRect:
        return pygame.rect.FRect(rect.topleft - self.offset, rect.size)

    def camera2world(self, rect: pygame.rect.FRect) -> pygame.rect.FRect:
        return pygame.rect.FRect(rect.topleft + self.offset, rect.size)

