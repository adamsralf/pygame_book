import pygame


def main():
    pygame.init()
    window = pygame.Window(size=(512, 512), title="Draw a Part of a Bitmap")
    screen = window.get_surface()
    clock = pygame.time.Clock()

    image = pygame.image.load("images/forest_tiles.png")
    x, y = 0, 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_RIGHT:
                    x += 32
                elif event.key == pygame.K_LEFT:
                    x -= 32
                if event.key == pygame.K_DOWN:
                    y += 32
                if event.key == pygame.K_UP:
                    y -= 32
        x = pygame.math.clamp(x, 0, 512-32)
        y = pygame.math.clamp(y, 0, 512-32)

        screen.fill("white")
        screen.blit(image, (0, 0))
        pygame.draw.rect(screen, "red", (x, y, 32, 32), 2)   # Draw rectangle around the part§\label{srcBlitofparts02}§
        screen.blit(image, (512-32, 512-32), (x, y, 32, 32)) # Blit a part of the image§\label{srcBlitofparts01}§
        window.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
