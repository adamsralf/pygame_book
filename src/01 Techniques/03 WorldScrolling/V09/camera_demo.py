from time import time

import config as cfg
import pygame
from objects import Mob, Player, Tile
from windows import (WindowAuto, WindowBirdEyeView, WindowCenteredCamera,
                     WindowPagewise, WindowPlain)


class Game:

    def __init__(self) -> None:
        pygame.init()
        self.clock = pygame.time.Clock()
        self.create_tiles()
        self.create_mobs()
        self.window_plain = WindowPlain(self.tiles, self.mobs)
        self.window_birdeye = WindowBirdEyeView(self.tiles, self.mobs)
        self.player = Player(cfg.WORLD.center)
        self.mobs.add(self.player)
        self.window_centered = WindowCenteredCamera(self.player, self.tiles, self.mobs)
        self.window_pagewise = WindowPagewise(self.player, self.tiles, self.mobs, 3)
        self.window_auto = WindowAuto(self.player, self.tiles, self.mobs, (50,10))
        self.running = True

    def run(self) -> None:
        time_previous = time()
        while self.running:
            self.watch_for_events()
            if self.running:
                self.update()
                self.draw()
                self.clock.tick(cfg.FPS)
                time_current = time()
                cfg.DELTATIME = time_current - time_previous
                time_previous = time_current
        pygame.quit()

    def watch_for_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.WINDOWCLOSE:
                self.running = False
                event.window.destroy()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_UP:
                    self.player.update(move="up")
                elif event.key == pygame.K_DOWN:
                    self.player.update(move="down")
                elif event.key == pygame.K_LEFT:
                    self.player.update(move="left")
                elif event.key == pygame.K_RIGHT:
                    self.player.update(move="right")
                elif event.key == pygame.K_s:
                    self.save()

            elif event.type == pygame.KEYUP:
                if event.key in (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT):
                    self.player.update(move="stop")

    def update(self) -> None:
        self.player.update()
        self.mobs.update()
        self.window_centered.scroll()
        self.window_pagewise.scroll()
        self.window_auto.scroll()

    def draw(self) -> None:
        self.window_plain.draw()
        self.window_plain.window.title = f"Plain Window (size={self.window_plain.rect.size}, fps={self.clock.get_fps():.0f})"

        self.window_pagewise.draw()
        xy = int(self.window_pagewise.offset.x), int(self.window_pagewise.offset.y)
        self.window_pagewise.window.title = f"Pagewise Window (offset={xy})"

        self.window_centered.draw()
        self.window_centered.window.title = f"Centered Window (offset={self.window_centered.offset})"

        self.window_auto.window.title = f"Auto Window (offset={self.window_auto.offset})"
        self.window_auto.draw()

        inner = self.window_pagewise.camera2world(self.window_pagewise.inner_rect)
        auto = self.window_auto.camera2world(self.window_auto.rect)
        self.window_birdeye.draw([{"rect":self.window_plain.rect, "color":"blue"},
                                  {"rect":self.window_pagewise.rect, "color":"red"},
                                  {"rect":inner, "color":"brown"},
                                  {"rect":auto, "color":"pink"},
                                  {"rect":self.window_centered.rect, "color":"green"}] )

    def create_tiles(self) -> None:
        self.tiles = pygame.sprite.Group()
        for row in range(cfg.NOF_ROWS):
            for col in range(cfg.NOF_COLS):
                x = col * cfg.TILESIZE_WORLD.x
                y = row * cfg.TILESIZE_WORLD.y
                self.tiles.add(Tile((x, y)))

    def create_mobs(self) -> None:
        self.mobs = pygame.sprite.Group()
        for _ in range(cfg.NOF_MOBS):
            self.mobs.add(Mob())

    def save(self):
        self.window_plain.save()
        self.window_birdeye.save()
        self.window_centered.save()
        self.window_pagewise.save() 
        self.window_auto.save() 

   
def main() -> None:
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
    game.run()


if __name__ == "__main__":
    main()
