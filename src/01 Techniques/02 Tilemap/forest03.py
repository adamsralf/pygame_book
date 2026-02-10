from time import time

import config as cfg
import pygame


class Spritelib:
    def __init__(self, filename: str) -> None:
        self.image = pygame.image.load(filename).convert_alpha()

    def subsurface(self, tilenumber: int) -> pygame.Surface:
        left = (tilenumber % cfg.TILEMAP_NOF_COLS) * cfg.TILESIZE.x # 
        top = (tilenumber // cfg.TILEMAP_NOF_COLS) * cfg.TILESIZE.y # 
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
        self.tiles.append([99,98,113,17,18,17,18,18,17,18,51,17,17,13,34,34])
        self.tiles.append([115,114,97,60,18,20,34,29,34,34,34,13,34,36,116,117])
        self.tiles.append([99,115,113,17,18,20,116,117,117,117,64,117,120,117,164,133])
        self.tiles.append([115,113,18,18,18,20,132,133,133,136,10,136,133,136,155,155])
        self.tiles.append([99,97,18,17,104,105,132,136,185,152,71,152,152,149,180,133])
        self.tiles.append([115,113,18,13,17,20,132,136,137,55,56,0,0,53,132,155])
        self.tiles.append([99,97,19,18,18,20,132,136,137,0,0,0,0,0,132,133])
        self.tiles.append([115,113,18,51,18,20,75,10,69,0,50,0,53,0,135,133])
        self.tiles.append([99,97,18,17,17,20,132,136,137,0,0,82,0,0,135,133])
        self.tiles.append([115,113,128,129,18,20,132,136,134,0,0,0,0,0,135,155])
        self.tiles.append([99,97,144,145,13,20,132,136,137,87,103,0,13,0,73,11])
        self.tiles.append([115,113,19,18,19,36,132,133,169,139,139,139,139,139,164,136])

    def draw(self) -> None:
        self.screen.fill("black")
        for row in range(cfg.TILEMAP_NOF_ROWS):
            for col in range(cfg.TILEMAP_NOF_COLS):
                index = self.tiles[row][col]        # §\label{srcforest0301}§
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

