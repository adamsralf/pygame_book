from random import randint
from time import time
from typing import Any, Tuple

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
        self.image: pygame.Surface = pygame.image.load(imagename).convert()
        self.image = pygame.transform.scale(self.image, cfg.WINDOW.size)
        self.rect = self.image.get_rect()


class BubbleContainer:
    def __init__(self) -> None:
        imagename = cfg.get_image("bubble1.png")
        image: pygame.Surface = pygame.image.load(imagename).convert_alpha()
        self._images = {i: pygame.transform.scale(image, (i * 2, i * 2)) for i in range(cfg.RADIUS["min"], cfg.RADIUS["max"] + 1)}

    def get(self, radius: int) -> pygame.Surface:
        radius = max(cfg.RADIUS["min"], radius)
        radius = min(cfg.RADIUS["max"], radius)
        return self._images[radius]


class Bubble(pygame.sprite.Sprite):
    def __init__(self, bubble_container: BubbleContainer) -> None:
        super().__init__()
        self.bubble_container = bubble_container
        self.radius = cfg.RADIUS["min"]
        self.image = self.bubble_container.get(self.radius)
        self.rect: pygame.Rect = self.image.get_rect()
        self.fradius = float(self.radius)
        self.speed = 100

    def update(self, *args: Any, **kwargs: Any) -> None:
        if "action" in kwargs.keys():
            if kwargs["action"] == "grow":
                self.fradius += self.speed * cfg.DELTATIME
                self.fradius = min(self.fradius, cfg.RADIUS["max"])
                self.radius = round(self.fradius)
                center = self.rect.center
                self.image = self.bubble_container.get(self.radius)
                self.rect = self.image.get_rect()
                self.rect.center = center

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
        self.bubble_container = BubbleContainer()
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
            elif event.type == pygame.MOUSEBUTTONDOWN:  # Mouse clicked?§\label{srcBubble0601}§
                if event.button == 1:  # left
                    self.sting(pygame.mouse.get_pos())  #§\label{srcBubble0602}§

    def draw(self) -> None:
        self.background.draw(self.screen)
        self.all_sprites.draw(self.screen)
        self.window.flip()

    def update(self) -> None:
        self.all_sprites.update(action="grow")
        self.spawn_bubble()
        self.set_mousecursor()

    def spawn_bubble(self) -> None:
        if self.timer_bubble.is_next_stop_reached():
            if len(self.all_sprites) <= cfg.MAX_BUBBLES:
                b = Bubble(self.bubble_container)
                for _ in range(100):
                    b.randompos()
                    b.radius += cfg.DISTANCE
                    collided = pygame.sprite.spritecollide(b, self.all_sprites, False, pygame.sprite.collide_circle)
                    b.radius -= cfg.DISTANCE
                    if not collided:
                        self.all_sprites.add(b)
                        break

    def collidepoint(self, point: Tuple[int, int], sprite: pygame.sprite.Sprite) -> bool:
        if hasattr(sprite, "radius"):
            deltax = point[0] - sprite.rect.centerx
            deltay = point[1] - sprite.rect.centery
            return deltax * deltax + deltay * deltay <= sprite.radius * sprite.radius
        return False

    def set_mousecursor(self) -> None:
        is_over = False
        pos = pygame.mouse.get_pos()
        for b in self.all_sprites:
            if self.collidepoint(pos, b):
                is_over = True
                break
        if is_over:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_CROSSHAIR)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)

    def sting(self, mousepos: Tuple[int, int]) -> None:
        for bubble in self.all_sprites:
            if self.collidepoint(mousepos, bubble): # Inside? §\label{srcBubble0603}§
                bubble.kill()

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
