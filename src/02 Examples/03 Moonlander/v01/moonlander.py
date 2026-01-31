from time import time

import config as cfg
import pygame


class Sky:
    def __init__(self, screen:pygame.surface.Surface) -> None:
        top = 0 
        left = 0
        width = cfg.WINDOW.width
        height = cfg.WINDOW.height - cfg.HORIZONT
        self.rect = pygame.rect.Rect(top, left, width, height)
        self.screen = screen

    def draw(self) -> None:
        pygame.draw.rect(self.screen, "black", self.rect)

class Moon:
    def __init__(self, screen:pygame.surface.Surface) -> None:
        top = 0 
        left = cfg.WINDOW.height - cfg.HORIZONT
        width = cfg.WINDOW.width
        height = cfg.HORIZONT
        self.rect = pygame.rect.Rect(top, left, width, height)
        self.screen = screen


    def draw(self) -> None:
        pygame.draw.rect(self.screen, "gray", self.rect)

class Earth:
    def __init__(self, screen:pygame.surface.Surface) -> None:
        self.radius = 80
        left = cfg.WINDOW.right - 2*self.radius - 30
        top = cfg.WINDOW.top + 15
        width = 2*self.radius
        height = 2*self.radius
        self.rect = pygame.rect.Rect(left, top, width, height)
        self.screen = screen


    def draw(self) -> None:
        pygame.draw.circle(self.screen, "blue", self.rect.center, self.radius)

class Game:
    def __init__(self) -> None:
        pygame.init()
        self.window = pygame.Window(size=cfg.WINDOW.size, title="MyMoonlander", position=pygame.WINDOWPOS_CENTERED)
        self.screen = self.window.get_surface()
        self.clock = pygame.time.Clock()


    def run(self) -> None:
        self.restart()
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
                elif event.key == pygame.K_r:
                    self.restart()

    def update(self) -> None:
        pass

    def draw(self) -> None:
        self.background.draw()
        self.moon.draw()
        self.earth.draw()
        self.window.flip()

    def restart(self) -> None:
        self.background = Sky(self.screen)
        self.moon = Moon(self.screen)
        self.earth = Earth(self.screen)
        self.running = True

def main():
    Game().run()

if __name__ == "__main__":
    main()




