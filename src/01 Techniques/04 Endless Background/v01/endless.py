from time import time
from typing import Any

import pygame

import config as cfg


class EndlessBackground(pygame.sprite.Sprite):
    def __init__(self, player:pygame.sprite.Sprite, bgimage: pygame.sprite.Sprite) -> None:
        super().__init__()
        self.player = player
        self.bgimage = bgimage
        self.offset = pygame.Vector2(0, 0) 
        self.image = pygame.Surface(cfg.WINDOW.size)
        self.rect = self.image.get_frect()

    def update(self, *args: Any, **kwargs: Any) -> None:
        super().update(args, kwargs)
        if "action" in kwargs.keys():
            if kwargs["action"] == "toggle_frame":
                self.bgimage.update(action="toggle_frame")
            elif kwargs["action"] == "scroll":
                self.scroll()
                position = cfg.world2camera(self.bgimage.rect, self.offset)
                self.image.fill("Grey")
                self.image.blit(self.bgimage.image, position)
    
    def save(self, filename: str) -> None:
        pygame.image.save(self.image, filename)

    def scroll(self) -> None:
        if self.player:
            self.offset.x = self.player.rect.centerx - self.rect.width / 2
        self.rect.topleft = self.offset


class Player(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        width = 80
        self.images = {
            "stop": pygame.Surface((width, width), pygame.SRCALPHA),
            "left": pygame.Surface((width, width), pygame.SRCALPHA),
            "right": pygame.Surface((width, width), pygame.SRCALPHA),
        }
        self.image = self.images["stop"]
        self.rect = self.image.get_frect()
        self.rect.center = cfg.WINDOW.center
        w, w2, w4 = width, width // 2, width // 4
        pygame.draw.circle(self.image, "Red", (w2, w2), w4)
        self.images["left"].blit(self.images["stop"], (0, 0))
        pygame.draw.polygon(self.images["left"], "Red", [(w2, w4), (0, w2), (w2, w - w4)])
        self.images["right"].blit(self.images["stop"], (0, 0))
        pygame.draw.polygon(self.images["right"], "Red", [(w2, w4), (w, w2), (w2, w - w4)])
        self.speed = pygame.Vector2(0, 0)

    def update(self, *args: any, **kwargs: any) -> None:
        super().update(*args, **kwargs)
        if "move" in kwargs.keys():
            if kwargs["move"] == "left":
                self.speed.x = -200
            elif kwargs["move"] == "right":
                self.speed.x = 200
            else :
                self.speed = pygame.Vector2(0, 0)
            self.image = self.images[kwargs["move"]]
        self.rect.move_ip(self.speed * cfg.DELTATIME)


class Landscape(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        self.image = pygame.image.load(cfg.get_image("backgroundtile.png")).convert()
        self.rect = self.image.get_rect()
        self.frame = True
        pygame.draw.rect(self.image, "Blue", self.rect, 2)

    def update(self, *args: Any, **kwargs: Any) -> None:
        super().update(args, kwargs)
        if action := kwargs.get("action", None):
            if action == "toggle_frame":
                self.toggle_frame()

    def toggle_frame(self) -> None:
        self.image = pygame.image.load(cfg.get_image("backgroundtile.png")).convert()
        self.frame = not self.frame
        if self.frame:
            pygame.draw.rect(self.image, "Blue", self.rect, 2)

    
class Game:

    def __init__(self) -> None:
        pygame.init()
        self.window = pygame.Window(size=cfg.WINDOW.size)
        self.window.position = pygame.WINDOWPOS_CENTERED
        self.screen : pygame.Surface = self.window.get_surface()
        self.player = Player()
        self.landscape = Landscape()
        self.bg = EndlessBackground(self.player, self.landscape)
        self.clock = pygame.time.Clock()
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
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_LEFT:
                    self.player.update(move="left")
                elif event.key == pygame.K_RIGHT:
                    self.player.update(move="right")
                elif event.key == pygame.K_s:
                    self.save()
                elif event.key == pygame.K_f:
                    self.bg.update(action="toggle_frame")
            elif event.type == pygame.KEYUP:
                if event.key in (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN):
                    self.player.update(move="stop")

    def update(self) -> None:
        self.player.update()
        self.bg.update(action="scroll")

    def draw(self) -> None:
        cx, cy = int(self.player.rect.center[0]), int(self.player.rect.center[1])
        self.window.title= f"Endless Background - Player: ({cx}, {cy})"
        self.screen.fill("White")
        self.screen.blit(self.bg.image, (0, 0))
        self.screen.blit(self.player.image, cfg.world2camera(self.player.rect, self.bg.offset))
        self.window.flip()

    def save(self):
        pygame.image.save(self.window.get_surface(), "screenshot.png")
        self.bg.save("bg_image.png")



   
def main() -> None:
    game = Game()
    game.run()

if __name__ == "__main__":
    main()
