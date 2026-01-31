from time import time
from typing import Any, Tuple

import config as cfg
import pygame


class Background(pygame.sprite.Sprite):
    def __init__(self, *groups: Tuple[pygame.sprite.Group]) -> None:
        super().__init__(*groups)
        self.image = pygame.surface.Surface(cfg.WINDOW.size).convert()
        self.rect = self.image.get_rect()
        self.image.fill("darkred")
        self.paint_net()

    def paint_net(self) -> None:
        net_rect = pygame.rect.Rect(0, 0, 0, 0)
        net_rect.centerx = cfg.WINDOW.centerx
        net_rect.top = 50
        net_rect.size = (3, 30)
        while net_rect.bottom < cfg.WINDOW.bottom:
            pygame.draw.rect(self.image, "grey", net_rect, 0)
            net_rect.move_ip(0, 40)


class Paddle(pygame.sprite.Sprite):
    BORDERDISTANCE = {"horizontal": 50, "vertical": 10}
    DIRECTION = {"up": -1, "down": 1, "halt": 0}

    def __init__(self, player: str, *groups: Tuple[pygame.sprite.Group]) -> None:
        super().__init__(*groups)
        self.rect = pygame.rect.FRect(0, 0, 15, cfg.WINDOW.height // 10)# Size§\label{srcPong0201}§
        self.rect.centery = cfg.WINDOW.centery                          # Position §\label{srcPong0202}§
        self.player = player
        if self.player == "left":
            self.rect.left = Paddle.BORDERDISTANCE["horizontal"]
        else:
            self.rect.right = cfg.WINDOW.right - Paddle.BORDERDISTANCE["horizontal"]
        self.speed = cfg.WINDOW.height // 2                             # Speed§\label{srcPong0206}§
        self.direction = Paddle.DIRECTION["halt"]   # 
        self.image = pygame.surface.Surface(self.rect.size)             # Surface§\label{srcPong0203}§
        self.image.fill("yellow")

    def update(self, *args: Any, **kwargs: Any) -> None:
        if "action" in kwargs.keys():
            if kwargs["action"] == "move":                              # Change Postion§\label{srcPong0204}§
                self.move()
            elif kwargs["action"] in Paddle.DIRECTION.keys():           # Direction§\label{srcPong0205}§
                self.direction = Paddle.DIRECTION[kwargs["action"]]
        return super().update(*args, **kwargs)

    def move(self) -> None:
        if self.direction != Paddle.DIRECTION["halt"]:
            self.rect.move_ip(0, self.speed * self.direction * cfg.DELTATIME)  # §\label{srcPong0207}§
            if self.direction == Paddle.DIRECTION["up"]:
                self.rect.top = max(self.rect.top, Paddle.BORDERDISTANCE["vertical"])
            elif self.direction == Paddle.DIRECTION["down"]:
                self.rect.bottom = min(self.rect.bottom, cfg.WINDOW.height - Paddle.BORDERDISTANCE["vertical"])


class Game:
    def __init__(self):
        pygame.init()
        self.window = pygame.Window(size=cfg.WINDOW.size, title="My Kind of Pong", position=pygame.WINDOWPOS_CENTERED)
        self.screen = self.window.get_surface()
        self.clock = pygame.time.Clock()
        self.background = pygame.sprite.GroupSingle(Background())
        self.all_sprites = pygame.sprite.Group()
        self.paddle = {}  # Schläger §\label{srcPong0208}§
        self.paddle["left"] = Paddle("left", self.all_sprites)
        self.paddle["right"] = Paddle("right", self.all_sprites)
        self.running = True

    def run(self):
        time_previous = time()
        while self.running:
            self.watch_for_events()
            self.update()
            self.draw()
            self.clock.tick(cfg.FPS)
            time_current = time()
            cfg.DELTATIME = time_current - time_previous
            time_previous = time_current
        pygame.quit()

    def update(self):
        self.all_sprites.update(action="move")      # Move§\label{srcPong0209}§

    def draw(self):
        self.background.draw(self.screen)
        self.all_sprites.draw(self.screen)          # §\label{srcPong0210}§
        self.window.flip()

    def watch_for_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_UP:      # Paddle moves§\label{srcPong0211}§
                    self.paddle["right"].update(action="up")
                elif event.key == pygame.K_DOWN:
                    self.paddle["right"].update(action="down")
                elif event.key == pygame.K_w:
                    self.paddle["left"].update(action="up")
                elif event.key == pygame.K_s:
                    self.paddle["left"].update(action="down")
            elif event.type == pygame.KEYUP:        # Paddle stops§\label{srcPong0212}§
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    self.paddle["right"].update(action="halt")
                elif event.key == pygame.K_w or event.key == pygame.K_s:
                    self.paddle["left"].update(action="halt")


def main():
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
