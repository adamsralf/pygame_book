from time import time

import pygame

import config as cfg
from scenes.letters import Letters
from scenes.playground import Playground
from scenes.status import StatusBar
from scenes.titlebar import TitleBar


class Game():
    def __init__(self) -> None:
        pygame.init()
        self.window = pygame.Window(size=cfg.WINDOW.size, title="Four Connect - © Ralf Adams 2026")
        self.screen = self.window.get_surface()
        self.clock = pygame.time.Clock()
        self.ui_sprites = pygame.sprite.Group()
        self.title_bar = TitleBar(self.ui_sprites)
        self.playground = Playground(self.ui_sprites)
        self.letter = Letters(self.ui_sprites)
        self.status_bar = StatusBar(self.ui_sprites)

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
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

    def update(self) -> None:
        pass

    def draw(self) -> None:
        self.screen.fill(cfg.COLOR["BG"])
        self.ui_sprites.draw(self.screen)
        self.window.flip()


def main() -> None:
    game = Game()
    game.run()


if __name__ == "__main__":
    main()