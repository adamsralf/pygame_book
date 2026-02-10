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


class Map:
    def __init__(self) -> None:
        self.layer_data = []
        self.layer_data.append([])
        self.layer_data[0].append([18,17,18,17,18,17,18,18,17,18,18,17,17,19,34,34])
        self.layer_data[0].append([17,18,17,17,18,20,34,34,34,34,34,34,34,36,0,0])
        self.layer_data[0].append([18,1,18,17,18,20,0,0,0,0,64,0,0,0,0,0])
        self.layer_data[0].append([17,17,18,18,18,20,0,0,0,0,10,0,0,0,0,0])
        self.layer_data[0].append([17,18,18,17,18,20,0,0,0,0,71,0,0,0,0,0])
        self.layer_data[0].append([18,17,18,17,17,20,0,0,0,0,0,0,0,0,0,0])
        self.layer_data[0].append([18,1,19,18,18,20,0,0,0,0,0,0,0,0,0,0])
        self.layer_data[0].append([18,18,18,18,18,20,75,10,69,0,0,0,0,0,0,0])
        self.layer_data[0].append([18,18,18,17,17,20,0,0,0,0,0,0,0,0,0,0])
        self.layer_data[0].append([18,18,17,1,18,20,0,0,0,0,0,0,0,0,0,0])
        self.layer_data[0].append([18,18,18,18,17,20,0,0,0,0,0,0,0,0,73,11])
        self.layer_data[0].append([18,18,19,18,19,36,0,0,0,0,0,0,0,0,0,0])
        self.layer_data.append([])
        self.layer_data[1].append([99,98,113,-1,-1,-1,-1,-1,-1,-1,51,-1,-1,-1,-1,-1,-1])
        self.layer_data[1].append([115,114,97,-1,-1,-1,-1,29,-1,-1,-1,-1,-1,-1,116,117])
        self.layer_data[1].append([99,115,113,-1,-1,-1,116,117,117,117,-1,117,120,117,164,133])
        self.layer_data[1].append([115,113,-1,-1,-1,-1,132,133,133,136,-1,136,133,136,155,155])
        self.layer_data[1].append([99,97,-1,-1,104,105,132,136,185,152,-1,152,152,149,180,133])
        self.layer_data[1].append([115,113,-1,-1,-1,-1,132,136,137,55,56,-1,-1,53,132,155])
        self.layer_data[1].append([99,97,-1,-1,-1,-1,132,136,137,-1,-1,-1,-1,-1,132,133])
        self.layer_data[1].append([115,113,-1,51,-1,-1,-1,-1,-1,-1,50,-1,53,-1,135,133])
        self.layer_data[1].append([99,97,-1,-1,-1,-1,132,136,137,-1,-1,82,-1,-1,135,133])
        self.layer_data[1].append([115,113,128,129,-1,-1,132,136,134,-1,-1,-1,-1,-1,135,155])
        self.layer_data[1].append([99,97,144,145,-1,-1,132,136,137,87,103,-1,-1,-1,-1,-1])
        self.layer_data[1].append([115,113,-1,-1,-1,-1,132,133,169,139,139,139,139,139,164,136])
        self.layer_data.append([])
        self.layer_data[2].append([-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,13,-1,-1])
        self.layer_data[2].append([-1,-1,-1,60,-1,-1,-1,-1,-1,-1,-1,13,-1,-1,-1,-1])
        self.layer_data[2].append([-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1])
        self.layer_data[2].append([-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1])
        self.layer_data[2].append([-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1])
        self.layer_data[2].append([-1,-1,-1,13,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1])
        self.layer_data[2].append([-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1])
        self.layer_data[2].append([-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1])
        self.layer_data[2].append([-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1])
        self.layer_data[2].append([-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1])
        self.layer_data[2].append([-1,-1,-1,-1,13,-1,-1,-1,-1,-1,-1,-1,13,-1,-1,-1])
        self.layer_data[2].append([-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1])

    def get_layer_data(self, layer_index: int) -> list[list[int]]:
        return self.layer_data[layer_index]

class WindowGame:

    def __init__(self) -> None:
        self.window = pygame.Window(size=cfg.TILEMAP_WINDOW.size)
        self.screen : pygame.Surface = self.window.get_surface()
        self.rect = self.screen.get_frect()
        self.window.title = "Tilemap Example"
        self.clock = pygame.time.Clock()
        self.spritelib = Spritelib("images/forest_tiles.png")
        self.map = Map()

    def draw(self) -> None:
        self.screen.fill("black")
        for layer_index in range(3):
            tiles = self.map.get_layer_data(layer_index)
            for row in range(cfg.TILEMAP_NOF_ROWS):
                for col in range(cfg.TILEMAP_NOF_COLS):
                    index = tiles[row][col]                
                    if index > -1:                  # §\label{srcforest0401}§
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

