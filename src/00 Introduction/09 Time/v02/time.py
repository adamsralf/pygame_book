from time import time
from typing import Any, Tuple

import pygame

import config as cfg


class Enemy(pygame.sprite.Sprite):

    def __init__(self, filename: str) -> None:
        super().__init__()
        self.image = pygame.image.load(cfg.imagepath(filename)).convert_alpha()
        self.rect = pygame.rect.FRect(self.image.get_rect())
        self.rect.topleft = (10, 10)
        self.direction = 1
        self.speed = pygame.math.Vector2(150, 0)

    def update(self, *args: Any, **kwargs: Any) -> None:
        newpos = self.rect.move(self.speed * cfg.DELTATIME * self.direction)
        if newpos.left < 10 or newpos.right >= cfg.WINDOW.right - 10:
            self.direction *= -1
        else:
            self.rect = newpos


class Bullet(pygame.sprite.Sprite):

    def __init__(self, picturefile: str, startpos: Tuple[int, int]) -> None:
        super().__init__()
        self.image = pygame.image.load(cfg.imagepath(picturefile)).convert_alpha()
        self.rect = pygame.rect.FRect(self.image.get_rect())
        self.rect.center = startpos
        self.direction = 1
        self.speed = pygame.math.Vector2(0, 100)

    def update(self, *args: Any, **kwargs: Any) -> None:
        self.rect.move_ip(self.speed * cfg.DELTATIME * self.direction)
        if self.rect.top > cfg.WINDOW.bottom - 30:
            self.kill()


class Game(object):

    def __init__(self) -> None:
        pygame.init()
        self.window = pygame.Window(size=cfg.WINDOW.size, title=cfg.TITLE)
        self.screen = self.window.get_surface()
        self.clock = pygame.time.Clock()

        self.enemy = pygame.sprite.GroupSingle(Enemy("alienbig1.png"))
        self.all_bullets = pygame.sprite.Group()
        self.time_counter = 0                       # Counter§\label{srcTime0101}§
        self.time_range = 30                        # Threshold§\label{srcTime0102}§
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
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

    def draw(self) -> None:
        self.screen.fill((200, 200, 200))
        self.all_bullets.draw(self.screen)
        self.enemy.draw(self.screen)
        self.window.flip()

    def update(self) -> None:
        self.new_bullet()
        self.all_bullets.update()
        self.enemy.update()

    def new_bullet(self) -> None:
        self.time_counter += 1                      # Increment per frame§\label{srcTime0103}§
        if self.time_counter >= self.time_range:    # If threshold reached§\label{srcTime0104}§
            self.all_bullets.add(Bullet("shoot.png", self.enemy.sprite.rect.move(0, 20).center))
            self.time_counter = 0                   # reset counter§\label{srcTime0105}§


def main():
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
