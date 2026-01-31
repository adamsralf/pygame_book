import pygame


def main():
    pygame.init()
    window_first = pygame.Window(size=(300, 50), 
        title="Main Window",
        position=(500, 50))  
    window_second = pygame.Window(size=(300, 50), 
        title="Side Window",
        position=(820, 50))  
    screen_first = window_first.get_surface()
    screen_second = window_second.get_surface()
    clock = pygame.time.Clock()

 
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.WINDOWCLOSE:  
                running = False
                event.window.destroy()
            elif event.type == pygame.KEYDOWN:
                if event.window == window_first:    # Check which window the event belongs to§\label{srcKeyboard03a}§
                    window_id = window_first.id
                    event.window.title = "Main Window (Key Pressed: '" + pygame.key.name(event.key) + "')"
                elif event.window == window_second: #§\label{srcKeyboard03b}§
                    window_id = window_second.id
                    event.window.title = "Side Window (Key Pressed: '" + pygame.key.name(event.key) + "')"
                else:
                    window_id = None
                
                print(f"ID {window_id}: {event.window.title}")
        if running:
            screen_first.fill((0, 255, 0))
            window_first.flip()
            screen_second.fill((255, 0, 0))
            window_second.flip()
            clock.tick(60)         

    pygame.quit()


if __name__ == "__main__":
    main()
