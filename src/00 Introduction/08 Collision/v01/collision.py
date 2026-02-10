from typing import Any

import config as cfg
import pygame


class Obstacle(pygame.sprite.Sprite):

    def __init__(self, filename1: str, filename2: str) -> None:
        super().__init__()
        self.image_normal = pygame.image.load(cfg.imagepath(filename1)).convert_alpha()
        self.image_hit = pygame.image.load(cfg.imagepath(filename2)).convert_alpha()
        self.image = self.image_normal
        self.rect: pygame.Rect = self.image.get_rect()      # Bounding rectangle§\label{srcCollision01}§
        self.mask = pygame.mask.from_surface(self.image)    # Pixel mask§\label{srcCollision02}§
        self.radius = self.rect.width // 2                  # Bounding circle§\label{srcCollision03}§
        self.rect.centery = cfg.WINDOW.centery
        self.hit = False

    def update(self, *args: Any, **kwargs: Any) -> None:
        if "hit" in kwargs.keys():
            self.hit = kwargs["hit"]
        self.image = self.image_hit if (self.hit) else self.image_normal


class Bullet(pygame.sprite.Sprite):

    def __init__(self, picturefile: str) -> None:
        super().__init__()
        self.image = pygame.image.load(cfg.imagepath(picturefile)).convert_alpha()
        self.rect = self.image.get_rect()
        self.radius = self.rect.centery
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.center = (10, 10)
        self.directions = {"stop": (0, 0), "down": (0, 1), "up": (0, -1), 
                           "left": (-1, 0), "right": (1, 0)}
        self.set_direction("stop")

    def update(self, *args: Any, **kwargs: Any) -> None:
        if "action" in kwargs.keys():
            if kwargs["action"] == "move":
                self.rect.move_ip(self.speed)
        elif "direction" in kwargs.keys():
            self.set_direction(kwargs["direction"])

    def set_direction(self, direction: str) -> None:
        self.speed = self.directions[direction]


class Game(object):

    def __init__(self) -> None:
        pygame.init()
        self.window = pygame.Window(size=cfg.WINDOW.size, title=cfg.TITLE)
        self.screen = self.window.get_surface()
        self.clock = pygame.time.Clock()

        self.font = pygame.font.Font(pygame.font.get_default_font(), 24)
        self.bullet = pygame.sprite.GroupSingle(Bullet("shoot.png"))
        self.all_obstacles = pygame.sprite.Group()
        self.all_obstacles.add(Obstacle("brick1.png", "brick2.png"))
        self.all_obstacles.add(Obstacle("ship1.png", "ship2.png"))
        self.all_obstacles.add(Obstacle("alienbig1.png", "alienbig2.png"))
        self.running = False

    def run(self) -> None:
        self.resize()
        self.running = True
        while self.running:
            self.watch_for_events()
            self.update()
            self.draw()
            self.clock.tick(cfg.FPS)
        pygame.quit()

    def watch_for_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_DOWN:
                    self.bullet.sprite.update(direction="down")
                elif event.key == pygame.K_UP:
                    self.bullet.sprite.update(direction="up")
                elif event.key == pygame.K_LEFT:
                    self.bullet.sprite.update(direction="left")
                elif event.key == pygame.K_RIGHT:
                    self.bullet.sprite.update(direction="right")
                elif event.key == pygame.K_r:
                    cfg.MODE = "rect"
                elif event.key == pygame.K_c:
                    cfg.MODE = "circle"
                elif event.key == pygame.K_m:
                    cfg.MODE = "mask"
            elif event.type == pygame.KEYUP:
                self.bullet.sprite.update(direction="stop")

    def update(self) -> None:
        self.check_for_collision()
        self.bullet.update(action="move")
        self.all_obstacles.update()

    def draw(self) -> None:
        self.screen.fill("white")
        self.all_obstacles.draw(self.screen)
        self.bullet.draw(self.screen)
        text_surface_modus = self.font.render(f"Mode: {cfg.MODE}", True, "blue")
        self.screen.blit(text_surface_modus, dest=(10, cfg.WINDOW.bottom - 30))
        self.window.flip()

    def resize(self) -> None:
        total_width = 0
        for s in self.all_obstacles:
            total_width += s.rect.width
        padding = (cfg.WINDOW.width - total_width) // 4  # Spacing between obstacles§\label{srcCollision04}§
        for i in range(len(self.all_obstacles)):
            if i == 0:
                self.all_obstacles.sprites()[i].rect.left = padding
            else:
                self.all_obstacles.sprites()[i].rect.left = self.all_obstacles.sprites()[i - 1].rect.right + padding

    def check_for_collision(self) -> None:
        if cfg.MODE == "circle":
            for s in self.all_obstacles:
                s.update(hit=pygame.sprite.collide_circle(self.bullet.sprite, s))
        elif cfg.MODE == "mask":
            for s in self.all_obstacles:
                s.update(hit=pygame.sprite.collide_mask(self.bullet.sprite, s))
        else:
            for s in self.all_obstacles:
                s.update(hit=pygame.sprite.collide_rect(self.bullet.sprite, s))


def main():
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
