from time import time
from typing import Any

import config as cfg
import pygame


class Defender(pygame.sprite.Sprite):

    def __init__(self) -> None:
        super().__init__()
        self.image = pygame.image.load("images/defender01.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = pygame.FRect(self.image.get_rect())
        self.rect.centerx = cfg.WINDOW.centerx
        self.rect.bottom = cfg.WINDOW.height - 5
        self.speed = 300

    def update(self, *args: Any, **kwargs: Any) -> None:
        if "action" in kwargs.keys():
            if kwargs["action"] == "newpos":        # Compute new position§\label{srcInvader06e01}§
                self.rect.move_ip(self.speed * cfg.DELTATIME, 0)
            elif kwargs["action"] == "direction":   # Change direction§\label{srcInvader06e02}§
                self.change_direction()

    def change_direction(self) -> None:
        self.speed *= -1


class Border(pygame.sprite.Sprite):

    def __init__(self, leftright: str) -> None:
        super().__init__()
        self.image = pygame.image.load("images/brick01.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (35, cfg.WINDOW.height))
        self.rect = self.image.get_rect()
        if leftright == "right":
            self.rect.left = cfg.WINDOW.width - self.rect.width


class Game(object):

    def __init__(self) -> None:
        pygame.init()
        self.window = pygame.Window(size=cfg.WINDOW.size, title="Sprite", position=(10, 50))
        self.screen = self.window.get_surface()
        self.clock = pygame.time.Clock()

        self.defender = pygame.sprite.GroupSingle(Defender())
        self.all_border = pygame.sprite.Group()
        self.all_border.add(Border("left"))
        self.all_border.add(Border("right"))
        self.running = False

    def run(self) -> None:
        time_previous = time()
        self.running = True
        while self.running:
            self.watch_for_events()
            self.update()
            self.draw()
            self.clock.tick(cfg.FPS)
            time_current = time()
            cfg.DELTATIME = time_current - time_previous
            time_previous = time_current
        pygame.quit()

    def watch_for_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self) -> None:
        if pygame.sprite.spritecollide(self.defender.sprite, self.all_border, False):
            self.defender.update(action="direction")  # Better (don't aks - tell!)§\label{srcInvader06e03}§
        self.defender.update(action="newpos")

    def draw(self) -> None:
        self.screen.fill((255, 255, 255))
        self.defender.draw(self.screen)
        self.all_border.draw(self.screen)
        self.window.flip()


if __name__ == "__main__":
    game = Game()
    game.run()
