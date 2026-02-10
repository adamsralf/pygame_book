from random import choice, randint
from typing import Any

import config as cfg
import pygame


class Tile(pygame.sprite.Sprite):
    def __init__(self, position: tuple[float, float]) -> None:
        super().__init__()
        self.image = pygame.Surface(cfg.TILESIZE_WORLD)
        # Yellow -> White according to the distance to the center
        v1 = pygame.Vector2(position)
        v2 = pygame.Vector2(cfg.WORLD.center)
        distance = v2.distance_to(v1)
        max_distance = v2.length()
        rel_dist_center = min(1.0, distance / max_distance)
        blue_value = int(255 * (1 - rel_dist_center))       
        color = (255, 255, blue_value)
        self.image.fill(color)
        if cfg.TILE_WITH_BORDER > 0:
            pygame.draw.rect(self.image, "Black", 
                             ((0,0), cfg.TILESIZE_WORLD), 
                             cfg.TILE_WITH_BORDER)
        self.rect = self.image.get_rect(topleft=position)
        self.image_small = pygame.transform.scale_by(self.image, cfg.ZOOM_BIRDEYE,)#§\label{tilev0401}§
   

class Player(pygame.sprite.Sprite):

    def __init__(self, position: tuple[float, float]) -> None:
        super().__init__()
        self.image : pygame.Surface = pygame.Surface(cfg.TILESIZE_WORLD)
        self.image.set_colorkey((0, 0, 0))
        self.radius = int(cfg.TILESIZE_WORLD.x // 2)
        pygame.draw.circle(self.image, "red", (self.radius, self.radius), self.radius)
        self.rect : pygame.FRect = self.image.get_frect(center=position)
        self.image_small = pygame.transform.scale_by(self.image, cfg.ZOOM_BIRDEYE)#§\label{tilev0402}§
        rect = self.image_small.get_frect()
        pygame.draw.circle(self.image_small, "red", rect.center, self.radius * cfg.ZOOM_BIRDEYE.x)

        self.speed = 400.0  # pixels per second
        self.directions = {
            "left": pygame.Vector2(-1, 0),
            "right": pygame.Vector2(1, 0),
            "up": pygame.Vector2(0, -1),
            "down": pygame.Vector2(0, 1),
            "stop": pygame.Vector2(0, 0),
        }
        self.direction = self.directions["stop"]

    def update(self, *args: Any, **kwargs: Any) -> None:
        if "position" in kwargs:
            self.rect.center = kwargs["position"]
        if "move" in kwargs:
            self.direction = self.directions[kwargs["move"]]
        new_position = pygame.Vector2(self.rect.center) + self.direction * (
            self.speed * cfg.DELTATIME
        )
        self.rect.center = new_position
        self.rect.clamp_ip(cfg.WORLD)
        return super().update(*args, **kwargs)


class Mob(pygame.sprite.Sprite):

    def __init__(self) -> None:
        super().__init__()
        x1 = int(cfg.TILESIZE_WORLD.x + 10)
        x2 = int(cfg.WORLD.width - (cfg.TILESIZE_WORLD.x + 10))
        y1 = int(cfg.TILESIZE_WORLD.y + 10)
        y2 = int(cfg.WORLD.height - (cfg.TILESIZE_WORLD.y + 10))
        position = (randint(x1, x2), randint(y1, y2))
        self.image = pygame.Surface(cfg.TILESIZE_WORLD, pygame.SRCALPHA)
        color = (0, 0, randint(10, 255))
        pad = randint(0, int(cfg.TILESIZE_WORLD.x//2 - 1))
        pygame.draw.rect(self.image, 
                         color, 
                         ((pad,pad), (cfg.TILESIZE_WORLD.x - 2*pad, 
                                      cfg.TILESIZE_WORLD.y - 2*pad)))
        self.rect = self.image.get_frect()
        self.rect.topleft = position
        self.direction = pygame.Vector2(choice((-1, 1)), choice((-1,1)))
        self.speed = randint(100, 500) # px/sec
        self.image_small = pygame.Surface(cfg.TILESIZE_WORLD.elementwise()*cfg.ZOOM_BIRDEYE, pygame.SRCALPHA)
        self.image_small.fill("LightBlue")



    def update(self, *args: Any, **kwargs: Any) -> None:
        self.rect.move_ip(self.direction * self.speed * cfg.DELTATIME)
        if self.rect.right < cfg.WORLD.left:
            self.rect.left = cfg.WORLD.right
        elif self.rect.left > cfg.WORLD.right:
            self.rect.right = cfg.WORLD.left
        if self.rect.bottom < cfg.WORLD.top:
            self.rect.top = cfg.WORLD.bottom
        elif self.rect.top > cfg.WORLD.bottom:
            self.rect.bottom = cfg.WORLD.top
        return super().update(*args, **kwargs)


