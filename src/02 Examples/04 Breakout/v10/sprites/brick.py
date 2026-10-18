import random
from typing import Any

import pygame

import config as cfg


class Brick(pygame.sprite.Sprite):
    def __init__(self, position: tuple[int, int]):
        super().__init__()
        self.images = []
        image_count = 2 if random.random() < min(cfg.LEVEL, 10) / 10 else 1
        for i in range(image_count):
            filename = cfg.get_image(f"brick{position[1]:02d}0{i}.png")
            image = pygame.image.load(filename).convert_alpha()
            image = pygame.transform.scale(image, cfg.BRICK["rect"].size)
            self.images.append(image)
        self.imageindex = 0
        self.image: pygame.Surface = self.images[self.imageindex]
        self.rect: pygame.FRect = self.image.get_frect()
        self.rect.left = cfg.BRICK["dist"]["x"]
        self.rect.left += position[0] * (cfg.BRICK["rect"].width + cfg.BRICK["dist"]["x"])
        self.rect.top = 2 * cfg.BALLSIZE
        self.rect.top += position[1] * (cfg.BRICK["rect"].height + cfg.BRICK["dist"]["y"])
        self.points = (cfg.BRICK["rows"] - position[1]) * 10

    def update(self, *args: Any, **kwargs: Any) -> None:
        if "action" in kwargs and kwargs["action"] == "hit":
            self.hit()
        return super().update(*args, **kwargs)

    def hit(self) -> None:
        if self.imageindex < len(self.images) - 1:
            self.imageindex += 1
            self.image = self.images[self.imageindex]
        else:
            cfg.POINTS += self.points
            self.kill()
