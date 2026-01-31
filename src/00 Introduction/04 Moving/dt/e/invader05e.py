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
    defender_rect.bottom = cfg.WINDOW.bottom - 5
    defender_speed = 2
    defender_direction_v = -1

    start_time = pygame.time.get_ticks()                        # Movement starts§\label{srcInvader05e02}§
    running = True
    while running:
        if pygame.time.get_ticks() > start_time + cfg.LIMIT:    # Ready?§\label{srcInvader05e04}§
            defender_speed = 0
        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update
        defender_rect.top += defender_direction_v * defender_speed  # New height§\label{srcInvader05e03}§
        if defender_rect.bottom >= cfg.WINDOW.bottom:
            defender_direction_v *= -1
        elif defender_rect.top <= 0:
            defender_direction_v *= -1

        # Draw
        screen.fill("white")
        screen.blit(defender_image, defender_rect)
        window.flip()
        clock.tick(cfg.FPS)
    print(f"top={defender_rect.top}")

    pygame.quit()


if __name__ == "__main__":
    main()
