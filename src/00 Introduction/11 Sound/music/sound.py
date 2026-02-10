from typing import Any

import config as cfg
import pygame
from pygame.constants import K_ESCAPE, KEYDOWN, KEYUP, QUIT, K_f, K_j, K_p


class Game:
    def __init__(self) -> None:
        pygame.init()                               # Includes mixer §\label{srcSound0002}§
        self.window = pygame.Window(size=cfg.WINDOW.size, title='Sound Background Music')  
        self.screen = self.window.get_surface()
        self.clock = pygame.time.Clock()
        self.font_bigsize = pygame.font.Font(pygame.font.get_default_font(), 40)
        self.running = True
        self.pause = False
        self.sounds()

    def sounds(self) -> None:
        pygame.mixer.music.load(cfg.get_sound("Lucifer.mid"))
        pygame.mixer.music.set_volume(0.1)          # §\label{srcSound0004}§
        pygame.mixer.music.play(-1, 0.0)            # Endles loop§\label{srcSound0005}§

    def watch_for_events(self) -> None:
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.running = False
            elif event.type == KEYUP:
                if event.key == K_f:
                    self.music_start_stop(fadeout=5000)
                elif event.key == K_j:
                    self.music_start_stop(loop=-1)
                elif event.key == K_p:
                    self.pause_alter()
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 4:  # up
                    self.volume_alter(cfg.VOLUME_STEP)
                elif event.button == 5:  # down
                    self.volume_alter(-cfg.VOLUME_STEP)


    def music_start_stop(self, **kwargs: Any) -> None:
        if "fadeout" in kwargs.keys():
            pygame.mixer.music.fadeout(kwargs["fadeout"])   # §\label{srcSound0006}§
        if "loop" in kwargs.keys():
            pygame.mixer.music.play(kwargs["loop"], 0.0)    # §\label{srcSound0007}§

    def pause_alter(self) -> None:
        if self.pause:
            pygame.mixer.music.unpause()                    # §\label{srcSound0008}§
        else:
            pygame.mixer.music.pause()
        self.pause = not self.pause                         # §\label{srcSound0009}§

    def volume_alter(self, delta: float) -> None:
        volume = pygame.mixer.music.get_volume()
        volume += delta
        volume = pygame.math.clamp(volume, 0.0, 1.0)
        pygame.mixer.music.set_volume(volume)               # §\label{srcSound0010}§

    def draw(self) -> None:
        self.screen.fill("white")
        volume = pygame.mixer.music.get_volume()
        volume_surface = self.font_bigsize.render(f"Volume: {volume:3.2f}", True, "red")
        volume_rect = volume_surface.get_rect()
        volume_rect.center = cfg.WINDOW.center
        self.screen.blit(volume_surface, volume_rect)

        self.window.flip()

    def update(self):
        pass

    def run(self):
        self.running = True
        while self.running:
            self.watch_for_events()
            self.update()
            self.draw()
            self.clock.tick(cfg.FPS)
        pygame.quit()


def main():
    Game().run()


if __name__ == "__main__":
    main()
