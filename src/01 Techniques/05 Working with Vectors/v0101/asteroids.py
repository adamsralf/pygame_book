from time import time
from typing import Any

import pygame

import config as cfg


class Asteroid(pygame.sprite.Sprite):

    def __init__(self) -> None:
        super().__init__()
        self.image = pygame.Surface((60, 60), pygame.SRCALPHA)
        points = [(18, 3), (40, 6), (56, 22), (48, 43),
                  (32, 56), (10, 48), (3, 27)]
        pygame.draw.polygon(self.image, cfg.MYCOLORS["asteroid"], points, 2)
        self.rect : pygame.FRect = self.image.get_frect()
        self.rect.center = (100, 450)
        self.speed = (200, -150)

    def update(self, *args: Any, **kwargs: Any) -> None:
        self.rect.move_ip(self.speed[0] * cfg.DELTATIME, self.speed[1] * cfg.DELTATIME)
        if self.rect.left > cfg.WINDOW.right:
            self.rect.right = cfg.WINDOW.left + 1
        elif self.rect.right < cfg.WINDOW.left:
            self.rect.left = cfg.WINDOW.right - 1
        if self.rect.top > cfg.WINDOW.bottom:
            self.rect.bottom = cfg.WINDOW.top + 1
        elif self.rect.bottom < cfg.WINDOW.top:
            self.rect.top = cfg.WINDOW.bottom - 1


class Game:

    def __init__(self) -> None:
        pygame.init()
        self.window = pygame.Window(size=cfg.WINDOW.size, title=cfg.TITLE)
        self.screen = self.window.get_surface()
        self.clock = pygame.time.Clock()
        self.asteroid = pygame.sprite.Group(Asteroid())
        self.running = False

    def run(self) -> None:
        time_previous = time()
        self.running = True
        while self.running:
            self.watch_for_events()
            self.update()
            self.draw()
            time_current = time()
            cfg.DELTATIME = time_current - time_previous
            time_previous = time_current
        pygame.quit()

    def watch_for_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_SPACE:
                    self.asteroid.add(Asteroid())

    def update(self) -> None:
        self.asteroid.update()

    def draw(self) -> None:
        self.screen.fill(cfg.MYCOLORS["background"])
        self.asteroid.draw(self.screen)
        self.window.flip()


def main():
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
