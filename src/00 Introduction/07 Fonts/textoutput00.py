
import pygame

import config as cfg


def main():
    pygame.init()
    window = pygame.Window(size=cfg.WINDOW.size, title="Text with Fonts")
    screen = window.get_surface()
    clock = pygame.time.Clock()
    all_sprites = pygame.sprite.Group()

    font = pygame.font.SysFont(None, 24)                             # None -> default font§\label{textoutput00c}§
    text = "This is an example of printing text using a font"

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        all_sprites.update()
        screen.fill("white")
        # Render and center the text
        text_surface = font.render(text, True, (0, 0, 0))           # Render as usual§\label{textoutput00b}§
        text_rect = text_surface.get_rect(center=(cfg.WINDOW.width // 2, cfg.WINDOW.height // 2))
        screen.blit(text_surface, text_rect)
        all_sprites.draw(screen)
        window.flip()
        clock.tick(cfg.FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
