from random import randint
from time import time
from typing import Any

import config as cfg
import pygame


class Timer:
    def __init__(self, duration: int, with_start: bool = True) -> None:
        self.duration = duration
        if with_start:
            self._next = pygame.time.get_ticks()
        else:
            self._next = pygame.time.get_ticks() + self.duration

    def is_next_stop_reached(self) -> bool:
        if pygame.time.get_ticks() > self._next:
            self._next = pygame.time.get_ticks() + self.duration
            return True
        return False


class Background(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        imagename = cfg.get_image("aquarium.png")
        self.image: pygame.surface.Surface = pygame.image.load(imagename).convert()
        self.image = pygame.transform.scale(self.image, cfg.WINDOW.size)
        self.rect = self.image.get_rect()


class Bubble(pygame.sprite.DirtySprite):
    def __init__(self) -> None:
        super().__init__()
        self.radius = cfg.RADIUS["min"]
        imagename = cfg.get_image("bubble1.png")
        self.image: pygame.surface.Surface = pygame.image.load(imagename).convert_alpha()
        self.image = pygame.transform.scale(self.image, (cfg.RADIUS["min"], cfg.RADIUS["min"]))
        self.rect: pygame.rect.Rect = self.image.get_rect()

    def update(self, *args: Any, **kwargs: Any) -> None:
        pass

    def randompos(self) -> None:
        bubbledistance = cfg.DISTANCE + cfg.RADIUS["min"]
        centerx = randint(cfg.PLAYGROUND.left + bubbledistance, cfg.PLAYGROUND.right - bubbledistance)
        centery = randint(cfg.PLAYGROUND.top + bubbledistance, cfg.PLAYGROUND.bottom - bubbledistance)
        self.rect.center = (centerx, centery)


class Game:
    def __init__(self) -> None:
        pygame.init()
        self.window = pygame.Window(size=cfg.WINDOW.size, title=cfg.CAPTION)
        self.screen = self.window.get_surface()
        self.clock = pygame.time.Clock()
        self.background = pygame.sprite.GroupSingle(Background())
        self.timer_bubble = Timer(500, False)
        self.all_sprites = pygame.sprite.Group()
        self.running = True

    def watch_for_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

    def draw(self) -> None:
        self.background.draw(self.screen)
        self.all_sprites.draw(self.screen)
        self.window.flip()

    def update(self) -> None:
        self.spawn_bubble()

    def spawn_bubble(self) -> None:
        if self.timer_bubble.is_next_stop_reached():
            if len(self.all_sprites) <= cfg.MAX_BUBBLES:  # Enough space?§\label{srcBubble0306}§
                b = Bubble()
                for _ in range(100):
                    b.randompos()
                    b.radius += cfg.DISTANCE
                    collided = pygame.sprite.spritecollide(b, self.all_sprites, False, pygame.sprite.collide_circle)
                    b.radius -= cfg.DISTANCE
                    if not collided:
                        self.all_sprites.add(b)
                        break

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


def main():
    Game().run()


if __name__ == "__main__":
    main()
