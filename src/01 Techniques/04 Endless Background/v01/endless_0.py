from time import time
from typing import Any

import pygame

import config as cfg


class EndlessBackground(pygame.sprite.Sprite):

    def __init__(self, player:pygame.sprite.Sprite, bgimage: pygame.sprite.Sprite) -> None:
        super().__init__()
        self.player = player
        self.offset = pygame.Vector2(0, 0) 
        self.bgimage = bgimage
        self.image = pygame.Surface(cfg.WINDOW.size)
        self.rect = self.image.get_frect()
        self.clock = pygame.time.Clock()

    def update(self, *args: Any, **kwargs: Any) -> None:
        super().update(args, kwargs)
        w = self.camera2world(cfg.WINDOW)
        pos = self.world2camera(self.bgimage.rect)
        pos.left = pos.left % self.bgimage.rect.width
        pos.top = pos.top % self.bgimage.rect.height
        # Hauptbild
        self.image.blit(self.bgimage.image, pos)
        # Links
        if pos.left > 0:
            pos_left = pos.copy()
            pos_left.right = pos.left
            self.image.blit(self.bgimage.image, pos_left)
        # Oben
        if pos.top > 0:
            pos_top = pos.copy()
            pos_top.bottom = pos.top
            self.image.blit(self.bgimage.image, pos_top)
        # Rechts
        if pos.right < self.image.get_width():
            pos_right = pos.copy()
            pos_right.left = pos.right
            self.image.blit(self.bgimage.image, pos_right)
        # Unten
        if pos.bottom < self.image.get_height():
            pos_bottom = pos.copy()
            pos_bottom.top = pos.bottom
            self.image.blit(self.bgimage.image, pos_bottom)
        # Oben-Links
        if pos.left > 0 and pos.top > 0:
            pos_topleft = pos.copy()
            pos_topleft.right = pos.left
            pos_topleft.bottom = pos.top
            self.image.blit(self.bgimage.image, pos_topleft)
        # Oben-Rechts
        if pos.right < self.image.get_width() and pos.top > 0:
            pos_topright = pos.copy()
            pos_topright.left = pos.right
            pos_topright.bottom = pos.top
            self.image.blit(self.bgimage.image, pos_topright)
        # Unten-Links
        if pos.left > 0 and pos.bottom < self.image.get_height():
            pos_bottomleft = pos.copy()
            pos_bottomleft.right = pos.left
            pos_bottomleft.top = pos.bottom
            self.image.blit(self.bgimage.image, pos_bottomleft)
        # Unten-Rechts
        if pos.right < self.image.get_width() and pos.bottom < self.image.get_height():
            pos_bottomright = pos.copy()
            pos_bottomright.left = pos.right
            pos_bottomright.top = pos.bottom
            self.image.blit(self.bgimage.image, pos_bottomright)
        #self.window.flip()
    
    def save(self):
        pygame.image.save(self.image, "centered_image.png")

    def scroll(self) -> None:
        if self.player:
            self.offset.x = self.player.rect.centerx - self.rect.width / 2
            self.offset.y = self.player.rect.centery - self.rect.height / 2
        self.rect.topleft = self.offset

    def world2camera(self, rect: pygame.FRect|pygame.Rect|None) -> pygame.FRect:
        if rect is None:
            return pygame.FRect((0, 0), (0, 0))
        return pygame.FRect(rect.topleft - self.offset, rect.size)

    def camera2world(self, rect: pygame.FRect|pygame.Rect|None) -> pygame.FRect:
        if rect is None:
            return pygame.FRect((0, 0), (0, 0))
        return pygame.FRect(rect.topleft + self.offset, rect.size)


class Player(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        width = 80
        self.images = {
            "stop": pygame.Surface((width, width), pygame.SRCALPHA),
            "left": pygame.Surface((width, width), pygame.SRCALPHA),
            "right": pygame.Surface((width, width), pygame.SRCALPHA),
            "top": pygame.Surface((width, width), pygame.SRCALPHA),
            "bottom": pygame.Surface((width, width), pygame.SRCALPHA)
        }
        self.image = self.images["stop"]
        self.rect = self.image.get_frect()
        self.rect.center = cfg.WINDOW.center
        pygame.draw.circle(self.image, "Red", (width // 2, width // 2), width // 4)
        self.images["left"].blit(self.images["stop"], (0, 0))
        pygame.draw.polygon(self.images["left"], "Red", [(width // 2, width // 4), (0, width // 2), (width // 2, width - width // 4)])
        self.images["right"].blit(self.images["stop"], (0, 0))
        pygame.draw.polygon(self.images["right"], "Red", [(width // 2, width // 4), (width, width // 2), (width // 2, width - width // 4)])
        self.images["top"].blit(self.images["stop"], (0, 0))
        pygame.draw.polygon(self.images["top"], "Red", [(width // 2, 0), (width//4  , width // 2), (width - width // 4, width // 2)])
        self.images["bottom"].blit(self.images["stop"], (0, 0))
        pygame.draw.polygon(self.images["bottom"], "Red", [(width // 2, width), (width//4  , width // 2), (width - width // 4, width // 2)])
        self.speed = pygame.Vector2(0, 0)

    def update(self, *args: any, **kwargs: any) -> None:
        super().update(*args, **kwargs)
        if "move" in kwargs.keys():
            if kwargs["move"] == "left":
                self.speed.x = -200
            elif kwargs["move"] == "right":
                self.speed.x = 200
            elif kwargs["move"] == "top":
                self.speed.y = -200
            elif kwargs["move"] == "bottom":
                self.speed.y = 200
            elif kwargs["move"] == "stop":
                self.speed = pygame.Vector2(0, 0)
            self.image = self.images[kwargs["move"]]
        self.rect.move_ip(self.speed * cfg.DELTATIME)


class Landscape(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        self.image = pygame.image.load(cfg.get_image("backgroundtile.png")).convert()
        self.rect = self.image.get_rect()
        pygame.draw.rect(self.image, "Blue", self.image.get_rect(), 2)




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
            elif event.type == pygame.WINDOWCLOSE:
                self.running = False
                event.window.destroy()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_LEFT:
                    self.player.update(move="left")
                elif event.key == pygame.K_RIGHT:
                    self.player.update(move="right")
                elif event.key == pygame.K_UP:
                    self.player.update(move="top")  
                elif event.key == pygame.K_DOWN:
                    self.player.update(move="bottom")
                elif event.key == pygame.K_s:
                    self.save()

            elif event.type == pygame.KEYUP:
                if event.key in (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN):
                    self.player.update(move="stop")

    def update(self) -> None:
        self.player.update()
        self.bg.scroll()
        self.bg.update()

    def draw(self) -> None:
        self.screen.blit(self.bg.image, (0, 0))
        self.screen.blit(self.player.image, self.bg.world2camera(self.player.rect))
        self.window.flip()

    def save(self):
        self.window.save()

   
def main() -> None:
    game = Game()
    game.run()

if __name__ == "__main__":
    main()
