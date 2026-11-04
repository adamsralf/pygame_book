from random import choice, randint
from time import time
from typing import Any, ClassVar

import pygame

import config as cfg


class Asteroid(pygame.sprite.Sprite):

    SHAPES : ClassVar[list[tuple[int, list[tuple[int, int]]]]] = [
        (30, [(9, 2), (23, 4), (28, 14), (21, 27), (5, 24), (2, 12)]),
        (45, [(14, 2), (37, 5), (42, 20), (30, 25),
              (35, 40), (13, 42), (2, 25)]),
        (60, [(18, 3), (40, 6), (56, 22), (48, 43),
              (32, 56), (10, 48), (3, 27)]),
        (75, [(23, 3), (48, 8), (70, 25), (57, 38),
              (68, 56), (42, 71), (17, 62), (3, 35)]),
        (90, [(30, 3), (60, 7), (85, 28), (73, 47),
              (83, 65), (54, 86), (34, 70), (10, 78), (3, 34)]),
    ]

    def __init__(self, number : int) -> None:
        super().__init__()
        size, points = self.SHAPES[number]
        self.image = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.polygon(self.image, cfg.MYCOLORS["asteroid"], points, 2)
        self.rect : pygame.FRect = self.image.get_frect()
        self.rect.center = cfg.WINDOW.center
        self.speed = (choice((-1, 1)) * randint(250, 250),
                      choice((-1, 1)) * randint(250, 250))

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
        self.asteroid = pygame.sprite.Group()
        self.size_by_key = {
            pygame.K_1: 0,
            pygame.K_2: 1,
            pygame.K_3: 2,
            pygame.K_4: 3,
            pygame.K_5: 4,
        }
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
                    if len(self.asteroid) > 0:
                        self.asteroid.remove(self.asteroid.sprites()[0])
                elif event.key in (pygame.K_1, pygame.K_2, 
                                   pygame.K_3, pygame.K_4, 
                                   pygame.K_5):
                    self.asteroid.add(Asteroid(self.size_by_key.get(event.key)))

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
