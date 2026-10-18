## BEGIN Änderung: eigenständiges BrickFragment-Sprite nach dem TrailBall-Muster
import random
from typing import Any

import pygame

import config as cfg
from sprites.brick import Brick


class BrickFragment(pygame.sprite.Sprite):
    DURATION = 1.6
    FADE_DURATION = 0.4

    def __init__(self, brick: Brick, col: int, row: int):
        super().__init__()
        width = brick.image.get_width() // cfg.BRICK["fragx"]
        height = brick.image.get_height() // cfg.BRICK["fragy"]
        subrect = pygame.Rect(col * width, row * height, width, height)
        self.image: pygame.Surface = brick.image.subsurface(subrect).copy()
        self.original_image = self.image
        self.angle = random.uniform(-20, 20)
        spin_direction = random.choice((-1, 1))
        self.angular_velocity = spin_direction * random.uniform(100, 240)
        self.rect: pygame.FRect = self.image.get_frect()
        self.rect.topleft = (brick.rect.left + subrect.left, brick.rect.top + subrect.top)
        self.velocity = pygame.Vector2(random.uniform(-130, 130), random.uniform(-240, -70))
        self.remaining = self.DURATION

    def update(self, *args: Any, **kwargs: Any) -> None:
        self.remaining -= cfg.DELTATIME
        self.velocity.y += cfg.BRICK["gravity"] * cfg.DELTATIME
        self.rect.move_ip(self.velocity * cfg.DELTATIME)
        center = self.rect.center
        self.angle = (self.angle + self.angular_velocity * cfg.DELTATIME) % 360
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_frect()
        self.rect.center = center
        if self.remaining <= 0:
            self.kill()
        elif self.remaining < self.FADE_DURATION:
            self.image.set_alpha(round(255 * self.remaining / self.FADE_DURATION))
        return super().update(*args, **kwargs)
