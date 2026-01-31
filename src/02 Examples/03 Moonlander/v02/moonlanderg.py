from random import randint
from time import time

import config as cfg
import pygame

from continent_polygons import continent_polygons


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
        self.surface = pygame.surface.Surface((cfg.WINDOW.width, 
                                                cfg.HORIZONT + layer_count*30),
                                                pygame.SRCALPHA)
        self.rect = self.surface.get_rect()
        self.rect.left = cfg.WINDOW.left
        self.rect.bottom = cfg.WINDOW.bottom
        landingarea = pygame.rect.Rect(0, self.rect.height - cfg.HORIZONT, 
                                     cfg.WINDOW.width, cfg.HORIZONT) 

        layers = []
        for layer_index in range(layer_count):
            mypeaks = randint(peaks//2, peaks)
            dist = landingarea.width // mypeaks 
            mycolor = 180 - layer_index * 20  
            y = landingarea.top - 10 - randint(5, 30)*layer_index 
            x = landingarea.left                
            lofPeaks = [(x, landingarea.top)]   
            for i in range(mypeaks):           
                lofPeaks.append((x, y + randint(-5, 20))) 
                x += dist                      
            lofPeaks.append((landingarea.right, y))   
            lofPeaks.append((landingarea.right, landingarea.top)) 

            poly = []
            for index in range(len(lofPeaks)-1):
                p1 = lofPeaks[index]
                p2 = lofPeaks[index+1]
                p3 = (lofPeaks[index+1][0], landingarea.top)
                p4 = (lofPeaks[index][0], landingarea.top)
                r = randint(-5,5)
                c =  [mc +  r for mc in (mycolor, mycolor, mycolor)]
                poly.append({"points":(p1, p2, p3, p4), "color":c})
            layers.append(poly)

        pygame.draw.rect(self.surface, (230, 230, 230), landingarea)
        for layer in reversed(layers):
            for poly in layer:
                pygame.draw.polygon(
                    self.surface,
                    poly["color"],
                    poly["points"])

    def draw(self):
        self.screen.blit(self.surface, self.rect.topleft)
 
class Earth:
    def __init__(self, screen:pygame.surface.Surface) -> None:
        self.radius = 80
        self.surface = pygame.surface.Surface(
            (2*self.radius, 2*self.radius), 
            pygame.SRCALPHA)
        self.rect = self.surface.get_rect()
        self.rect.left = cfg.WINDOW.right - 200
        self.rect.top = cfg.WINDOW.top + 50
        self.screen = screen

        for a in range(20, 1, -1):
            pygame.draw.circle(self.surface, 
                               (135, 206, 250, 210-a*10),   
                               (self.radius, self.radius), 
                               self.radius-20+a)            
        pygame.draw.circle(self.surface, 
                           (30, 144, 255), 
                           (self.radius, self.radius), 
                           self.radius-20)
        
        for continent in continent_polygons:
            poly = [(self.radius + (0.5*x), self.radius + (0.5*y)) for (x, y) in continent]
            pygame.draw.polygon(self.surface, (181, 150, 116), poly)


    def draw(self) -> None:
        self.screen.blit(self.surface, self.rect.topleft)

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




