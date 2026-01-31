import pygame


class Meadow:
    def __init__(self, window: pygame.window.Window, horizon: int) -> None:
        self.window = window
        self.horizon = horizon
        self.color = (50, 180, 50)
        self.lefttop = 0, self.horizon
        self.widthheight= self.window.size[0], self.window.size[1] - self.horizon

    def draw(self) -> None:
        screen = self.window.get_surface()
        pygame.draw.rect(screen, self.color, (self.lefttop, self.widthheight))


class Sky:
    def __init__(self, window: pygame.window.Window, horizon: int) -> None:
        self.window = window
        self.horizon = horizon
        self.color = (100, 150, 255)

    def draw(self) -> None:
        screen = self.window.get_surface()
        pygame.draw.rect(screen, self.color, (0, 0, self.window.size[0], self.horizon))


class Tree:
    def __init__(self, window: pygame.window.Window, horizon: int) -> None:
        self.window = window
        self.colors = [(120, 80, 40), (20, 140, 20)]
        self.start = (100, horizon - 50)

    def draw(self) -> None:
        screen = self.window.get_surface()
        pygame.draw.rect(screen, self.colors[0], (self.start, (20, 60)))
        pygame.draw.circle(screen, self.colors[1], (self.start[0]+10, self.start[1]-20), 35)


def main():
    size = (600, 400)
    pygame.init()
    window = pygame.Window( size=size, title = "A Peaceful Day")         
    clock = pygame.time.Clock()
    horizon = 250
    meadow = Meadow(window, horizon)                
    sky = Sky(window, horizon)                      
    tree = Tree(window, horizon)                    # §\label{srcLandscape0401}§


    running = True
    while running:
        # Watch for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Updates

        # Draw 
        meadow.draw()                               
        sky.draw()
        tree.draw()                                 # §\label{srcLandscape0402}§
        window.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()









