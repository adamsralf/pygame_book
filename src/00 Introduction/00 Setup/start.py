import pygame  # Pygame-Modul (also for pygame-ce!)


def main():
    pygame.init()                                  
    window = pygame.Window(size=(400, 100))        
    window.title = "Pygame test"       
    screen = window.get_surface()                  

    running = True
    while running:                                 
        for event in pygame.event.get():           
            if event.type == pygame.QUIT:          
                running = False
        screen.fill("white")                   
        window.flip()                              

    pygame.quit()                                  


if __name__ == "__main__":
    main()
