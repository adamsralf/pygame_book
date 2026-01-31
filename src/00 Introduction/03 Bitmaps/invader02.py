import pygame

import config as cfg


def main():
    pygame.init()
    window = pygame.Window(
        size=(cfg.WINDOW_WIDTH, cfg.WINDOW_HEIGHT), 
        title="Load and Draw of Bitmaps", 
        position=(10, 50))
    screen = window.get_surface()
    clock = pygame.time.Clock()

    defender_image = pygame.image.load("images/defender01.png").convert() # to display format§\label{srcInvader0201}§
    defender_image = pygame.transform.scale(defender_image, (30, 30))     # Scale surface§\label{srcInvader0202}§

    enemy_image = pygame.image.load("images/alienbig0101.png").convert()
    enemy_image = pygame.transform.scale(enemy_image, (50, 45))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill("white")
        screen.blit(enemy_image, (10, 10))
        screen.blit(defender_image, (10, 80))
        window.flip()
        clock.tick(cfg.FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
