from typing import Any

import pygame

import config as cfg


class Status(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image: pygame.Surface = pygame.surface.Surface((cfg.WINDOW.width, cfg.STATUSHEIGHT))
        self.image_ball: pygame.Surface = pygame.image.load(cfg.get_image("ball.png")).convert_alpha()
        self.image_ball = pygame.transform.scale_by(self.image_ball, 0.125)
        self.rect = self.image.get_rect()
        self.rect.bottom = cfg.WINDOW.bottom
        self.points = 0
        self.level = 0
        self.balls = 0

    def update(self, *args: Any, **kwargs: Any) -> None:
        if self.points != cfg.POINTS or self.level != cfg.LEVEL or self.balls != cfg.BALLS:
            self.balls = cfg.BALLS
            self.level = cfg.LEVEL
            self.points = cfg.POINTS
            self.render()

    def render(self) -> None:
        self.image.fill("black")
        font = pygame.font.Font(None, 36)

        balls_text = font.render("Balls: ", True, "white")
        balls_rect = balls_text.get_rect()
        balls_rect.centery = self.image.get_rect().centery
        balls_rect.left = 10
        self.image.blit(balls_text, balls_rect)
        for i in range(self.balls):
            ball_rect = self.image_ball.get_rect()
            ball_rect.centery = self.image.get_rect().centery
            ball_rect.left = balls_rect.right + 10 + i * (ball_rect.width + 5)
            self.image.blit(self.image_ball, ball_rect)

        points_text = font.render(f"Points: {self.points}", True, "white")
        points_rect = points_text.get_rect()
        points_rect.centery = self.image.get_rect().centery
        points_rect.centerx = self.image.get_rect().centerx
        self.image.blit(points_text, points_rect)

        level_text = font.render(f"Level: {self.level}", True, "white")
        level_rect = level_text.get_rect()
        level_rect.centery = self.image.get_rect().centery
        level_rect.right = self.image.get_rect().right - 10
        self.image.blit(level_text, level_rect)
