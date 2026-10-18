from typing import Any

import pygame

import config as cfg


class Paddle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image: pygame.Surface = pygame.image.load(cfg.get_image("bar.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, cfg.BRICK["rect"].size)
        self.rect: pygame.FRect = self.image.get_frect()
        self.speed_max = 1000
        self.reset()

    def update(self, *args: Any, **kwargs: Any) -> None:
        if "action" in kwargs:
            if kwargs["action"] == "right":
                self.speed_now = self.speed_max
            elif kwargs["action"] == "left":
                self.speed_now = -self.speed_max
            elif kwargs["action"] == "stop":
                self.speed_now = 0
            elif kwargs["action"] == "move":
                self.rect.left += self.speed_now * cfg.DELTATIME
                self.rect.clamp_ip(cfg.WINDOW)
            elif kwargs["action"] == "reset":
                self.reset()
        return super().update(*args, **kwargs)

    def reset(self) -> None:
        self.rect.centerx = cfg.WINDOW.centerx
        self.rect.bottom = cfg.WINDOW.bottom - cfg.STATUSHEIGHT
        self.speed_now = 0
