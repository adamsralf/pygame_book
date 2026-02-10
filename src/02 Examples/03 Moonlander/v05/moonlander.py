from random import randint
from time import time
from typing import Any

import config as cfg
import pygame
from continent_polygons import continent_polygons


class Sky:
    def __init__(self, screen:pygame.Surface, star_count: int=200) -> None:
        top = 0 
        left = 0
        width = cfg.WINDOW.width
        height = cfg.WINDOW.height - cfg.HORIZONT
        self.rect = pygame.Rect(top, left, width, height)
        self.screen = screen
        
        self.stars = []       
        for _ in range(star_count):
            self.stars.append({"pos":(randint(2, self.rect.right-1), 
                                       randint(2, self.rect.right-1)),
                          "size":randint(1, 3),
                          "duration": randint(200, 600), 
                          "counter":0,
                          "color":randint(10, 255)})
    
    def update(self) -> None:
        for star in self.stars:
            star["counter"] = (star["counter"] + 1) % (star["duration"] + 1) 
            if star["counter"] == 0:          
                star["color"] = (star["color"] + randint(0, 70)) % 256
                star["size"] = (star["size"] + 1) % 4

    def draw(self) -> None:
        pygame.draw.rect(self.screen, "black", self.rect)
        for star in self.stars:
            pygame.draw.circle(self.screen, (255,255,star["color"]), star["pos"], star["size"])

class Moon:
    def __init__(self, screen: pygame.Surface, layer_count:int=5, peaks: int=35):
        self.screen = screen
        self.surface = pygame.Surface((cfg.WINDOW.width, 
                                                cfg.HORIZONT + layer_count*30),
                                                pygame.SRCALPHA)
        self.rect = self.surface.get_rect()
        self.rect.left = cfg.WINDOW.left
        self.rect.bottom = cfg.WINDOW.bottom
        landingarea = pygame.Rect(0, self.rect.height - cfg.HORIZONT, 
                                     cfg.WINDOW.width, cfg.HORIZONT) 

        layers = []
        for layer_index in range(layer_count): 
            mypeaks = randint(peaks//2, peaks) 
            dist = landingarea.width // mypeaks
            mycolor = 180 - layer_index * 20   
            y = landingarea.top - 10 - randint(5, 10)*layer_index 
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
    def __init__(self, screen:pygame.Surface) -> None:
        self.radius = 80
        self.surface = pygame.Surface(
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

class Lander:
    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen
        self.surface = pygame.Surface((90,81), pygame.SRCALPHA)
        self.surface_thrusting = pygame.Surface((90,81), pygame.SRCALPHA)
        self.rect = self.surface.get_frect()
        self.rect.centerx = cfg.WINDOW.centerx 
        self.rect.top = self.rect.height       
        self.create_lander()                   
        self.thrusting = False                 
        self.velocity = 0                      

    def create_lander(self) -> None:
        # A few abbreviations
        cx = self.rect.width // 2
        cy = self.rect.height //2
        s = self.rect.width // 2
        sur = self.surface

        # Antenna
        pygame.draw.line(sur, (220, 220, 220), (cx, cy - s//2), (cx, cy - s//1.2), 2)
        pygame.draw.circle(sur, (255, 255, 255), (cx, cy - s//1.2), 3)

        # Upper crew module (narrower)
        pygame.draw.polygon(
            sur, (160, 160, 160),
            [(cx - s//4, cy - s//2),
             (cx - s//6, cy - s//3),
             (cx + s//6, cy - s//3),
             (cx + s//4, cy - s//2)]
        )

        # Connector between base and crew module
        conn_color = (160, 160, 160)
        pygame.draw.line(sur, conn_color, (cx - s//3, cy), (cx - s//6, cy - s//3), 2)
        pygame.draw.line(sur, conn_color, (cx, cy), (cx, cy - s//3), 2)
        pygame.draw.line(sur, conn_color, (cx + s//3, cy), (cx + s//6, cy - s//3), 2)

        # Module base (central capsule, light gray)
        pygame.draw.polygon(
            sur, (200, 200, 200),
            [(cx - s//3, cy),
             (cx - s//2, cy + s//2),
             (cx + s//2, cy + s//2),
             (cx + s//3, cy)]
        )

        # Windows in module
        r = 5
        window_color = (50, 50, 50)
        pygame.draw.circle(sur, window_color, (cx, cy+(s//4)), r)
        pygame.draw.circle(sur, window_color, (cx-(s//4), cy+(s//4)), r)
        pygame.draw.circle(sur, window_color, (cx+(s//4), cy+(s//4)), r)

        # Landing legs
        leg_color = (100, 100, 100)
        pygame.draw.line(sur, leg_color, (cx - s//2, cy + s//2), (cx - s, cy + s), 3)
        pygame.draw.line(sur, leg_color, (cx + s//2, cy + s//2), (cx + s, cy + s), 3)
        pygame.draw.line(sur, leg_color, (cx - s//4, cy + s//2), (cx - s//3, cy + s), 3)
        pygame.draw.line(sur, leg_color, (cx + s//4, cy + s//2), (cx + s//3, cy + s), 3)

        # Feet
        feet_color = (150, 150, 150)
        pygame.draw.circle(sur, feet_color, (cx - s + (r+2), cy + s - (r+2)), r-1)
        pygame.draw.circle(sur, feet_color, (cx + s - (r+2), cy + s - (r+2)), r-1)
        pygame.draw.circle(sur, feet_color, (cx - s//3 + (r-4), cy + s - (r+2)), r-1)
        pygame.draw.circle(sur, feet_color, (cx + s//3 - (r-4), cy + s - (r+2)), r-1)

        # Thruster exhaust
        self.surface_thrusting.blit(sur, (0,0))
        pygame.draw.polygon(self.surface_thrusting, (255, 140, 0), [
            (cx - 5, cy + s//2),
            (cx + 5, cy + s//2),
            (cx, cy + s//2 + 20)
        ])

    def update(self, *args: Any, **kwargs: Any) -> None:
        if "action" in kwargs.keys():
            if kwargs["action"] == "thrust":
                self.thrusting = True
            elif kwargs["action"] == "unthrust":
                self.thrusting = False
            elif kwargs["action"] == "move":
                self.move()
            
    def draw(self) -> None:
        if self.thrusting:
            self.screen.blit(self.surface_thrusting, self.rect.topleft)
        else:
            self.screen.blit(self.surface, self.rect.topleft)

    def move(self) -> None:
        if self.thrusting:
            self.velocity += cfg.THRUST * cfg.DELTATIME
        self.velocity += cfg.GRAVITY * cfg.DELTATIME
        self.rect.top += self.velocity * cfg.DELTATIME
        if self.rect.bottom >= cfg.WINDOW.bottom - cfg.HORIZONT:
            self.rect.bottom = cfg.WINDOW.bottom -cfg.HORIZONT

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
                elif event.key == pygame.K_SPACE:
                    self.lander.update(action="thrust")
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    self.lander.update(action="unthrust")

    def update(self) -> None:
        self.background.update()
        self.lander.update(action="move")    

    def draw(self) -> None:
        self.background.draw()
        self.moon.draw()
        self.earth.draw()
        self.lander.draw()
        self.window.flip()

    def restart(self) -> None:
        self.background = Sky(self.screen)
        self.moon = Moon(self.screen)
        self.earth = Earth(self.screen)
        self.lander = Lander(self.screen)
        self.running = True

def main():
    Game().run()

if __name__ == "__main__":
    main()





