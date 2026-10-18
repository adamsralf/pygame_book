from abc import ABC, abstractmethod

import pygame

import config as cfg


class State(ABC):
    def __init__(self, game, melody):
        self.game = game
        self.fonts = {
            "title": pygame.font.SysFont("arial", 52, bold=True),
            "text": pygame.font.SysFont("arial", 24),
        }
        self.melody = melody

    @abstractmethod
    def watch_for_events(self, events: list[pygame.event.Event]) -> None:
        pass

    @abstractmethod
    def update(self) -> None:
        pass

    @abstractmethod
    def draw(self) -> None:
        pass

    def draw_message(self, message: cfg.Message) -> None:
        surface = pygame.Surface(cfg.WINDOW.size, pygame.SRCALPHA)
        surface.fill((0, 0, 0, 190))
        headline = self.fonts["title"].render(message["headline"], True, "gold")
        headline_rect = headline.get_rect(center=(cfg.WINDOW.centerx, cfg.WINDOW.centery - 150))
        surface.blit(headline, headline_rect)

        line_height = self.fonts["text"].get_linesize()
        top = headline_rect.bottom + 35
        for line in message["message"]:
            if line:
                text = self.fonts["text"].render(line, True, "white")
                text_rect = text.get_rect(centerx=cfg.WINDOW.centerx, top=top)
                surface.blit(text, text_rect)
            top += line_height + 8
        self.game.screen.blit(surface, (0, 0))