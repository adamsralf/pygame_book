import math
from typing import Any

import pygame

import config as cfg
from sprites.brick import Brick
from sprites.paddle import Paddle


class Ball(pygame.sprite.Sprite):
    def __init__(self, paddle: Paddle):
        super().__init__()
        self.paddle = paddle
        self.image: pygame.Surface = pygame.image.load(cfg.get_image("ball.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, (cfg.BALLSIZE, cfg.BALLSIZE))
        self.rect: pygame.FRect = self.image.get_frect()
        self.speed = 500
        self.reset()

    def update(self, *args: Any, **kwargs: Any) -> None:
        if "action" in kwargs:
            if kwargs["action"] == "launch":
                if self.speedxy.length() == 0:
                    self.launch()
            elif kwargs["action"] == "move":
                if self.speedxy.length() > 0:
                    self.rect.move_ip(self.speedxy * cfg.DELTATIME)
                    if self.rect.left <= cfg.WINDOW.left or self.rect.right >= cfg.WINDOW.right:
                        self.speedxy.x *= -1
                    if self.rect.top <= cfg.WINDOW.top or self.rect.bottom >= cfg.WINDOW.bottom:
                        self.speedxy.y *= -1
                    self.rect.clamp_ip(cfg.WINDOW)
                    self.bounce_bar()
                else:
                    self.reset()
            elif kwargs["action"] == "reset":
                self.reset()
            elif kwargs["action"] == "bounce" and "brick" in kwargs:
                self.bounce(kwargs["brick"])
        return super().update(*args, **kwargs)

    def launch(self) -> None:
        self.reset()
        self.speedxy = pygame.Vector2(self.speed, -self.speed)

    def reset(self) -> None:
        self.rect.centerx = self.paddle.rect.centerx
        self.rect.bottom = self.paddle.rect.top + 2
        self.speedxy = pygame.Vector2(0, 0)

    def bounce_bar(self) -> None:
        if self.speedxy.y <= 0:
            return
        if not self.rect.colliderect(self.paddle.rect):
            return

        self.rect.bottom = self.paddle.rect.top
        offset = (self.rect.centerx - self.paddle.rect.centerx) / (self.paddle.rect.width / 2)
        offset = pygame.math.clamp(offset, -1.0, 1.0)

        speed = self.speed * (1 + abs(offset) * 0.75)
        angle = math.radians(offset * 60)
        self.speedxy.x = speed * math.sin(angle)
        self.speedxy.y = -speed * math.cos(angle)

    def bounce(self, brick: Brick) -> None:
        overlap_x = min(self.rect.right, brick.rect.right) - max(self.rect.left, brick.rect.left)
        overlap_y = min(self.rect.bottom, brick.rect.bottom) - max(self.rect.top, brick.rect.top)
        if overlap_x < overlap_y:
            if self.rect.centerx < brick.rect.centerx:
                self.rect.right = brick.rect.left
            else:
                self.rect.left = brick.rect.right
            self.speedxy.x *= -1
        else:
            if self.rect.centery < brick.rect.centery:
                self.rect.bottom = brick.rect.top
            else:
                self.rect.top = brick.rect.bottom
            self.speedxy.y *= -1

    def is_lost(self) -> bool:
        return self.rect.top >= self.paddle.rect.bottom
