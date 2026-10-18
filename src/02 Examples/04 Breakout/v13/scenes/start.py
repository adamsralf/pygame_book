import pygame

import config as cfg
from scenes.state import State


class StartState(State):
    def __init__(self, game):
        super().__init__(game, "start.ogg")

    def watch_for_events(self, events: list[pygame.event.Event]) -> None:
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pygame.event.post(pygame.event.Event(self.game.events["PLAY"]))

    def update(self) -> None:
        pass

    def draw(self) -> None:
        self.draw_message(cfg.MSGSTRINGS["start"])
