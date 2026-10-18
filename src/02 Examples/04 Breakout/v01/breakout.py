from time import time

import config as cfg
import pygame


class Brick(pygame.sprite.Sprite):
    def __init__(self, position: tuple[int, int]):
        super().__init__()
        filename = cfg.get_image(f"brick{position[1]:02d}00.png")
        self.image : pygame.Surface = pygame.image.load(filename).convert_alpha()
        self.image = pygame.transform.scale(self.image, cfg.BRICK["rect"].size)
        self.rect : pygame.FRect = self.image.get_frect()
        self.rect.left = cfg.BRICK["dist"]["x"] 
        self.rect.left += position[0] * (cfg.BRICK["rect"].width + cfg.BRICK["dist"]["x"])
        self.rect.top = 2 * cfg.BALLSIZE 
        self.rect.top += position[1] * (cfg.BRICK["rect"].height + cfg.BRICK["dist"]["y"])


class Game:
    def __init__(self):
        pygame.init()
        self.window = pygame.Window(size=cfg.WINDOW.size)
        self.window.title = cfg.CAPTION
        self.screen : pygame.Surface = self.window.get_surface()
        self.clock = pygame.time.Clock()
        self.running = True
        self.bricks = pygame.sprite.Group()
        for row in range(cfg.BRICK["rows"]):        # setup bricks§\label{breakout0101}§
            for col in range(cfg.BRICK["cols"]):
                self.bricks.add(Brick((col, row)))        

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

    def watch_for_events(self)-> None:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                         self.running = False

    def update(self) -> None:
        pass

    def draw(self) -> None:
            self.screen.fill("black")
            self.bricks.draw(self.screen)
            self.window.flip()



def main():
    game = Game()
    game.run()

if __name__ == "__main__":
    main()