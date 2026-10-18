import pygame

import config as cfg
from scenes.state import State


class GameOverState(State):
    def watch_for_events(self, events: list[pygame.event.Event]) -> None:
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    pygame.event.post(pygame.event.Event(self.game.events["NEW_GAME"]))
                elif event.key == pygame.K_n:
                    self.game.running = False

    def update(self) -> None:
        pass

    def draw(self) -> None:
        self.draw_message(cfg.MSGSTRINGS["gameover"])
