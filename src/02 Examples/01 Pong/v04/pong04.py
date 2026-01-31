from random import choice
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
        self.rect = pygame.rect.FRect(0, 0, 15, cfg.WINDOW.height // 10)
        self.rect.centery = cfg.WINDOW.centery
        self.player = player
        if self.player == "left":
            self.rect.left = Paddle.BORDERDISTANCE["horizontal"]
        else:
            self.rect.right = cfg.WINDOW.right - Paddle.BORDERDISTANCE["horizontal"]
        self.speed = cfg.WINDOW.height // 2
        self.direction = Paddle.DIRECTION["halt"]  
        self.image = pygame.surface.Surface(self.rect.size)
        self.image.fill("yellow")

    def update(self, *args: Any, **kwargs: Any) -> None:
        if "action" in kwargs.keys():
            if kwargs["action"] == "move":
                self.move()
            elif kwargs["action"] in Paddle.DIRECTION.keys():
                self.direction = Paddle.DIRECTION[kwargs["action"]]
        return super().update(*args, **kwargs)

    def move(self) -> None:
        if self.direction != Paddle.DIRECTION["halt"]:
            self.rect.move_ip(0, self.speed * self.direction * cfg.DELTATIME)
            if self.direction == Paddle.DIRECTION["up"]:
                self.rect.top = max(self.rect.top, Paddle.BORDERDISTANCE["vertical"])
            elif self.direction == Paddle.DIRECTION["down"]:
                self.rect.bottom = min(self.rect.bottom, cfg.WINDOW.height - Paddle.BORDERDISTANCE["vertical"])


class Ball(pygame.sprite.Sprite):
    def __init__(self, *groups: Tuple[pygame.sprite.Group]) -> None:
        super().__init__(*groups)
        self.rect = pygame.rect.FRect(0, 0, 20, 20)
        self.image = pygame.surface.Surface(self.rect.size).convert()
        self.image.set_colorkey("black")
        pygame.draw.circle(self.image, "white", self.rect.center, self.rect.width // 2)
        self.speed = cfg.WINDOW.width // 3
        self.speedxy = pygame.Vector2()
        self.service()

    def update(self, *args: Any, **kwargs: Any) -> None:
        if "action" in kwargs.keys():
            if kwargs["action"] == "move":
                self.move()
            elif kwargs["action"] == "hflip":
                self.horizontal_flip()
            elif kwargs["action"] == "vflip":
                self.vertical_flip()
            elif kwargs["action"] == "reset":
                self.service()
        return super().update(*args, **kwargs)

    def move(self) -> None:
        self.rect.move_ip(self.speedxy * cfg.DELTATIME)
        if self.rect.top <= 0:
            self.vertical_flip()
            self.rect.top = 0
        elif self.rect.bottom >= cfg.WINDOW.bottom:
            self.vertical_flip()
            self.rect.bottom = cfg.WINDOW.bottom
        elif self.rect.right < 0:
            MyEvents.MYEVENT.player = 2             # Player§\label{srcPong0402}§
            pygame.event.post(MyEvents.MYEVENT)     # Shoot event§\label{srcPong0403}§
            self.service()
        elif self.rect.left > cfg.WINDOW.right:
            MyEvents.MYEVENT.player = 1
            pygame.event.post(MyEvents.MYEVENT)
            self.service()

    def service(self) -> None:
        self.rect.center = cfg.WINDOW.center
        self.speedxy = pygame.Vector2(choice([-1, 1]), choice([-1, 1])) * self.speed

    def horizontal_flip(self) -> None:
        self.speedxy.x *= -1

    def vertical_flip(self) -> None:
        self.speedxy.y *= -1


class Score(pygame.sprite.Sprite):

    def __init__(self, *groups: Tuple[pygame.sprite.Group]):
        super().__init__(*groups)
        self.font = pygame.font.SysFont(None, 30)
        self.score = {1: 0, 2: 0}                   # Not in Settings anymore!§\label{srcPong0405}§
        self.image: pygame.surface.Surface = None
        self.rect: pygame.rect.Rect = None
        self.render()

    def update(self, *args: Any, **kwargs: Any) -> None:
        if "player" in kwargs.keys():
            self.score[kwargs["player"]] += 1
            self.render()
        return super().update(*args, **kwargs)

    def render(self):
        self.image = self.font.render(f"{self.score[1]} : {self.score[2]}", True, "white")
        self.rect = self.image.get_rect(centerx=cfg.WINDOW.centerx, top=15)


class Game:
    def __init__(self):
        pygame.init()
        self.window = pygame.Window(size=cfg.WINDOW.size, title="My Kind of Pong", position=pygame.WINDOWPOS_CENTERED)
        self.screen = self.window.get_surface()
        self.clock = pygame.time.Clock()
        self.background = pygame.sprite.GroupSingle(Background())
        self.all_sprites = pygame.sprite.Group()
        self.paddle = {}
        self.paddle["left"] = Paddle("left", self.all_sprites)
        self.paddle["right"] = Paddle("right", self.all_sprites)
        self.ball = Ball(self.all_sprites)
        self.score = Score(self.all_sprites)
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
        self.all_sprites.update(action="move")

    def draw(self):
        self.background.draw(self.screen)
        self.all_sprites.draw(self.screen)
        self.window.flip()

    def watch_for_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_UP:
                    self.paddle["right"].update(action="up")
                elif event.key == pygame.K_DOWN:
                    self.paddle["right"].update(action="down")
                elif event.key == pygame.K_w:
                    self.paddle["left"].update(action="up")
                elif event.key == pygame.K_s:
                    self.paddle["left"].update(action="down")
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    self.paddle["right"].update(action="halt")
                elif event.key == pygame.K_w or event.key == pygame.K_s:
                    self.paddle["left"].update(action="halt")
            elif event.type == MyEvents.POINT_FOR:  # User event§\label{srcPong0404}§
                self.score.update(player=event.player)


def main():
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
