import config as cfg
import pygame


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
        Game.FONTS["text"] = pygame.font.SysFont("arial", 18)
 
        # Creating the player bitmaps 
        padding = 10
        linewidth = 7
        Game.SYMBOLS["X"] = pygame.Surface((cfg.CELL_SIZE, cfg.CELL_SIZE), pygame.SRCALPHA) 
        pygame.draw.line(Game.SYMBOLS["X"], cfg.COLORS["X"], 
                         (padding, padding), (cfg.CELL_SIZE - padding, cfg.CELL_SIZE - padding), 
                         linewidth)  
        pygame.draw.line(Game.SYMBOLS["X"], cfg.COLORS["X"], 
                         (cfg.CELL_SIZE - padding, padding), (padding, cfg.CELL_SIZE - padding), 
                         linewidth)  
        Game.SYMBOLS["O"] = pygame.Surface((cfg.CELL_SIZE, cfg.CELL_SIZE), pygame.SRCALPHA) 
        pygame.draw.circle(Game.SYMBOLS["O"], cfg.COLORS["O"], 
                           (cfg.CELL_SIZE // 2, cfg.CELL_SIZE // 2), 
                           cfg.CELL_SIZE // 2 - padding, linewidth)

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
                if event.key in (pygame.K_ESCAPE, pygame.K_q):
                    self.running = False
            if Game.STATUS == "start":              
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        Game.STATUS = "play"
            elif Game.STATUS == "play":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.update(action="place", pos=event.pos)
            elif Game.STATUS in ["win", "draw"]:       
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_y:
                        self.reset()
                    elif event.key == pygame.K_n:
                        self.running = False

    def update(self, *args, **kwargs) -> None:
        if Game.STATUS == "play":
            if kwargs.get("action") == "place":
                pos = kwargs.get("pos")
                if cfg.PLAYGROUND.collidepoint(pos):
                    row = (pos[1] - cfg.PLAYGROUND.top) // cfg.CELL_SIZE
                    col = (pos[0] - cfg.PLAYGROUND.left) // cfg.CELL_SIZE
                    if Game.BOARD[row][col] is None:
                        Game.BOARD[row][col] = Game.PLAYER
                        if self.check_winning():        
                            Game.STATUS = "win"
                            return
                        else:
                            self.change_player()
            if self.check_ending():
                Game.STATUS = "draw"

    def check_ending(self) -> bool:
        for row in Game.BOARD:
            for cell in row:
                if cell is None:
                    return False
        return True

    def check_winning(self) -> bool:
        for i in range(3):
            # rows
            if Game.BOARD[i][0] == Game.BOARD[i][1] == Game.BOARD[i][2] is not None:
                return True
            # cols
            if Game.BOARD[0][i] == Game.BOARD[1][i] == Game.BOARD[2][i] is not None:
                return True
        # diagonal
        if Game.BOARD[0][0] == Game.BOARD[1][1] == Game.BOARD[2][2] is not None:
            return True
        # anti-diagonal
        if Game.BOARD[0][2] == Game.BOARD[1][1] == Game.BOARD[2][0] is not None:
            return True
        return False

    def change_player(self) -> None:
        Game.PLAYER = "O" if Game.PLAYER == "X" else "X"

    def draw(self) -> None:
        self.screen.fill(cfg.COLORS["BG"])
        if Game.STATUS == "start":
            self.draw_start()
        elif Game.STATUS == "play":
            self.draw_play()
        elif Game.STATUS == "win":
            self.draw_play()
            self.draw_win()
        elif Game.STATUS == "draw":
            self.draw_play()
            self.draw_draw()
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
        self.draw_message(cfg.MSGSTRINGS["start"])    

    def draw_win(self) -> None:
        self.draw_message(cfg.MSGSTRINGS["win"])

    def draw_draw(self) -> None:
        self.draw_message(cfg.MSGSTRINGS["draw"])

    def draw_message(self, message: dict[str, str|list[str]]) -> None:
        surface = pygame.Surface(cfg.WINDOW.size, pygame.SRCALPHA)
        surface.fill((0, 0, 0, 180))
        headline = Game.FONTS["title"].render(message["headline"], True, cfg.COLORS["TITLE"])
        rect = headline.get_rect()
        rect.centerx = cfg.WINDOW.centerx
        rect.top = 10
        surface.blit(headline, rect)
        left,top = 15,90
        for line in message["message"]:
            textline = Game.FONTS["text"].render(line, True, cfg.COLORS["TEXT"])
            surface.blit(textline, (left, top))
            top += 30
        self.screen.blit(surface, (0, 0))
        

    def reset(self) -> None:
        Game.PLAYER = "X"
        Game.BOARD = [[None] * 3 for _ in range(3)]

def main():
    Game().run()

if __name__ == "__main__":
    main()