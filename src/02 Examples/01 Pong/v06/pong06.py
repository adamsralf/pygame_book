from random import choice, randint
from time import time
from typing import Any, Tuple

import config as cfg
import pygame
from config import MyEvents


class Background(pygame.sprite.Sprite):
    def __init__(self, *groups: Tuple[pygame.sprite.Group]) -> None:
        super().__init__(*groups)
        self.image = pygame.Surface(cfg.WINDOW.size).convert()
        self.rect = self.image.get_rect()
        self.image.fill("darkred")
        self.paint_net()

    def paint_net(self) -> None:
        net_rect = pygame.Rect(0, 0, 0, 0)
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
        self.rect = pygame.FRect(0, 0, 15, cfg.WINDOW.height // 10)
        self.rect.centery = cfg.WINDOW.centery
        self.images = {
            "byhand": pygame.Surface(self.rect.size).convert(),
            "byki": pygame.Surface(self.rect.size).convert(),
        }
        self.images["byhand"].fill("yellow")
        self.images["byki"].fill("deepskyblue2")
        self.player = player
        if self.player == "left":
            self.rect.left = Paddle.BORDERDISTANCE["horizontal"]
        else:
            self.rect.right = cfg.WINDOW.right - Paddle.BORDERDISTANCE["horizontal"]
        self.speed = cfg.WINDOW.height // 2
        self.direction = Paddle.DIRECTION["halt"]  
        self.select_image()

    def update(self, *args: Any, **kwargs: Any) -> None:
        if "action" in kwargs.keys():
            if kwargs["action"] == "move":
                self.move()
            elif kwargs["action"] in Paddle.DIRECTION.keys():
                self.direction = Paddle.DIRECTION[kwargs["action"]]
        self.select_image()
        return super().update(*args, **kwargs)

    def move(self) -> None:
        if self.direction != Paddle.DIRECTION["halt"]:
            self.rect.move_ip(0, self.speed * self.direction * cfg.DELTATIME)
            if self.direction == Paddle.DIRECTION["up"]:
                self.rect.top = max(self.rect.top, Paddle.BORDERDISTANCE["vertical"])
            elif self.direction == Paddle.DIRECTION["down"]:
                self.rect.bottom = min(self.rect.bottom, cfg.WINDOW.height - Paddle.BORDERDISTANCE["vertical"])

    def select_image(self) -> None:
        if self.player == "left":
            if cfg.KI["left"]:
                self.image = self.images["byki"]
            else:
                self.image = self.images["byhand"]
        else:
            if cfg.KI["right"]:
                self.image = self.images["byki"]
            else:
                self.image = self.images["byhand"]


class Ball(pygame.sprite.Sprite):
    def __init__(self, *groups: Tuple[pygame.sprite.Group]) -> None:
        super().__init__(*groups)
        self.rect = pygame.FRect(0, 0, 20, 20)
        self.image = pygame.Surface(self.rect.size).convert()
        self.image.set_colorkey("black")
        pygame.draw.circle(self.image, "green", self.rect.center, self.rect.width // 2)
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
            MyEvents.MYEVENT.player = 2
            pygame.event.post(MyEvents.MYEVENT)
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
        self.respeed()

    def vertical_flip(self) -> None:
        self.speedxy.y *= -1

    def respeed(self) -> None:
        self.speedxy.x += randint(0, self.speed // 4)
        self.speedxy.y += randint(0, self.speed // 4)


class Score(pygame.sprite.Sprite):

    def __init__(self, *groups: Tuple[pygame.sprite.Group]):
        super().__init__(*groups)
        self.font = pygame.font.SysFont(None, 30)
        self.score = {1: 0, 2: 0}
        self.image: pygame.Surface = None
        self.rect: pygame.Rect = None
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
        self.check_collision()
        for i in cfg.KI.keys():                # Computer commands§\label{srcPong0603}§
            if cfg.KI[i]:
                self.paddlecontroler(self.paddle[i])
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
                    if not cfg.KI["right"]:    # §\label{srcPong0604}§
                        self.paddle["right"].update(action="up")
                elif event.key == pygame.K_DOWN:
                    if not cfg.KI["right"]:
                        self.paddle["right"].update(action="down")
                elif event.key == pygame.K_w:
                    if not cfg.KI["left"]:
                        self.paddle["left"].update(action="up")
                elif event.key == pygame.K_s:
                    if not cfg.KI["left"]:
                        self.paddle["left"].update(action="down")
                elif event.key == pygame.K_1:
                    cfg.KI["left"] = not cfg.KI["left"]
                    if not cfg.KI["left"]:     # Stop!§\label{srcPong0605}§
                        self.paddle["left"].update(action="halt")
                elif event.key == pygame.K_2:
                    cfg.KI["right"] = not cfg.KI["right"]
                    if not cfg.KI["right"]:
                        self.paddle["right"].update(action="halt")
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    if not cfg.KI["right"]:
                        self.paddle["right"].update(action="halt")
                elif event.key == pygame.K_w or event.key == pygame.K_s:
                    if not cfg.KI["left"]:
                        self.paddle["left"].update(action="halt")
            elif event.type == MyEvents.POINT_FOR:
                self.score.update(player=event.player)

    def check_collision(self):
        if pygame.sprite.collide_rect(self.ball, self.paddle["left"]):
            self.ball.update(action="hflip")
            self.ball.rect.left = self.paddle["left"].rect.right + 1
        elif pygame.sprite.collide_rect(self.ball, self.paddle["right"]):
            self.ball.update(action="hflip")
            self.ball.rect.right = self.paddle["right"].rect.left - 1

    def paddlecontroler(self, paddle: pygame.sprite.Sprite) -> None:
        if paddle.rect.centery > self.ball.rect.centery and paddle.rect.top > 10:
            paddle.update(action="up")
        elif paddle.rect.centery < self.ball.rect.centery and paddle.rect.bottom < cfg.WINDOW.bottom - 10:
            paddle.update(action="down")
        else:
            paddle.update(action="halt")


def main():
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
