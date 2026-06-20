import pygame

import config as cfg


class Game:
    FONTS = {}

    def __init__(self):
        pygame.init()
        self.window = pygame.Window(size=cfg.WINDOW.size, title=cfg.TITLE)
        self.screen = self.window.get_surface()
        self.clock = pygame.time.Clock()

        Game.FONTS["title"] = pygame.font.SysFont("arial", 36, bold=True)
        Game.FONTS["text"] = pygame.font.SysFont("consolas", 14)

        self.running = True

    def run(self) -> None:
        while self.running:
            self.watch_for_events()
            self.update()
            self.draw()
            self.clock.tick(cfg.FPS)
        pygame.quit()
    
    def watch_for_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

    def update(self) -> None:
        pass

    def draw(self) -> None:
        self.screen.fill(cfg.COLORS["BG"])
        welcome = "Welcome to TicTacToe"
        text = [
            "Place three of your symbols in one straight line to win.",
            "The line can be horizontal, vertical, or diagonal.",
            "After each move, the other player takes a turn.",
            "",
            "Player 1: X",
            "Player 2: O",
            "",
            "Keys:",
            "SPACE    - start",
            "P        - pause",
            "H        - help",
            "ESC / Q  - quit",
        ]
        
        headline = Game.FONTS["title"].render(welcome, True, cfg.COLORS["TITLE"])
        rect = headline.get_rect()
        rect.centerx = cfg.WINDOW.centerx
        rect.top = 10
        self.screen.blit(headline, rect)
        left,top = 15,90
        for line in text:
            textline = Game.FONTS["text"].render(line, True, cfg.COLORS["TEXT"])
            self.screen.blit(textline, (left, top))
            top += 30
        self.window.flip()


def main():
    Game().run()

if __name__ == "__main__":
    main()