import config as cfg
import pygame
from scenes import DrawState, PlayState, StartState, WinState


class Game:
    FONTS = {}
    PLAYER = "X"
    BOARD = [[None, None, None], [None, None, None], [None, None, None]]
    SYMBOLS = {}
    EVENTS = {
        "START": pygame.event.custom_type(),
        "PLAY": pygame.event.custom_type(),
        "WIN": pygame.event.custom_type(),
        "DRAW": pygame.event.custom_type(),
    }

    def __init__(self):
        pygame.init()
        self.window = pygame.Window(size=cfg.WINDOW.size, title=cfg.TITLE)
        self.screen = self.window.get_surface()
        self.clock = pygame.time.Clock()

        Game.FONTS["title"] = pygame.font.SysFont("arial", 36, bold=True)
        Game.FONTS["text"] = pygame.font.SysFont("consolas", 14)
 
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
        pygame.event.post(pygame.event.Event(Game.EVENTS["START"]))          # §\label{srcTictactoe0701}§

    def run(self) -> None:
        while self.running:
            self.watch_for_events()
            self.update()
            self.draw()
            self.clock.tick(cfg.FPS)
        pygame.quit()
    
    def watch_for_events(self) -> None:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_q):
                    self.running = False
            elif event.type == Game.EVENTS["START"]:
                self.reset()
                self.state = StartState(self)
            elif event.type == Game.EVENTS["PLAY"]:
                self.state = PlayState(self)
            elif event.type == Game.EVENTS["WIN"]:
                self.reset()
                self.state = WinState(self)
            elif event.type == Game.EVENTS["DRAW"]:
                self.reset()
                self.state = DrawState(self)
        self.state.watch_for_events(events)

    def update(self) -> None:
        self.state.update()

    def draw(self) -> None:
        self.screen.fill(cfg.COLORS["BG"])
        self.state.draw()
        self.window.flip()

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