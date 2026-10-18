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
        self.image : pygame.Surface = pygame.image.load(cfg.get_image("Paddle.png")).convert_alpha()
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


class Game:
    def __init__(self):
        pygame.init()
        self.window = pygame.Window(size=cfg.WINDOW.size)
        self.window.title = cfg.CAPTION
        self.screen : pygame.Surface = self.window.get_surface()
        self.clock = pygame.time.Clock()
        self.running = True
        self.bricks = pygame.sprite.Group()
        for row in range(cfg.BRICK["rows"]):        
            for col in range(cfg.BRICK["cols"]):
                self.bricks.add(Brick((col, row))) 
        self.paddle = pygame.sprite.GroupSingle(Paddle())     # setup Paddle§\label{breakout0201}§      

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
                          self.paddle.update(action="right")   # set direction right§\label{breakout0202}§
                    elif event.key == pygame.K_LEFT:
                        self.paddle.update(action="left")      # set direction left
                elif event.type == pygame.KEYUP:
                    if event.key in (pygame.K_RIGHT, pygame.K_LEFT):
                        self.paddle.update(action="stop")      # stop moving§\label{breakout0203}§

    def update(self) -> None:
        self.paddle.update(action="move")                      # move Paddle§\label{breakout0204}§
        self.bricks.update()

    def draw(self) -> None:
            self.screen.fill("black")
            self.bricks.draw(self.screen)
            self.paddle.draw(self.screen)                      # draw Paddle§\label{breakout0205}§
            self.window.flip()



def main():
    game = Game()
    game.run()

if __name__ == "__main__":
    main()