from time import time
from typing import Any

import pygame

import config as cfg


class Brick(pygame.sprite.Sprite):
    def __init__(self, position: tuple[int, int]):
        super().__init__()
        filename = cfg.get_image(f"brick{position[1]:02d}00.png")
        self.image : pygame.Surface = pygame.image.load(filename).convert_alpha()
        self.image = pygame.transform.scale(self.image, cfg.BRICK["rect"].size)
        self.rect : pygame.FRect = self.image.get_frect()
        self.rect.left = cfg.BRICK["dist"]["x"] 
        self.rect.left += position[0] * (cfg.BRICK["rect"].width + cfg.BRICK["dist"]["x"])
        self.rect.top = 2 * cfg.BALLSIZE 
        self.rect.top += position[1] * (cfg.BRICK["rect"].height + cfg.BRICK["dist"]["y"])


class Paddle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image : pygame.Surface = pygame.image.load(cfg.get_image("bar.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, cfg.BRICK["rect"].size)
        self.rect : pygame.FRect = self.image.get_frect()
        self.rect.bottom = cfg.WINDOW.bottom - cfg.STATUSHEIGHT
        self.rect.centerx = cfg.WINDOW.centerx
        self.speed_max = 500                # px/s
        self.speed_now = 0                  # px/s

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
        return super().update(*args, **kwargs)

    
class Ball(pygame.sprite.Sprite):
    def __init__(self, paddle: Paddle):
        super().__init__()
        self.paddle = paddle
        self.image : pygame.Surface = pygame.image.load(cfg.get_image("ball.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, (cfg.BALLSIZE, cfg.BALLSIZE))
        self.rect : pygame.FRect = self.image.get_frect()
        self.speed = 500                # px/s
        self.speedxy : pygame.Vector2 = pygame.Vector2(0, 0)
        self.reset()

    def update(self, *args: Any, **kwargs: Any) -> None:
        if "action" in kwargs:
            if kwargs["action"] == "launch":
                if self.speedxy.length() == 0:            # ball is not moving§\label{breakout0303}§
                    self.launch()
            elif kwargs["action"] == "move":
                if self.speedxy.length() > 0:             # ball is moving§\label{breakout0304}§
                    self.rect.move_ip(self.speedxy * cfg.DELTATIME)
                    if self.rect.left <= cfg.WINDOW.left or self.rect.right >= cfg.WINDOW.right:
                        self.speedxy.x *= -1
                    if self.rect.top <= cfg.WINDOW.top or self.rect.bottom >= cfg.WINDOW.bottom:
                        self.speedxy.y *= -1
                    self.rect.clamp_ip(cfg.WINDOW)
                else:                                   # ball is not moving§\label{breakout0305}§
                    self.reset()
            elif kwargs["action"] == "reset":
                self.reset()
        return super().update(*args, **kwargs)

    def launch(self) -> None:
        self.reset()
        self.speedxy : pygame.Vector2 = pygame.Vector2(self.speed, -self.speed)  # px/s

    def reset(self) -> None:
        self.rect : pygame.FRect = self.image.get_frect()
        self.rect.centerx = self.paddle.rect.centerx
        self.rect.bottom = self.paddle.rect.top + 2
        self.speedxy : pygame.Vector2 = pygame.Vector2(0, 0)  # px/s


class Game:
    def __init__(self):
        pygame.init()
        self.window = pygame.Window(size=cfg.WINDOW.size)
        self.window.title = cfg.CAPTION
        self.screen = self.window.get_surface()
        self.clock = pygame.time.Clock()
        self.running = True
        self.bricks = pygame.sprite.Group()
        for row in range(cfg.BRICK["rows"]):        
            for col in range(cfg.BRICK["cols"]):
                self.bricks.add(Brick((col, row))) 
        self.paddle  = pygame.sprite.GroupSingle(Paddle())
        self.ball = pygame.sprite.GroupSingle(Ball(self.paddle.sprite))    # setup ball§\label{breakout0301}§      

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

    def watch_for_events(self)-> None:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                         self.running = False
                    elif event.key == pygame.K_RIGHT:
                          self.paddle.update(action="right")   
                    elif event.key == pygame.K_LEFT:
                        self.paddle.update(action="left")  
                    elif event.key == pygame.K_SPACE:
                        self.ball.update(action="launch")    
                elif event.type == pygame.KEYUP:
                    if event.key in (pygame.K_RIGHT, pygame.K_LEFT):
                        self.paddle.update(action="stop")      

    def update(self) -> None:
        self.paddle.update(action="move")                      
        self.ball.update(action="move")                     # move ball§\label{breakout0302}§
        self.bricks.update()

    def draw(self) -> None:
            self.screen.fill("black")
            self.bricks.draw(self.screen)
            self.paddle.draw(self.screen)                      
            self.ball.draw(self.screen)                     # draw ball§\label{breakout0306}§
            self.window.flip()



def main():
    game = Game()
    game.run()

if __name__ == "__main__":
    main()