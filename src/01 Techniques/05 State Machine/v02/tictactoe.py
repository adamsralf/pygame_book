import pygame

import config as cfg


class Game:
    FONTS = {}
    STATUS = "start"
    PLAYER = "X"
    BOARD = [[None, None, None], [None, None, None], [None, None, None]]
    SYMBOLS = {}

    def __init__(self):
        pygame.init()
        self.window = pygame.Window(size=cfg.WINDOW.size, title=cfg.TITLE)
        self.screen = self.window.get_surface()
        self.clock = pygame.time.Clock()

        Game.FONTS["title"] = pygame.font.SysFont("arial", 36, bold=True)
        Game.FONTS["text"] = pygame.font.SysFont("consolas", 14)
 
        # Creating the player bitmaps §\label{srcTictactoe0201}§
        padding = 10
        linewidth = 7
        cs = cfg.CELL_SIZE
        Game.SYMBOLS["X"] = pygame.Surface((cs, cs), pygame.SRCALPHA)  # §\label{srcTictactoe0202}§ 
        pygame.draw.line(Game.SYMBOLS["X"], cfg.COLORS["X"], 
                         (padding, padding), (cs - padding, cs - padding), 
                         linewidth)  
        pygame.draw.line(Game.SYMBOLS["X"], cfg.COLORS["X"], 
                         (cs - padding, padding), (padding, cs - padding), 
                         linewidth)  
        Game.SYMBOLS["O"] = pygame.Surface((cs, cs), pygame.SRCALPHA)  # §\label{srcTictactoe0203}§
        pygame.draw.circle(Game.SYMBOLS["O"], cfg.COLORS["O"], 
                           (cs // 2, cs // 2), 
                           cs // 2 - padding, linewidth)

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
            if Game.STATUS == "start":              # §\label{srcTictactoe0204}§
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        Game.STATUS = "play"
            elif Game.STATUS == "play":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.update(action="place", pos=event.pos)

    def update(self, *args, **kwargs) -> None:
        if Game.STATUS == "play":
            if kwargs.get("action") == "place":
                pos = kwargs.get("pos")
                if cfg.PLAYGROUND.collidepoint(pos):
                    row = (pos[1] - cfg.PLAYGROUND.top) // cfg.CELL_SIZE  #§\label{srcTictactoe0205}§
                    col = (pos[0] - cfg.PLAYGROUND.left) // cfg.CELL_SIZE #§\label{srcTictactoe0206}§
                    if Game.BOARD[row][col] is None:
                        Game.BOARD[row][col] = Game.PLAYER
                        Game.PLAYER = "O" if Game.PLAYER == "X" else "X"
            if self.check_ending():
                print("Game Over!")
                Game.STATUS = "over"

    def check_ending(self) -> bool:
        for row in Game.BOARD:
            for cell in row:
                if cell is None:
                    return False
        return True

    def draw(self) -> None:
        self.screen.fill(cfg.COLORS["BG"])
        if Game.STATUS == "start":
            self.draw_start()
        elif Game.STATUS == "play":
            self.draw_play()
        self.window.flip()

    def draw_play(self) -> None:
        self.screen.fill(cfg.COLORS["PLAYGROUND"], cfg.PLAYGROUND)
        for i in range(1, 3):
            pygame.draw.line(self.screen, cfg.COLORS["GRID"], (cfg.PLAYGROUND.left + i*cfg.CELL_SIZE, cfg.PLAYGROUND.top), (cfg.PLAYGROUND.left + i*cfg.CELL_SIZE, cfg.PLAYGROUND.bottom), 2)
            pygame.draw.line(self.screen, cfg.COLORS["GRID"], (cfg.PLAYGROUND.left, cfg.PLAYGROUND.top + i*cfg.CELL_SIZE), (cfg.PLAYGROUND.right, cfg.PLAYGROUND.top + i*cfg.CELL_SIZE), 2)
        player = Game.FONTS["text"].render(f"Player {Game.PLAYER}'s turn", True, cfg.COLORS[Game.PLAYER])
        rect = player.get_rect()
        rect.centerx = cfg.PLAYGROUND.centerx
        rect.bottom  = cfg.WINDOW.bottom - 10
        for y in range(3):
            for x in range(3):
                cell = Game.BOARD[y][x]
                if cell is not None:
                    symbol = Game.SYMBOLS[cell]
                    symbol_rect = symbol.get_rect()
                    symbol_rect.center = (cfg.PLAYGROUND.left + (x + 0.5) * cfg.CELL_SIZE, cfg.PLAYGROUND.top + (y + 0.5) * cfg.CELL_SIZE)
                    self.screen.blit(symbol, symbol_rect)
        self.screen.blit(player, rect)

    def draw_start(self) -> None:
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


def main():
    Game().run()

if __name__ == "__main__":
    main()