import pygame

import config as cfg
from scenes.state import State


class HelpState(State):
    def __init__(self, game):
        super().__init__(game, "help.ogg")

    def watch_for_events(self, events: list[pygame.event.Event]) -> None:
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_h:
                pygame.event.post(pygame.event.Event(self.game.events["UNHELP"]))

    def update(self) -> None:
        pass

    def draw(self) -> None:
        self.draw_message(cfg.MSGSTRINGS["help"])
