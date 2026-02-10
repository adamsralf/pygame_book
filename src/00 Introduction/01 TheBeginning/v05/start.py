import pygame


def main():
    pygame.init()                                   
    screen = pygame.display.set_mode((400,600))     # Create window§\label{srcStart0501}§
    pygame.display.set_caption("Window by Display Module") # Set window title§\label{srcStart0502}§

    running = True
    while running:                                  
        for event in pygame.event.get():            
            if event.type == pygame.QUIT:           
                running = False
        
        screen.fill("white")                        # Fill background with white§\label{srcStart0503}§
        pygame.display.flip()                       # Update display§\label{srcStart0504}§

    pygame.quit()                                   


if __name__ == "__main__":
    main()
