from time import time

import pygame

import config as cfg
from scenes import GameOverState, HelpState, PauseState, PlayState, StartState, State


class Game:
    def __init__(self):
        pygame.init()
        self.window = pygame.Window(size=cfg.WINDOW.size)
        self.window.title = cfg.CAPTION
        self.screen = self.window.get_surface()
        self.clock = pygame.time.Clock()
        self.running = True
        self.events = {
            "PLAY": pygame.event.custom_type(),
            "GAME_OVER": pygame.event.custom_type(),
            "NEW_GAME": pygame.event.custom_type(),
            "PAUSE": pygame.event.custom_type(),
            "HELP": pygame.event.custom_type(),
            "UNHELP": pygame.event.custom_type(),
            "UNPAUSE": pygame.event.custom_type(),
        }
        self.stack_state: list[State] = [StartState(self)]

    def run(self):
        time_previous = time()
        while self.running:
            self.watch_for_events()
            self.update()
            self.draw()
            self.clock.tick(cfg.FPS)
            time_current = time()
            cfg.DELTATIME = time_current - time_previous
            time_previous = time_current
        pygame.quit()

    def watch_for_events(self)-> None:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key in (pygame.K_ESCAPE, pygame.K_q):
                self.running = False
            elif event.type == self.events["PLAY"]:
                self.replace_state(PlayState(self))
            elif event.type == self.events["GAME_OVER"]:
                self.replace_state(GameOverState(self))
            elif event.type == self.events["NEW_GAME"]:
                self.start_new_game()
            elif event.type == self.events["PAUSE"]:
                self.push_state(PauseState(self))
            elif event.type == self.events["HELP"]:
                self.push_state(HelpState(self))
            elif event.type == self.events["UNHELP"] or event.type == self.events["UNPAUSE"]:
                self.pop_state()

        if self.current_state:
            self.current_state.watch_for_events(events)

    def update(self) -> None:
        if self.current_state:
            self.current_state.update()

    def draw(self) -> None:
        self.screen.fill("black")
        for state in self.stack_state:
            state.draw()
        self.window.flip()

    def push_state(self, state: State) -> None:
        self.stack_state.append(state)

    def pop_state(self) -> None:
        if len(self.stack_state) > 1:
            self.stack_state.pop()

    def replace_state(self, state: State) -> None:
        self.stack_state = [state]

    def start_new_game(self) -> None:
        playstate = PlayState(self)
        self.replace_state(playstate)

    @property
    def current_state(self) -> State | None:
        return self.stack_state[-1] if self.stack_state else None


def main():
    game = Game()
    game.run()

if __name__ == "__main__":
    main()