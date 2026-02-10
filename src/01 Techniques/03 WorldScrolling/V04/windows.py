from typing import Union

import config as xfg
import pygame


class WindowPlain:

    def __init__(self, tiles:pygame.sprite.Group, mobs:pygame.sprite.Group) -> None:
        self.tiles = tiles
        self.mobs = mobs
        self.window = pygame.Window(size=xfg.WINDOW.size)
        self.window.position = (0 * (xfg.WINDOW.width + 60), 
                                0 * (xfg.WINDOW.height) + 30)
        self.screen : pygame.Surface = self.window.get_surface()
        self.rect = self.screen.get_frect()
        self.window.title = f"Plain Window (size={self.rect.size})"
        self.clock = pygame.time.Clock()

    def draw(self):
        self.screen.fill("Black")
        a = [r for r in self.tiles.sprites() if xfg.WINDOW.colliderect(r.rect)]
        for sprite in a:
            self.screen.blit(sprite.image, sprite.rect) 
        a = [r for r in self.mobs.sprites() if xfg.WINDOW.colliderect(r.rect)]
        for sprite in a:
            self.screen.blit(sprite.image, sprite.rect) 
        self.window.flip()

    def save(self):
        pygame.image.save(self.screen, "plain_image.png")


class WindowBirdEyeView:

    def __init__(self, tiles:pygame.sprite.Group, mobs:pygame.sprite.Group) -> None:
        self.tiles = tiles
        self.mobs = mobs

        self.zoom = xfg.ZOOM_BIRDEYE                       
        self.window = pygame.Window(size=xfg.WINDOW.size)
        self.window.position = (1 * (xfg.WINDOW.width + 60), 
                                0 * (xfg.WINDOW.height) + 30)
        self.screen : pygame.Surface = self.window.get_surface()
        self.rect = self.screen.get_frect()
        self.window.title = f"Birdeye (zoom=({self.zoom.x:0.2f}, {self.zoom.y:0.2f})"
        self.clock = pygame.time.Clock()

    def draw(self, rects:list):
        for sprite in self.tiles:
            self.screen.blit(sprite.image_small, self.zoom_rect(sprite.rect))
        for sprite in self.mobs:
            self.screen.blit(sprite.image_small, self.zoom_rect(sprite.rect))
        if rects:                                               # Are rects to draw? §\label{windowsv0401}§
            for item in rects:
                pygame.draw.rect(self.screen, item["color"], self.zoom_rect(item["rect"]), 2)
        self.window.flip()

    def zoom_rect(self, rect: Union[pygame.Rect, pygame.FRect]) -> pygame.FRect:
        x = rect.x * self.zoom.x
        y = rect.y * self.zoom.y
        w = rect.w * self.zoom.x
        h = rect.h * self.zoom.y
        return pygame.FRect(x, y, w, h)

    def save(self):
        pygame.image.save(self.screen, "birdeye_image.png")

        
