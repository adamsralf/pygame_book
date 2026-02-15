from typing import Tuple

import pygame

import config as cfg


class TextSprite(pygame.sprite.Sprite):
    def __init__(self, fontsize: int, fontcolor: list[int], 
                center: Tuple[int, int], text: str = "Hello World!") -> None:
        super().__init__()
        self.image = None
        self.rect = None
        self.fontsize = fontsize
        self.fontcolor = fontcolor
        self.fontsize_update(0)     # 0! §\label{srcTextoutputSimple02}§
        self.text = text
        self.center = center
        self.dirty = True
        self.render()               # §\label{srcTextoutputSimple03}§

    def render(self) -> None:
        self.image = self.font.render(self.text, True, self.fontcolor)  # Bitmap §\label{srcTextoutputSimple04}§
        self.rect = self.image.get_rect()
        self.rect.center = self.center
        self.dirty = False

    def text_update(self, text: str) -> None:
        self.text = text
        self.dirty = True

    def fontsize_update(self, step: int = 1) -> None:
        self.fontsize += step
        self.font = pygame.font.SysFont(None, self.fontsize)  # §\label{srcTextoutputSimple01}§
        self.dirty = True

    def fontcolor_update(self, delta: Tuple[int, int, int]) -> None:
        for i in range(3):
            self.fontcolor[i] = (self.fontcolor[i] + delta[i]) % 256
        self.dirty = True

    def update(self) -> None:
        if self.dirty:
            self.render()


def main():
    pygame.init()
    window = pygame.Window(size=cfg.WINDOW.size, title="Text with Fonts", position=(10, 50))
    screen = window.get_surface()
    clock = pygame.time.Clock()

    hello = TextSprite(24, [255, 255, 255], (cfg.WINDOW.center))  # §\label{srcTextoutputSimple07}§
    info = TextSprite(12, [255, 0, 0], (cfg.WINDOW.centerx, cfg.WINDOW.bottom - 20))  # Fontinfo§\label{srcTextoutputSimple08}§
    all_sprites = pygame.sprite.Group()
    all_sprites.add(hello, info)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_KP_PLUS or event.key == pygame.K_PLUS:   # Bigger§\label{srcTextoutputSimple05}§
                    hello.fontsize_update(+1)
                elif event.key == pygame.K_KP_MINUS or event.key == pygame.K_MINUS: # Smaller§\label{srcTextoutputSimple06}§
                    hello.fontsize_update(-1)
                elif event.key == pygame.K_r:
                    if event.mod & pygame.KMOD_SHIFT:
                        hello.fontcolor_update((-1, 0, 0))  # Less red§\label{srcTextoutputSimple09}§
                    else:
                        hello.fontcolor_update((+1, 0, 0))  # More red§\label{srcTextoutputSimple10}§
                elif event.key == pygame.K_g:
                    if event.mod & pygame.KMOD_SHIFT:
                        hello.fontcolor_update((0, -1, 0))  # Less green
                    else:
                        hello.fontcolor_update((0, +1, 0))  # More green
                elif event.key == pygame.K_b:
                    if event.mod & pygame.KMOD_SHIFT:
                        hello.fontcolor_update((0, 0, -1))  # Less blue
                    else:
                        hello.fontcolor_update((0, 0, +1))  # More blue

        info.text_update(f"size={hello.fontsize}, r={hello.fontcolor[0]}, g={hello.fontcolor[1]}, b={hello.fontcolor[2]}")
        all_sprites.update()
        screen.fill("cornsilk1")
        all_sprites.draw(screen)
        window.flip()
        clock.tick(cfg.FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
