from time import time

import pygame

import config as cfg
from mobs.coin import Coin
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
        self.coins = pygame.sprite.Group()
        self.coin = Coin(player=1, groups=self.coins)

        self.playernumber = 1

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
                elif event.key in (pygame.K_a, pygame.K_b, pygame.K_c, pygame.K_d, pygame.K_e, pygame.K_f, pygame.K_g):
                    self.coin.colrow = self.playground.insert(event.key - pygame.K_a, self.playernumber)
                    if self.coin.colrow != (-1, -1):
                        self.playernumber = 2 if self.playernumber == 1 else 1
                        self.coin = Coin(player=self.playernumber, groups=self.coins)
                    print(self.coin.colrow)
                    

    def update(self) -> None:
        pass

    def draw(self) -> None:
        self.screen.fill(cfg.COLOR["BG"])
        self.draw_coins()
        self.ui_sprites.draw(self.screen)
        self.window.flip()

    def draw_coins(self) -> None:
        for coinn in self.coins.sprites():
            coinn.draw(self.screen)

def main() -> None:
    game = Game()
    game.run()


if __name__ == "__main__":
    main()