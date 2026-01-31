from random import randint
from time import time

import config as cfg
import pygame


class Sky:
    def __init__(self, screen:pygame.surface.Surface) -> None:
        top = 0 
        left = 0
        width = cfg.WINDOW.width
        height = cfg.WINDOW.height - cfg.HORIZONT
        self.rect = pygame.rect.Rect(top, left, width, height)
        self.screen = screen

    def draw(self) -> None:
        pygame.draw.rect(self.screen, "black", self.rect)

class Moon:
    def __init__(self, screen: pygame.surface.Surface, layer_count: int=5):
        self.screen = screen
        top = cfg.WINDOW.height - cfg.HORIZONT
        self.rect = pygame.rect.Rect(0, top, 
                                      cfg.WINDOW.width, cfg.HORIZONT)   # Landing area§\label{moonlander02a01}§

        self.layers = []
        for layer_index in range(layer_count):  # Mountain range§\label{moonlander02a02}§
            mycolor = 180 - layer_index * 20    # Foreground darker, background lighter§\label{moonlander02a03}§
            self.layers.append({"y":self.rect.top - 10 - randint(5, 30)*layer_index, 
                                "color":(mycolor, mycolor, mycolor)})

    def draw(self):
        pygame.draw.rect(self.screen, (230, 230, 230), self.rect)

        for layer in reversed(self.layers):
            r = pygame.rect.Rect()
            r.top = layer["y"]
            r.left = self.rect.left
            r.width = self.rect.width
            r.height = self.rect.top - r.top
            pygame.draw.rect(self.screen, layer["color"], r)

class Earth:
    def __init__(self, screen:pygame.surface.Surface) -> None:
        self.radius = 80
        left = cfg.WINDOW.right - 2*self.radius - 30
        top = cfg.WINDOW.top + 15
        width = 2*self.radius
        height = 2*self.radius
        self.rect = pygame.rect.Rect(left, top, width, height)
        self.screen = screen


    def draw(self) -> None:
        pygame.draw.circle(self.screen, "blue", self.rect.center, self.radius)

class Game:
    def __init__(self) -> None:
        pygame.init()
        self.window = pygame.Window(size=cfg.WINDOW.size, title="MyMoonlander", position=pygame.WINDOWPOS_CENTERED)
        self.screen = self.window.get_surface()
        self.clock = pygame.time.Clock()


    def run(self) -> None:
        self.restart()
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

    def watch_for_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_r:
                    self.restart()

    def update(self) -> None:
        pass

    def draw(self) -> None:
        self.background.draw()
        self.moon.draw()
        self.earth.draw()
        self.window.flip()

    def restart(self) -> None:
        self.background = Sky(self.screen)
        self.moon = Moon(self.screen)
        self.earth = Earth(self.screen)
        self.running = True

def main():
    Game().run()

if __name__ == "__main__":
    main()




