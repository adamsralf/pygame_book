import pygame


def main():
    pygame.init()
    window = pygame.Window(size=(200, 200), title="MessageBoxes")
    screen = window.get_surface()
    clock = pygame.time.Clock()


    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_1:
                    pygame.display.message_box("Information",   #§\label{srcMessageboxes01}§ 
                                               "This is an info message box.", 
                                               "info")  
                elif event.key == pygame.K_2:
                    a = pygame.display.message_box("Warning",   #§\label{srcMessageboxes02}§
                                                   "This is a warning message box. Procced?", 
                                                   "warn", 
                                                   buttons=["Yes", "No"])
                    print("User selected:", a)
                elif event.key == pygame.K_3:
                    pygame.display.message_box("Error",         #§\label{srcMessageboxes03}§
                                               "This is an error message box.", 
                                               "error")
        screen.fill("white")
        window.flip()
        clock.tick(10)

    pygame.quit()


if __name__ == "__main__":
    main()
