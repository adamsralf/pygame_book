import pygame

import config as cfg


class TextSprite(pygame.sprite.Sprite):
    def __init__(self, fontname: str, fontsize: int = 24, fontcolor: list[int] = [255, 255, 255], text: str = "") -> None:
        super().__init__()
        self.image = None
        self.fontname = fontname
        self.fontsize = fontsize
        self.fontcolor = fontcolor
        self.fontsize_update(0)
        if text == "":
            self.text = f"{self.fontname}: abcdefghijklmnopqrstxyzßöäü0123456789"
        else:
            self.text = text
        self.render()

    def render(self) -> None:
        self.image = self.font.render(self.text, True, self.fontcolor)
        self.rect = self.image.get_rect()

    def fontsize_update(self, step: int = 1) -> None:
        self.fontsize += step
        self.font = pygame.font.Font(pygame.font.match_font(self.fontname), self.fontsize)  #§\label{srcTextoutputFontlist03}§

    def fontcolor_update(self, delta: list[int]) -> None:
        for i in range(3):
            self.fontcolor[i] = (self.fontcolor[i] + delta[i]) % 256

    def update(self) -> None:
        self.render()


class BigImage(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.offset = pygame.Rect(cfg.WINDOW)

    def create_image(self, width: int, height: int) -> None:
        self.image_total = pygame.Surface((width, height))
        self.image_total.fill("white")
        self.update(0)

    def update(self, delta: int) -> None:  # Compute offset§\label{srcTextoutputFontlist01}§
        if self.offset.top + delta >= 0:
            if self.offset.bottom + delta <= self.image_total.get_rect().height:
                self.offset.move_ip(0, delta)
            else:
                self.offset.bottom = self.image_total.get_rect().height
        else:
            self.offset.top = 0
        self.image = self.image_total.subsurface(self.offset)
        self.rect = self.image.get_rect()


def main():
    pygame.init()
    window = pygame.Window(size=cfg.WINDOW.size, title="List of all Installed Fonts", position=(10, 50))
    screen = window.get_surface()
    clock = pygame.time.Clock()

    fonts = pygame.font.get_fonts()  # All installed Fonts§\label{srcTextoutputFontlist02}§

    list_of_fontsprites = pygame.sprite.Group()
    height = 0
    width = 0
    for name in sorted(fonts):
        try:
            t = TextSprite(name, 24, "black")
            t.rect.top = height
            height += t.rect.height
            width = t.rect.width if t.rect.width > width else width
            list_of_fontsprites.add(t)
        except OSError as err:
            print(f"OS error {err}")
        except pygame.error as perr:
            print(f"Pygame error: {perr} with font {name}")

    bigimage = pygame.sprite.GroupSingle(BigImage())
    bigimage.sprite.create_image(width, height)
    list_of_fontsprites.draw(bigimage.sprite.image_total)  # §\label{srcTextoutputFontlist04}§

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_UP:
                    bigimage.update(-cfg.WINDOW.height // 2)
                if event.key == pygame.K_DOWN:
                    bigimage.update(cfg.WINDOW.height // 2)

        bigimage.draw(screen)
        window.flip()
        clock.tick(cfg.FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
