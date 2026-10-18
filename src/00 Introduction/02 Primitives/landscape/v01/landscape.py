import pygame


def main():
    size = (600, 400)
    pygame.init()
    window = pygame.Window(size=size, title = "A Peaceful Day")         
    screen = window.get_surface()   # required! §\label{srcLandscape0101}§
    clock = pygame.time.Clock()
    horizont = 250

    running = True
    while running:
        # Watch for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Updates

        # Draw 
        window.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()



