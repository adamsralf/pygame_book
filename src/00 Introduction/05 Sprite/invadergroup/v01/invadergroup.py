from random import randint
from time import time
from typing import Any

import pygame


class Ship(pygame.sprite.Sprite):
    def __init__(self, position:tuple[int,int], *groups: pygame.sprite.AbstractGroup[Any]) -> None:
        super().__init__(*groups)
        self.image = pygame.image.load("images/defender01.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = pygame.rect.FRect(self.image.get_rect())
        self.rect.left = position[0]
        self.rect.bottom = position[1]
        self.speed = -300

    def update(self, *args: Any, **kwargs: Any) -> None:
        self.rect.move_ip(0, self.speed * Game.DELTATIME)
        self.rect.clamp_ip(Game.WINDOW)
        return super().update(*args, **kwargs)



class Game():
    FPS = 60
    DELTATIME = 1.0 / FPS
    SPWAN = 15
    WINDOW = pygame.rect.Rect(0,0,300,600)

    def __init__(self) -> None:
        pygame.init()
        self.window = pygame.Window(size=Game.WINDOW.size, title="Spritegroup")
        self.screen = self.window.get_surface()
        self.clock = pygame.time.Clock()
        self.ships = pygame.sprite.Group()
        self.running = True
        self.counter = 0 


    def run(self) -> None:
        time_previous = time()
        while self.running:
            self.watch_for_events()
            self.update()
            self.draw()
            self.clock.tick(Game.FPS)
            time_current = time()
            Game.DELTATIME = time_current - time_previous
            time_previous = time_current

    def watch_for_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self) -> None:
        self.counter += 1
        if self.counter > Game.SPWAN:
            self.counter = 0
            Ship((randint(0, 300-30), 600), self.ships) # §\label{srcInvadergroup0101}§
        self.ships.update()

    def draw(self) -> None:
        self.screen.fill((255, 255, 255))
        self.ships.draw(self.screen)
        self.window.flip()

def main():
    game = Game()
    game.run()

if __name__ == "__main__":
    main()