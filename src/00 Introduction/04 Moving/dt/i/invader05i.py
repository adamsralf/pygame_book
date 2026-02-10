from time import time

import config as cfg
import pygame


def main():
    pygame.init()
    window = pygame.Window(size=cfg.WINDOW.size, title="Movement", position=(10, 50))
    screen = window.get_surface()
    clock = pygame.time.Clock()

    defender_image = pygame.image.load("images/defender01.png").convert_alpha()
    defender_image = pygame.transform.scale(defender_image, (30, 30))
    defender_rect = pygame.FRect(defender_image.get_rect())
    defender_rect.centerx = cfg.WINDOW.centerx
    defender_rect.bottom = cfg.WINDOW.height - 5
    defender_speed = 600
    defender_direction_v = -1

    start_time = pygame.time.get_ticks()
    time_previous = time()  # remember start time§\label{srcInvader05i01}§
    running = True
    while running:
        if pygame.time.get_ticks() > start_time + cfg.LIMIT:
            defender_speed = 0
        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update
        defender_rect.top += defender_direction_v * defender_speed * cfg.DELTATIME
        if defender_rect.bottom >= cfg.WINDOW.height:
            defender_direction_v *= -1
        elif defender_rect.top <= 0:
            defender_direction_v *= -1

        # Draw
        screen.fill("white")
        pygame.draw.line(screen, "red", (0, 315), (cfg.WINDOW.width, 315), 2)
        screen.blit(defender_image, defender_rect)
        window.flip()
        clock.tick(cfg.FPS)
        time_current = time()  # remember stop time§\label{srcInvader05i02}§
        cfg.DELTATIME = time_current - time_previous  # Time consumption§\label{srcInvader05i03}§
        time_previous = time_current  # New start time§\label{srcInvader05i04}§
    pygame.quit()


if __name__ == "__main__":
    main()
