from typing import List

import config as cfg
import pygame

from scenes.state import State


class DrawState(State):
    def __init__(self, game):
        super().__init__(game)
        
    def watch_for_events(self, events:List[pygame.event.Event]) -> None:
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    pygame.event.post(pygame.event.Event(self.game.EVENTS["START"]))     # §\label{srcDrawState0701}§
                elif event.key == pygame.K_n:
                    self.game.running = False
    
    def update(self, **kwargs):
        pass

    def draw(self):
        self.game.draw_message(cfg.MSGSTRINGS["draw"])

