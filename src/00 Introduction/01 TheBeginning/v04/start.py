import pygame


def main():
    pygame.init()
    window = pygame.Window(size=(600, 400), 
        title="My first Pygame program",
        position=(10, 50))  
    window.resizable = True
    window.borderless = False
    window.minimum_size = (300, 200)
    window.maximum_size = (800, 600)
    window.opacity = 0.9
    window.flash(pygame.FLASH_UNTIL_FOCUSED)
    screen = window.get_surface()
    clock = pygame.time.Clock()
 
    counter = 0
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        counter += 1
        window.title = f"My first Pygame program - Frame {counter} at pos {window.position}"
        screen.fill((0, 255, 0))
        window.flip()
        clock.tick(60)
        if counter >= 600:
            running = False

    pygame.quit()


if __name__ == "__main__":
    main()
