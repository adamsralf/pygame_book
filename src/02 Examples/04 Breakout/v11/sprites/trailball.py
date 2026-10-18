from typing import Any

import pygame

import config as cfg
from sprites.ball import Ball


class TrailBall(pygame.sprite.Sprite):
    TRAIL_DURATION = 0.4  

    def __init__(self, ball: Ball):
        super().__init__()
        self.image : pygame.Surface = ball.image.copy()  
        self.rect : pygame.FRect = ball.rect.copy()
        self.remaining = self.TRAIL_DURATION  

    def update(self, *args: Any, **kwargs: Any) -> None:
        if self.remaining > 0:
            self.remaining -= cfg.DELTATIME
            self.image = pygame.transform.scale_by(self.image, 0.99)
            self.image.set_alpha(round(255 * self.remaining / self.TRAIL_DURATION))
        else:
            self.kill()
        return super().update(*args, **kwargs)

