from time import time

import config as cfg
import pygame
from objects import Mob, Player, Tile
from windows import WindowPlain


class Game:

    def __init__(self) -> None:
        pygame.init()
        self.clock = pygame.time.Clock()
        self.create_tiles()
        self.create_mobs()
        self.window_plain = WindowPlain(self.tiles, self.mobs)
        self.world_image = pygame.surface.Surface(cfg.WORLD.size)
        self.player = Player(cfg.WORLD.center)
        self.mobs.add(self.player)
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
                elif event.key == pygame.K_UP:
                    self.player.update(move="up")
                elif event.key == pygame.K_DOWN:
                    self.player.update(move="down")
                elif event.key == pygame.K_LEFT:
                    self.player.update(move="left")
                elif event.key == pygame.K_RIGHT:
                    self.player.update(move="right")
                elif event.key == pygame.K_s:
                    self.save()

            elif event.type == pygame.KEYUP:
                if event.key in (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT):
                    self.player.update(move="stop")

    def update(self) -> None:
        self.player.update()
        self.mobs.update()

    def draw(self) -> None:
        self.window_plain.draw()
        self.tiles.draw(self.world_image)
        self.mobs.draw(self.world_image)
        self.window_plain.window.title = f"Plain Window (size={self.window_plain.rect.size}, fps={self.clock.get_fps():.0f})"

    def create_tiles(self) -> None:
        self.tiles = pygame.sprite.Group()
        for row in range(cfg.NOF_ROWS):
            for col in range(cfg.NOF_COLS):
                x = col * cfg.TILESIZE_WORLD.x
                y = row * cfg.TILESIZE_WORLD.y
                self.tiles.add(Tile((x, y)))

    def create_mobs(self) -> None:
        self.mobs = pygame.sprite.Group()
        for _ in range(cfg.NOF_MOBS):
            self.mobs.add(Mob())

    def save(self):
        pygame.image.save(self.world_image, "world_image.png")
        self.window_plain.save()

   
def main() -> None:
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
