
import pygame

import config as cfg


class Spritelib(pygame.sprite.Sprite):

    def __init__(self, filename: str) -> None:
        super().__init__()
        self.image = pygame.image.load(cfg.imagepath(filename)).convert()
        self.rect = self.image.get_rect()
        self.nof = {"rows": 4, "cols": 10}
        self.letter = {"width": 18, "height": 18}
        self.offset = {"h": 6, "v": 6}
        self.distance = {"h": 14, "v": 14}

    def draw(self, screen: pygame.surface.Surface) -> None:
        screen.blit(self.image, self.rect)


class Letters(object):

    def __init__(self, spritelib: Spritelib, colornumber: int) -> None:
        super().__init__()
        self.spritelib = spritelib
        self.letters: dict[str, pygame.surface.Surface] = {}
        self.create_letter_bitmap(colornumber)

    def create_letter_bitmap(self, colornumber: int):
        lettername = (
            "0",
            "1",  # The rows between 34 and 62 are skipped!!
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
            "a",
            "b",
            "c",
            "d",
            "e",
            "f",
            "g",
            "h",
            "i",
            "j",
            "k",
            "l",
            "m",
            "n",
            "o",
            "p",
            "q",
            "r",
            "s",
            "t",
            "u",
            "v",
            "w",
            "x",
            "y",
            "z",
            "-",
            " ",
            "copy",
            "square",
        )  # §\label{srcTextbitmaps0000}§
        index = 0
        startpos = (
            self.spritelib.offset["h"],
            self.spritelib.offset["v"] + colornumber * self.spritelib.nof["rows"] * (self.spritelib.letter["height"] + self.spritelib.distance["v"]),
        )  # §\label{srcTextbitmaps0001}§
        for row in range(self.spritelib.nof["rows"]):           # Rows§\label{srcTextbitmaps0002}§
            for col in range(self.spritelib.nof["cols"]):       # Columns§\label{srcTextbitmaps0003}§
                left = startpos[0] + col * (self.spritelib.letter["width"] + self.spritelib.distance["h"])  # §\label{srcTextbitmaps0004}§
                top = startpos[1] + row * (self.spritelib.letter["height"] + self.spritelib.distance["v"])  # §\label{srcTextbitmaps0005}§
                width  = self.spritelib.letter["width"]         # Size§\label{srcTextbitmaps0006}§
                height = self.spritelib.letter["height"]
                r = pygame.rect.Rect(left, top, width, height)
                self.letters[lettername[index]] = self.spritelib.image.subsurface(r)  # §\label{srcTextbitmaps0007}§
                index += 1

    def get_letter(self, letter: str) -> pygame.surface.Surface:
        if letter in self.letters:
            return self.letters[letter]
        else:
            return self.letters["square"]

    def get_text(self, text: str) -> pygame.surface.Surface:
        l = len(text) * self.spritelib.letter["width"]
        h = self.spritelib.letter["height"]
        bitmap = pygame.Surface((l, h))
        bitmap.set_colorkey((0, 0, 0))
        for a in range(len(text)):
            bitmap.blit(self.get_letter(text[a]), (a * self.spritelib.letter["width"], 0))
        return bitmap


class TextBitmaps(object):

    def __init__(self) -> None:
        pygame.init()
        self.window = pygame.Window(size=cfg.WINDOW.size, title="Text Output with Bitmaps", position=(10, 50))
        self.screen = self.window.get_surface()
        self.clock = pygame.time.Clock()

        self.filename = "chars.png"
        self.running = False
        self.input = ""

    def watch_for_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_BACKSPACE:
                    self.input = self.input[:-1] # Remove last character§\label{srcTextbitmaps0008}§
                else:
                    self.input += event.unicode  # Keyboard input as Unicode character§\label{srcTextbitmaps0009}§

    def run(self) -> None:
        spritelib = Spritelib(self.filename)
        letters = Letters(spritelib, 2)
        self.running = True
        while self.running:
            self.watch_for_events()
            self.screen.fill((200, 200, 200))
            self.screen.blit(letters.get_text(self.input), (400, 200))
            spritelib.draw(self.screen)
            self.window.flip()
            self.clock.tick(cfg.FPS)

        pygame.quit()


def main():

    demo = TextBitmaps()
    demo.run()


if __name__ == "__main__":
    main()
