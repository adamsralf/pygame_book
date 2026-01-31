from time import time

import config as cfg
import pygame
from pygame.constants import K_ESCAPE, KEYDOWN, QUIT


class Game:

    def __init__(self) -> None:
        pygame.init()
        self.window = pygame.Window(size=cfg.WINDOW.size, title="Event (0)", position=pygame.WINDOWPOS_CENTERED)
        self.screen = self.window.get_surface()
        self.clock = pygame.time.Clock()
        self.running = True

    def run(self) -> None:
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
            print(event)                            # Print event information§\label{srcEvents0001}§
            if event.type == QUIT:
                self.running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.running = False

    def update(self):
        pass

    def draw(self) -> None:
        self.screen.fill("white")
        self.window.flip()


def main():
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
