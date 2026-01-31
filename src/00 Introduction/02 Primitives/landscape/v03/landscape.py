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

def main():
    size = (600, 400)
    pygame.init()
    window = pygame.Window( size=size, title = "A Peaceful Day")         
    clock = pygame.time.Clock()
    horizon = 250
    meadow = Meadow(window, horizon)                
    sky = Sky(window, horizon)                      # §\label{srcLandscape0301}§


    running = True
    while running:
        # Watch for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Updates

        # Draw 
        meadow.draw()                               
        sky.draw()                                  # §\label{srcLandscape0302}§
        window.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()









