from time import time

import config as cfg
import pygame


class WindowGame:

    def __init__(self) -> None:
        self.window = pygame.Window(size=cfg.TILEMAP_WINDOW.size)
        self.screen : pygame.Surface = self.window.get_surface()
        self.spritelib = pygame.image.load("images/forest_tiles.png").convert_alpha()
        self.rect = self.screen.get_frect()
        self.window.title = "Tilemap Example"
        self.clock = pygame.time.Clock()

    def draw(self) -> None:
        self.screen.fill("black")
        image = self.spritelib.subsurface(pygame.Rect((0, 0), cfg.TILESIZE))
        for row in range(cfg.TILEMAP_NOF_ROWS):
            for col in range(cfg.TILEMAP_NOF_COLS):
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

