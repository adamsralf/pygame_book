from time import time

import config as cfg
import pygame


class Defender(pygame.sprite.Sprite):               # Child class of Sprite§\label{srcInvader06a01}§

    def __init__(self) -> None:                     # Constructor§\label{srcInvader06a02}§
        super().__init__()
        self.image = pygame.image.load("images/defender01.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = pygame.FRect(self.image.get_rect())
        self.rect.centerx = cfg.WINDOW.centerx
        self.rect.bottom = cfg.WINDOW.bottom - 5
        self.speed = 300

    def update(self) -> None:                       # State update§\label{srcInvader06a03}§
        newpos = self.rect.move(self.speed * cfg.DELTATIME, 0)
        if newpos.right >= cfg.WINDOW.right:
            self.change_direction()
            newpos.right = cfg.WINDOW.right
        elif newpos.left <= cfg.WINDOW.left:
            self.change_direction()
            newpos.left = cfg.WINDOW.left
        self.rect = newpos

    def draw(self, screen: pygame.Surface) -> None: # Drawing§\label{srcInvader06a04}§
        screen.blit(self.image, self.rect)

    def change_direction(self) -> None:             # OO style§\label{srcInvader06a08}§
        self.speed *= -1


def main():
    pygame.init()
    window = pygame.Window(size=cfg.WINDOW.size, title="Sprite", position=(10, 50))
    screen = window.get_surface()
    clock = pygame.time.Clock()
    defender = Defender()                           # Create object§\label{srcInvader06a05}§

    time_previous = time()
    running = True
    while running:
        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update
        defender.update()                           # Call§\label{srcInvader06a06}§

        # Draw
        screen.fill("white")
        defender.draw(screen)                       # Call§\label{srcInvader06a07}§
        window.flip()

        clock.tick(cfg.FPS)
        time_current = time()
        cfg.DELTATIME = time_current - time_previous
        time_previous = time_current
    pygame.quit()


if __name__ == "__main__":
    main()
