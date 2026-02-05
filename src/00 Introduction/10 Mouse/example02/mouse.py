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
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.window == window_first:    # Check which window the event belongs to§\label{srcMouse0201}§
                    window_id = window_first.id
                    event.window.title = f"Main Window (Mouse Pressed: '{event.button}' at {event.pos})"
                elif event.window == window_second: #§\label{srcMouse0202}§
                    window_id = window_second.id
                    event.window.title = f"Side Window (Mouse Pressed: '{event.button}' at {event.pos})"
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
