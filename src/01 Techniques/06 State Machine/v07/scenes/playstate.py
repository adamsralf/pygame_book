from typing import List

import config as cfg
import pygame

from scenes.state import State


class PlayState(State):
    def __init__(self, game):
        super().__init__(game)
        
    def watch_for_events(self, events:List[pygame.event.Event]) -> None:
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.update(action="place", pos=event.pos)
    
    def update(self, **kwargs):
        if kwargs.get("action") == "place":
            pos = kwargs.get("pos")
            if cfg.PLAYGROUND.collidepoint(pos):
                row = (pos[1] - cfg.PLAYGROUND.top) // cfg.CELL_SIZE
                col = (pos[0] - cfg.PLAYGROUND.left) // cfg.CELL_SIZE
                if self.game.BOARD[row][col] is None:
                    self.game.BOARD[row][col] = self.game.PLAYER
                    if self.check_winning():  
                        pygame.event.post( pygame.event.Event(self.game.EVENTS["WIN"]))   # §\label{srcPlayState0701}§
                        return
                    else:
                        self.change_player()
            if self.check_ending():
                pygame.event.post(pygame.event.Event(self.game.EVENTS["DRAW"]))          # §\label{srcPlayState0702}§
                return

    def draw(self):
        self.game.screen.fill(cfg.COLORS["PLAYGROUND"], cfg.PLAYGROUND)
        for i in range(1, 3):
            pygame.draw.line(self.game.screen, cfg.COLORS["GRID"], (cfg.PLAYGROUND.left + i*cfg.CELL_SIZE, cfg.PLAYGROUND.top), (cfg.PLAYGROUND.left + i*cfg.CELL_SIZE, cfg.PLAYGROUND.bottom), 2)
            pygame.draw.line(self.game.screen, cfg.COLORS["GRID"], (cfg.PLAYGROUND.left, cfg.PLAYGROUND.top + i*cfg.CELL_SIZE), (cfg.PLAYGROUND.right, cfg.PLAYGROUND.top + i*cfg.CELL_SIZE), 2)
        player = self.game.FONTS["text"].render(f"Player {self.game.PLAYER}'s turn", True, cfg.COLORS[self.game.PLAYER])
        rect = player.get_rect()
        rect.centerx = cfg.PLAYGROUND.centerx
        rect.bottom  = cfg.WINDOW.bottom - 10
        for y in range(3):
            for x in range(3):
                cell = self.game.BOARD[y][x]
                if cell is not None:
                    symbol = self.game.SYMBOLS[cell]
                    symbol_rect = symbol.get_rect()
                    symbol_rect.center = (cfg.PLAYGROUND.left + (x + 0.5) * cfg.CELL_SIZE, cfg.PLAYGROUND.top + (y + 0.5) * cfg.CELL_SIZE)
                    self.game.screen.blit(symbol, symbol_rect)
        self.game.screen.blit(player, rect)

    def check_winning(self) -> bool:
        for i in range(3):
            # rows
            if self.game.BOARD[i][0] == self.game.BOARD[i][1] == self.game.BOARD[i][2] is not None:
                return True
            # cols
            if self.game.BOARD[0][i] == self.game.BOARD[1][i] == self.game.BOARD[2][i] is not None:
                return True
        # diagonal
        if self.game.BOARD[0][0] == self.game.BOARD[1][1] == self.game.BOARD[2][2] is not None:
            return True
        # anti-diagonal
        if self.game.BOARD[0][2] == self.game.BOARD[1][1] == self.game.BOARD[2][0] is not None:
            return True
        return False

    def change_player(self) -> None:
        self.game.PLAYER = "O" if self.game.PLAYER == "X" else "X"

    def check_ending(self) -> bool:
        for row in self.game.BOARD:
            for cell in row:
                if cell is None:
                    return False
        return True
