from time import time
from typing import Tuple

import config as cfg
import pygame


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
        while net_rect.bottom < cfg.WINDOW.bottom:  # Net as a seq of rectangles§\label{srcPong0101}§
            pygame.draw.rect(self.image, "grey", net_rect, 0)
            net_rect.move_ip(0, 40)


class Game:
    def __init__(self):
        pygame.init()
        self.window = pygame.Window(size=cfg.WINDOW.size, title="My Kind of Pong", position=pygame.WINDOWPOS_CENTERED)
        self.screen = self.window.get_surface()
        self.clock = pygame.time.Clock()
        self.background = pygame.sprite.GroupSingle(Background())
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
        pass

    def draw(self):
        self.background.draw(self.screen)
        self.window.flip()

    def watch_for_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False


def main():
    Game().run()


if __name__ == "__main__":
    main()
