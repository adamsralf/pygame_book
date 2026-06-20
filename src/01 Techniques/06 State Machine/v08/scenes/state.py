from abc import ABC, abstractmethod
from pygame import event
from typing import List

class State(ABC):
    def __init__(self, game):
        self.game = game

    @abstractmethod
    def watch_for_events(self, events:List[event.Event]) -> None:
        pass

    @abstractmethod
    def update(self, **kwargs):
        pass

    @abstractmethod
    def draw(self):
        pass


