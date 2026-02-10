import config as cfg
import pygame
from pygame.constants import K_ESCAPE, KEYDOWN, QUIT


class Game:
    def __init__(self) -> None:
        pygame.init()
        self.window = pygame.Window(size=cfg.WINDOW.size, title='Sound Background Music')  
        self.screen = self.window.get_surface()
        self.clock = pygame.time.Clock()
        self.font_bigsize = pygame.font.Font(pygame.font.get_default_font(), 40)
        self.running = True
        self.pause = False
        self.sounds()

    def sounds(self) -> None:
        self.bubble = pygame.mixer.Sound(cfg.get_sound("plopp.mp3"))    # §\label{srcSound0101}§
        self.clash = pygame.mixer.Sound(cfg.get_sound("glas.wav"))      # §\label{srcSound0102}§

    def watch_for_events(self) -> None:
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.running = False
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:                       # left
                    self.bubble.play()                      # §\label{srcSound0103}§    
                elif event.button == 3:                     # right
                    self.clash.play()                       # §\label{srcSound0104}§
                elif event.button == 4:                     # up
                    self.volume_alter(0.05)
                elif event.button == 5:                     # down
                    self.volume_alter(-0.05)
       
    def volume_alter(self, delta: float) -> None:
        volume = self.bubble.get_volume()                   # For both§\label{srcSound0106}§
        volume += delta
        volume = pygame.math.clamp(volume, 0.0, 1.0)
        self.bubble.set_volume(volume)
        self.clash.set_volume(volume)

    def draw(self) -> None:
        self.screen.fill("black")
        volume = self.bubble.get_volume()                   # For both§\label{srcSound0105}§
        volume_surface = self.font_bigsize.render(f"Lautstärke: {volume:3.2f}", True, "red")
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
