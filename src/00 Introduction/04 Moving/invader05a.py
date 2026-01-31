import pygame

import config as cfg


def main():
    pygame.init()
    window = pygame.Window(size=cfg.WINDOW.size, title="Movement", position=(10, 50))
    screen = window.get_surface()
    clock = pygame.time.Clock()

    defender_image = pygame.image.load("images/defender01.png").convert_alpha()
    defender_image = pygame.transform.scale(defender_image, (30, 30))
    defender_rect = defender_image.get_rect()
    defender_rect.centerx = cfg.WINDOW.centerx
    defender_rect.bottom = cfg.WINDOW.height - 5

    running = True
    while running:
        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update
        defender_rect.left += 1

        # Draw
        screen.fill("white")
        screen.blit(defender_image, defender_rect)  # blit can also take a Rect§\label{srcInvader0504}§
        window.flip()
        clock.tick(cfg.FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
