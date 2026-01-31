import pygame  # Pygame-Modul (also for pygame-ce!)§\label{srcStart0001}§


def main():
    pygame.init()                                   # Start subsystem§\label{srcStart0003}§
    window = pygame.Window(size=(600, 400))         # Create Window§\label{srcStart0005}§
    window.title = "My first Pygame program"        # Set window title§\label{srcStart0004}§
    window.position = (10, 50)                      # Set window position§\label{srcStart0002}§
    screen = window.get_surface()                   # Get the window's bitmap surface§\label{srcStart0012}§

    running = True
    while running:                                  # Main program loop: start§\label{srcStart0006}§
        for event in pygame.event.get():            # Retrieve events§\label{srcStart0007}§
            if event.type == pygame.QUIT:           # Window X clicked?§\label{srcStart0008}§
                running = False
        screen.fill((0, 255, 0))                    # Fill playground§\label{srcStart0009}§
        window.flip()                               # Swap double buffer§\label{srcStart0010}§

    pygame.quit()                                   # Shut down subsystem§\label{srcStart0011}§


if __name__ == "__main__":
    main()
