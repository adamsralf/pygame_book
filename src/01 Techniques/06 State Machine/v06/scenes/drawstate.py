import pygame

import config as cfg
from scenes.state import State


class DrawState(State):
    def __init__(self, game):
        super().__init__(game)
        
    def watch_for_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_q):
                    self.game.running = False
                elif event.key == pygame.K_y:
                    from scenes.startstate import StartState
                    self.game.reset()
                    self.game.state = StartState(self.game)
                elif event.key == pygame.K_n:
                    self.game.running = False
    
    def update(self, **kwargs):
        pass

    def draw(self):
        self.game.draw_message(cfg.MSGSTRINGS["draw"])

