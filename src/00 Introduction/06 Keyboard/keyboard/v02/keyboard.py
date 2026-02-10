from time import time
from typing import Any

import config as cfg
import pygame


class Defender(pygame.sprite.Sprite):

    def __init__(self) -> None:
        super().__init__()
        self.image = pygame.image.load("images/defender01.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = pygame.FRect(self.image.get_rect())
        self.rect.center = cfg.WINDOW.center       
        self.speed = 100
        self.direction = cfg.DIRECTIONS["stop"]    

    def update(self, *args: Any, **kwargs: Any) -> None:
        if "action" in kwargs.keys():
            if kwargs["action"] == "move":
                    self.rect.move_ip(self.direction.elementwise() * self.speed * cfg.DELTATIME)
                    self.rect.clamp_ip(cfg.WINDOW)    
        elif "direction" in kwargs.keys():
            self.direction = cfg.DIRECTIONS[kwargs["direction"]]
        elif "speed" in kwargs.keys():
            if kwargs["speed"] == "faster":
                self.speed = 300
            elif kwargs["speed"] == "slower":
                self.speed = 10
            elif kwargs["speed"] == "normal":
                self.speed = 100



class Game(object):

    def __init__(self) -> None:
        pygame.init()
        self.window = pygame.Window(size=cfg.WINDOW.size, title="Keyboard", position=(10, 50))
        self.screen = self.window.get_surface()
        self.clock = pygame.time.Clock()
        self.defender = pygame.sprite.GroupSingle(Defender())
        self.running = False

    def run(self) -> None:
        time_previous = time()
        self.running = True
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

    def watch_for_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:    
                if event.mod == pygame.KMOD_NONE:                   # No modifier keys§\label{srcTastatur0101}§
                    self.defender.update(speed="normal")
                else:
                    if event.mod & pygame.KMOD_LSHIFT:              # Left shift pressed §\label{srcTastatur0102}§
                        self.defender.update(speed="faster")
                    if event.mod & pygame.KMOD_RSHIFT:              # Right shift pressed §\label{srcTastatur0103}§
                        self.defender.update(speed="slower")
                if event.key == pygame.K_ESCAPE:  
                    self.running = False
                elif event.key == pygame.K_RIGHT: 
                    self.defender.update(direction="right")
                elif event.key == pygame.K_LEFT:
                    self.defender.update(direction="left")
                elif event.key == pygame.K_UP:
                    self.defender.update(direction="up")
                elif event.key == pygame.K_DOWN:
                    self.defender.update(direction="down")
            elif event.type == pygame.KEYUP: 
                self.defender.update(speed="normal")         
                if event.key in (pygame.K_RIGHT, pygame.K_LEFT,
                                 pygame.K_UP, pygame.K_DOWN):
                    self.defender.update(direction="stop")

    def update(self) -> None:
        self.defender.update(action="move")

    def draw(self) -> None:
        self.screen.fill("white")
        self.defender.draw(self.screen)
        self.window.flip()


def main():
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
