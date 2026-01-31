from random import randint
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
    def __init__(self, screen: pygame.surface.Surface, layer_count:int=5, peaks: int=35):
        self.screen = screen
        top = cfg.WINDOW.height - cfg.HORIZONT
        self.rect = pygame.rect.Rect(0, top, 
                                     cfg.WINDOW.width, cfg.HORIZONT) # Landing area

        self._layers = []
        dist = self.rect.width // peaks        # Distance between height differences§\label{moonlander02b01}§ 
        for layer_index in range(layer_count): # Build mountain
            mycolor = 180 - layer_index * 20   # Foreground darker, background lighter
            y = self.rect.top - 10 - randint(5, 30)*layer_index # Random starting height§\label{moonlander02b02}§ 
            x = self.rect.left                 # First peak starts at the left§\label{moonlander02b03}§ 
            lofPeaks = [(x, top)]              # The first peak as a point§\label{moonlander02b04}§ 
            for i in range(peaks):             # The other peaks of the layer are generated.§\label{moonlander02b05}§ 
                lofPeaks.append((x, y + randint(-5, 10))) # Random height difference§\label{moonlander02b06}§ 
                x += dist                      # The next peak is further to the right§\label{moonlander02b07}§ 
            lofPeaks.append((self.rect.right, y))   # Last peak is at the right
            lofPeaks.append((self.rect.right, top)) # Base of the mountain range §\label{moonlander02b08}§ 
            self._layers.append({"color":(mycolor, mycolor, mycolor),
                                "peaks":lofPeaks})

    def draw(self):
        pygame.draw.rect(self.screen, (230, 230, 230), self.rect)
        for layer in reversed(self._layers):
            pygame.draw.polygon(
                self.screen,
                layer["color"],
                layer["peaks"]
            )

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




