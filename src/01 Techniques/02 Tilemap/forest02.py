from random import choice
from time import time

import config as cfg
import pygame


class Spritelib:
    def __init__(self, filename: str) -> None:
        self.image = pygame.image.load(filename).convert_alpha()

    def subsurface(self, tilenumber: int) -> pygame.Surface:
        left = (tilenumber % cfg.TILEMAP_NOF_COLS) * cfg.TILESIZE.x # §\label{srcforest0201}§
        top = (tilenumber // cfg.TILEMAP_NOF_COLS) * cfg.TILESIZE.y # §\label{srcforest0202}§
        tile_rect = pygame.Rect((left, top), cfg.TILESIZE)
        return self.image.subsurface(tile_rect)


class WindowGame:

    def __init__(self) -> None:
        self.window = pygame.Window(size=cfg.TILEMAP_WINDOW.size)
        self.screen : pygame.Surface = self.window.get_surface()
        self.rect = self.screen.get_frect()
        self.window.title = "Tilemap Example"
        self.clock = pygame.time.Clock()
        self.spritelib = Spritelib("images/forest_tiles.png")
        self.tiles = []
        for row in range(cfg.TILEMAP_NOF_ROWS):
            for col in range(cfg.TILEMAP_NOF_COLS):
                self.tiles.append(choice((0,1,2,3,4,16,17,18,19,20,32,33,34,35,36)))

    def draw(self) -> None:
        self.screen.fill("black")
        for row in range(cfg.TILEMAP_NOF_ROWS):
            for col in range(cfg.TILEMAP_NOF_COLS):
                index = self.tiles[row * cfg.TILEMAP_NOF_COLS + col]
                image = self.spritelib.subsurface(index)
                position = col * cfg.TILESIZE.x, row * cfg.TILESIZE.y
                self.screen.blit(image, position)
        self.window.flip()


class Game:

    def __init__(self) -> None:
        pygame.init()
        self.clock = pygame.time.Clock()
        self.window = WindowGame()
        self.running = True

    def run(self) -> None:
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

    def watch_for_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.WINDOWCLOSE:
                self.running = False
                event.window.destroy()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

    def update(self) -> None:
        pass

    def draw(self) -> None:
        self.window.draw()

        

   
def main() -> None:
    game = Game()
    game.run()


if __name__ == "__main__":
    main()

