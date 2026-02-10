from random import randint
from time import time

import config as cfg
import pygame


class Sky:
    def __init__(self, screen:pygame.Surface) -> None:
        top = 0 
        left = 0
        width = cfg.WINDOW.width
        height = cfg.WINDOW.height - cfg.HORIZONT
        self.rect = pygame.Rect(top, left, width, height)
        self.screen = screen

    def draw(self) -> None:
        pygame.draw.rect(self.screen, "black", self.rect)

class Moon:
    def __init__(self, screen: pygame.Surface, layer_count:int=5, peaks: int=35):
        self.screen = screen
        top = cfg.WINDOW.height - cfg.HORIZONT
        self.rect = pygame.Rect(0, top, 
                                     cfg.WINDOW.width, cfg.HORIZONT) 

        self._layers = []
        for layer_index in range(layer_count):
            mypeaks = randint(peaks//2, peaks)      # Number varies§\label{moonlander02c01}§
            dist = self.rect.width // mypeaks       # Distance between height differences§\label{moonlander02c02}§
            mycolor = 180 - layer_index * 20  
            y = self.rect.top - 10 - randint(5, 30)*layer_index 
            x = self.rect.left
            lofPeaks = [(x, top)]
            for i in range(mypeaks): 
                lofPeaks.append((x, y + randint(-5, 20))) 
                x += dist 
            lofPeaks.append((self.rect.right, y))
            lofPeaks.append((self.rect.right, top)) 

            poly = []                               # A polygon path§\label{moonlander02c03}§
            for index in range(len(lofPeaks)-1):
                p1 = lofPeaks[index]
                p2 = lofPeaks[index+1]
                p3 = (lofPeaks[index+1][0], self.rect.top)
                p4 = (lofPeaks[index][0], self.rect.top)
                r = randint(-5,5)
                c =  [mc +  r for mc in (mycolor, mycolor, mycolor)]
                poly.append({"points":(p1, p2, p3, p4), "color":c})
            self._layers.append(poly)

    def draw(self):
        pygame.draw.rect(self.screen, (230, 230, 230), self.rect)
        for layer in reversed(self._layers):
            for poly in layer:
                pygame.draw.polygon(
                    self.screen,
                    poly["color"],
                    poly["points"])

class Earth:
    def __init__(self, screen:pygame.Surface) -> None:
        self.radius = 80
        left = cfg.WINDOW.right - 2*self.radius - 30
        top = cfg.WINDOW.top + 15
        width = 2*self.radius
        height = 2*self.radius
        self.rect = pygame.Rect(left, top, width, height)
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




