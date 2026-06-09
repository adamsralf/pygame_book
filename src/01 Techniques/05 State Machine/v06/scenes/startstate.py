import config as cfg
import pygame

from scenes.state import State


class StartState(State):
    def __init__(self, game):
        super().__init__(game)
        self.game.reset()
        
    def watch_for_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_q):
                    self.game.running = False
                elif event.key == pygame.K_SPACE:
                    from scenes.playstate import PlayState  # to avoid circular imports
                    self.game.state = PlayState(self.game)  # §\label{srcStartState0601}§
    
    def update(self, **kwargs):
        pass

    def draw(self):
        self.game.draw_message(cfg.MSGSTRINGS["start"])
