from abc import ABC, abstractmethod


class State(ABC):
    def __init__(self, game):
        self.game = game

    @abstractmethod
    def watch_for_events(self):
        pass

    @abstractmethod
    def update(self, **kwargs):
        pass

    @abstractmethod
    def draw(self):
        pass


