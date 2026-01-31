import random
from time import time
from typing import Any

import pygame

import config as cfg
from windows import WindowBirdEyeView, WindowCenteredCamera


class TreeContainer:
    def __init__(self):
        self.trees = []
        img = pygame.image.load(cfg.get_image("tree1.png")).convert_alpha()
        for i in range(0, 4):
            for j in range(1, 4):
                tree = img.subsurface((i * 128, (j - 1) * 128, 128, 128))
                tree = pygame.transform.scale2x(tree)
                self.trees.append(tree)
    
    def get(self, index) -> pygame.Surface:
        return self.trees[index % len(self.trees)]
    
    def get_random(self) -> pygame.Surface:
        return random.choice(self.trees)

class Player(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        self.rect = pygame.rect.FRect(0, 0, 32, 32)
        self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255, 0, 0), (16, 16), 16)
        self.rect.centerx = cfg.WORLD.centerx
        self.rect.bottom = cfg.WORLD.bottom - 32
        self.speed = 300 # px/s
        self.direction = 0

    def update(self, *args: Any, **kwargs: Any) -> None:
        if "move" in kwargs.keys():
            match kwargs["move"]:
                case "left":
                    self.direction = -1
                case "right":
                    self.direction = 1
                case "stop":
                    self.direction = 0
                case _:
                    self.direction = 0
        self.rect.centerx += self.direction * self.speed * cfg.DELTATIME
        self.rect.clamp_ip(cfg.WORLD)
        print(self.rect)
        return super().update(*args, **kwargs)
    

class Game:
    def __init__(self):
        pygame.init()
        self.player = Player()
        self.trees = pygame.sprite.Group()
        self.playground = WindowCenteredCamera(self.player, self.trees, pygame.sprite.Group())
        self.playground.window.position = (5, 30)
        self.controll = WindowBirdEyeView(pygame.sprite.Group(), pygame.sprite.Group(self.player))
        self.controll.window.position = (5, self.playground.window.size[1] + 60)
        self.clock = pygame.time.Clock()
        self.running = True

    def run(self):
        time_previous = time()
        while self.running:
            self.watch_for_events()
            if self.running:
                self.update()
                self.draw()
                self.clock.tick(cfg.FPS)
                time_current = time()
                cfg.DELTATIME = time_current - time_previous
                time_previous = time_current
        pygame.quit()

    def update(self):
        self.player.update()

    def draw(self):
        self.playground.draw()
        self.controll.draw([])

    def watch_for_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.WINDOWCLOSE:
                self.running = False
                event.window.destroy()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_LEFT:
                    self.player.update(move="left")
                elif event.key == pygame.K_RIGHT:
                    self.player.update(move="right")
                elif event.key == pygame.K_s:
                    self.save()

            elif event.type == pygame.KEYUP:
                if event.key in (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT):
                    self.player.update(move="stop")


def main():
    Game().run()


if __name__ == "__main__":
    main()
