import math

import pygame


class Meadow:
    def __init__(self, window: pygame.window.Window, horizon: int) -> None:
        self.window = window
        self.pos = 0, horizon
        widthheight = self.window.size[0], self.window.size[1] - horizon
        self.surface = pygame.Surface(widthheight)                      # Meadow surface§\label{srcLandscapeBit00}§
        self.surface.fill((50, 180, 50))

    def draw(self) -> None:
        screen = self.window.get_surface()
        screen.blit(self.surface, self.pos)

class Sky:
    def __init__(self, window: pygame.window.Window, horizon: int) -> None:
        self.window = window
        self.pos = 0, 0
        self.color = (100, 150, 255)
        self.surface = pygame.Surface((self.window.size[0], horizon))   # Sky surface§\label{srcLandscapeBit02}§
        self.surface.fill(self.color)

    def update(self, progress: float) -> None:
        brightness = max(0, min(1, math.sin(progress * math.pi)))
        blue = int(80 + brightness * 120)
        self.color = (100, blue, 235)
        self.surface.fill(self.color)

    def draw(self) -> None:
        screen = self.window.get_surface()
        screen.blit(self.surface, self.pos)

class Tree:
    def __init__(self, window: pygame.window.Window, horizon: int) -> None:
        self.window = window
        self.pos = (65, horizon - 80)
        self.surface = pygame.Surface((90, 120), pygame.SRCALPHA)       # Tree surface§\label{srcLandscapeBit01}§
        pygame.draw.rect(self.surface, (120, 80, 40), (35, 60, 20, 60))
        pygame.draw.circle(self.surface, (20, 140, 20), (45, 35), 35)

    def draw(self) -> None:
        screen = self.window.get_surface()
        screen.blit(self.surface, self.pos)


class House:
    def __init__(self, window: pygame.window.Window, horizon: int) -> None:
        self.window = window
        self.pos = (200, horizon - 70)
        self.surface = pygame.Surface((150, 160), pygame.SRCALPHA)     # House surface§\label{srcLandscapeBit03}§
        pygame.draw.rect(self.surface, (200, 100, 100), ((0,60), (150, 100)))
        pygame.draw.polygon(
            self.surface,
            (150, 50, 50),
            [(0,60), (75, 0), (150, 60)]
        )
        pygame.draw.rect(self.surface, (100, 60, 30), (60, 100, 30, 60))

    def draw(self) -> None:
        screen = self.window.get_surface()
        screen.blit(self.surface, self.pos)


class Sun:
    def __init__(self, window: pygame.window.Window, horizon: int) -> None:
        self.speed = 1
        radius = 40
        self.pos = [-radius, 0]               
        self.horizon = horizon
        self.window = window
        self.surface = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)    # Sun surface§\label{srcLandscapeBit04}§
        pygame.draw.circle(self.surface,  (255, 220, 0), (radius, radius), radius)

    def update(self) -> float:
        self.pos[0] += self.speed
        progress = self.pos[0] / self.window.size[0]  # 0.0 -> 1.0
        self.pos[1] = round(self.horizon * (1 - math.sin(progress * math.pi)))
        return progress

    def draw(self) -> None:
        screen = self.window.get_surface()
        screen.blit(self.surface, (self.pos[0], self.pos[1]))



def main():
    size = (600, 400)
    pygame.init()
    window = pygame.Window( size=size, title = "A Peaceful Day")         
    clock = pygame.time.Clock()
    horizon = 250
    meadow = Meadow(window, horizon)                
    sky = Sky(window, horizon)                      
    tree = Tree(window, horizon)                    
    house = House(window, horizon)                    
    sun = Sun(window, horizon) 


    running = True
    while running:
        # Watch for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Updates
        progress = sun.update()
        sky.update(progress)

        # Draw 
        sky.draw()
        sun.draw()   
        meadow.draw()                               
        tree.draw()
        house.draw()
        window.flip()       
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()












