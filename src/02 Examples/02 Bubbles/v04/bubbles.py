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


class BubbleContainer:
    def __init__(self) -> None:
        imagename = cfg.get_image("bubble1.png")
        image: pygame.surface.Surface = pygame.image.load(imagename).convert_alpha()
        self.images = {i: pygame.transform.scale(image, (i * 2, i * 2)) for i in range(cfg.RADIUS["min"], cfg.RADIUS["max"] + 1)}  # §\label{srcBubble0403}§

    def get(self, radius: int) -> pygame.surface.Surface:
        radius = max(cfg.RADIUS["min"], radius)  # Lower limit§\label{srcBubble0404}§
        radius = min(cfg.RADIUS["max"], radius)  # Upper limit§\label{srcBubble0405}§
        return self.images[radius]


class Bubble(pygame.sprite.Sprite):
    def __init__(self, bubble_container: BubbleContainer) -> None:
        super().__init__()
        self.bubble_container = bubble_container    # Reference to container§\label{srcBubble0406}§
        self.radius = cfg.RADIUS["min"]
        self.image = self.bubble_container.get(self.radius)  # Get bubble§\label{srcBubble0407}§
        self.rect: pygame.rect.Rect = self.image.get_rect()
        self.fradius = float(self.radius)
        self.speed = 100

    def update(self, *args: Any, **kwargs: Any) -> None:
        if "action" in kwargs.keys():
            if kwargs["action"] == "grow":
                self.fradius += self.speed * cfg.DELTATIME
                self.fradius = min(self.fradius, cfg.RADIUS["max"])  # New radius§\label{srcBubble0410}§
                self.radius = round(self.fradius)
                center = self.rect.center           # Save center pos§\label{srcBubble0411}§
                self.image = self.bubble_container.get(self.radius)  # New image §\label{srcBubble0412}§
                self.rect = self.image.get_rect()
                self.rect.center = center           # Restore center pos§\label{srcBubble0413}§

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

    def draw(self) -> None:
        self.background.draw(self.screen)
        self.all_sprites.draw(self.screen)
        self.window.flip()

    def update(self) -> None:
        self.all_sprites.update(action="grow")      # Bubbles growing §\label{srcBubble0414}§
        self.spawn_bubble()

    def spawn_bubble(self) -> None:
        if self.timer_bubble.is_next_stop_reached():
            if len(self.all_sprites) <= cfg.MAX_BUBBLES:
                b = Bubble(self.bubble_container)  # §\label{srcBubble0415}§
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
