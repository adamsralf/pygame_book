import config as cfg
import pygame
from scenes import DrawState, HelpState, PlayState, StartState, WinState
from scenes.state import State


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
        "HELP": pygame.event.custom_type(),
        "UNHELP": pygame.event.custom_type(),
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
        self.stack_state: list[State] = [] # stack of states (bottom .. top)§\label{srcTictactoe0801}§
        pygame.event.post(pygame.event.Event(Game.EVENTS["START"]))

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
                self.replace_state(StartState(self))
            elif event.type == Game.EVENTS["PLAY"]:
                self.replace_state(PlayState(self))
            elif event.type == Game.EVENTS["WIN"]:
                self.push_state(WinState(self))
            elif event.type == Game.EVENTS["DRAW"]:
                self.push_state(DrawState(self))
            elif event.type == Game.EVENTS["HELP"]:
                self.push_state(HelpState(self))
            elif event.type == Game.EVENTS["UNHELP"]:
                self.pop_state()
        if self.current_state:
            self.current_state.watch_for_events(events)

    def update(self) -> None:
        if self.current_state:
            self.current_state.update()

    def draw(self) -> None:
        self.screen.fill(cfg.COLORS["BG"])
        for state in self.stack_state:
            state.draw()
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

    def push_state(self, state: State) -> None:
        self.stack_state.append(state)

    def pop_state(self) -> None:
        if self.stack_state:
            self.stack_state.pop()
        if not self.stack_state:
            self.running = False

    def replace_state(self, state: State) -> None:
        self.stack_state = [state]

    @property
    def current_state(self) -> State | None:
        return self.stack_state[-1] if self.stack_state else None



def main():
    Game().run()

if __name__ == "__main__":
    main()