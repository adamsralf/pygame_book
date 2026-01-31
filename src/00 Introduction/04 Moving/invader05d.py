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
    defender_speed = defender_rect.width
    defender_direction_h = 1

    running = True
    while running:
        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update
        newpos = defender_rect.move(defender_direction_h * defender_speed, 0)  # New position§\label{srcInvader0510}§
        if newpos.right >= cfg.WINDOW.right:
            defender_direction_h *= -1
            newpos.right = cfg.WINDOW.right     # Align to right edge
        elif newpos.left <= cfg.WINDOW.left:
            defender_direction_h *= -1
            newpos.left = cfg.WINDOW.left       # Align to left edge
        defender_rect = newpos                  # Accept new position§\label{srcInvader0511}§

        # Draw
        screen.fill("white")
        screen.blit(defender_image, defender_rect)
        window.flip()
        clock.tick(cfg.FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
