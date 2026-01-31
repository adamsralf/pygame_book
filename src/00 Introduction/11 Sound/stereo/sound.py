import os
from time import time
from typing import Any

import pygame
from pygame.constants import (K_DOWN, K_ESCAPE, K_LEFT, K_RIGHT, K_SPACE, K_UP,
                              KEYDOWN, QUIT)

import config as cfg


class Ground(pygame.sprite.Sprite):

    def __init__(self) -> None:
        super().__init__()
        fullfilename = cfg.get_image("tankbrigade_part64.png")
        tile = pygame.image.load(fullfilename).convert()
        rect = tile.get_rect()
        self.image = pygame.Surface(cfg.WINDOW.size)
        for row in range(cfg.WINDOW.width // rect.width):
            for col in range(cfg.WINDOW.height // rect.height):
                self.image.blit(tile, (row * rect.width, col * rect.height))
        self.rect = self.image.get_rect()


class Tank(pygame.sprite.Sprite):

    def __init__(self) -> None:
        super().__init__()
        self.image_filename = (209, 190, 202, 214, 226, 238, 250, 262)
        self.images: dict[str, list[pygame.surface.Surface]] = {"up": [], "down": [], "left": [], "right": []}
        for number in self.image_filename:
            fullfilename = cfg.get_image(f"tankbrigade_part{number}.png")
            picture = pygame.image.load(fullfilename).convert()
            picture.set_colorkey("black")
            self.images["up"].append(picture)
            self.images["down"].append(pygame.transform.rotate(picture, 180))
            self.images["left"].append(pygame.transform.rotate(picture, +90))
            self.images["right"].append(pygame.transform.rotate(picture, -90))
        self.direction = "right"
        self.imageindex = 0
        self.image = self.images[self.direction][self.imageindex]
        self.rect = pygame.rect.FRect(self.image.get_rect())
        self.rect.left, self.rect.top = 3 * self.rect.width, 2 * self.rect.height
        self.sound_drive = pygame.mixer.Sound(cfg.get_sound("tank_drive1.wav"))  # §\label{srcSound0201}§
        self.channel = pygame.mixer.find_channel()  # Find a free sound channel§\label{srcSound0204}§
        if self.channel:
            self.stereo()                           # §\label{srcSound0202}§
            self.channel.play(self.sound_drive, -1) # §\label{srcSound0203}§
        self.speed = 50

    def update(self, *args: Any, **kwargs: Any) -> None:
        if "go" in kwargs.keys():
            if kwargs["go"]:
                self.update_imageindex()
                self.image = self.images[self.direction][self.imageindex]
                if self.direction == "up" or self.direction == "left":
                    self.speed = -50
                elif self.direction == "down" or self.direction == "right":
                    self.speed = 50
                if self.direction == "up" or self.direction == "down":
                    self.rect.move_ip(0, self.speed * cfg.DELTATIME)
                    if self.rect.top <= cfg.WINDOW.top:
                        self.turn("down")
                    if self.rect.bottom >= cfg.WINDOW.bottom:
                        self.turn("up")
                elif self.direction == "left" or self.direction == "right":
                    self.rect.move_ip(self.speed * cfg.DELTATIME, 0)
                    if self.rect.left <= cfg.WINDOW.left:
                        self.turn("right")
                    if self.rect.right >= cfg.WINDOW.right:
                        self.turn("left")
                self.stereo()
        if "turn" in kwargs.keys():
            self.turn(kwargs["turn"])

    def stereo(self) -> None:
        volume_right = self.rect.centerx / cfg.WINDOW.width  # §\label{srcSound0205}§
        volume_left = 1 - volume_right
        self.channel.set_volume(volume_left, volume_right)

    def turn(self, direction: str) -> None:
        self.direction = direction

    def update_imageindex(self) -> None:
        if self.speed == 0:
            self.imageindex = 0
        else:
            self.imageindex = (self.imageindex + 1) % len(self.images[self.direction])


class Bullet(pygame.sprite.Sprite):

    SOUND_FIRE = None                               # Only one shared sound is needed§\label{srcSound0206}§

    def __init__(self, tank: Tank) -> None:
        super().__init__()
        bulletspeed = 300
        number: dict[str, int] = {"left": 49, "right": 61, "up": 37, "down": 73}
        directions = {
            "left": pygame.Vector2(-bulletspeed, 0),
            "right": pygame.Vector2(bulletspeed, 0),
            "up": pygame.Vector2(0, -bulletspeed),
            "down": pygame.Vector2(0, bulletspeed),
        }
        fullfilename = os.path.join(cfg.PATH["image"], f"tankbrigade_part{number[tank.direction]}.png")
        self.image = pygame.image.load(fullfilename).convert()
        self.image.set_colorkey("black")
        self.rect = self.image.get_rect()
        self.direction = tank.direction
        self.rect.center = tank.rect.center
        self.speed = directions[tank.direction]

        if Bullet.SOUND_FIRE == None:               # §\label{srcSound0207}§
            Bullet.SOUND_FIRE = pygame.mixer.Sound(cfg.get_sound("tank_fire1.wav"))
        volume_right = self.rect.centerx / cfg.WINDOW.width
        volume_left = 1 - volume_right
        self.channel: pygame.mixer.Channel = pygame.mixer.find_channel()
        if self.channel:
            self.channel.set_volume(volume_left, volume_right)
            self.channel.play(Bullet.SOUND_FIRE)

    def update(self, *args: Any, **kwargs: Any) -> None:
        self.rect.move_ip(self.speed * cfg.DELTATIME)
        if not cfg.WINDOW.contains(self.rect):
            self.kill()


class Game:

    def __init__(self) -> None:
        pygame.init()
        self.window = pygame.Window(size=cfg.WINDOW.size, title="Steroe Panning Sound Example")
        self.screen = self.window.get_surface()
        self.clock = pygame.time.Clock()

        self.ground = pygame.sprite.GroupSingle(Ground())
        self.tankreference = Tank()
        self.tank = pygame.sprite.GroupSingle(self.tankreference)
        self.all_bullets = pygame.sprite.Group()
        self.running = True

    def watch_for_events(self) -> None:
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.running = False
                elif event.key == K_UP:
                    self.tank.update(turn="up")
                elif event.key == K_DOWN:
                    self.tank.update(turn="down")
                elif event.key == K_LEFT:
                    self.tank.update(turn="left")
                elif event.key == K_RIGHT:
                    self.tank.update(turn="right")
                elif event.key == K_SPACE:
                    self.fire()

    def fire(self) -> None:
        if len(self.all_bullets) < 5:
            self.all_bullets.add(Bullet(self.tankreference))

    def draw(self) -> None:
        self.ground.draw(self.screen)
        self.tank.draw(self.screen)
        self.all_bullets.draw(self.screen)
        self.window.flip()

    def update(self) -> None:
        self.tank.update(go=True)
        self.all_bullets.update()

    def run(self) -> None:
        time_previous = time()
        self.running = True
        while self.running:
            self.watch_for_events()
            self.update()
            self.draw()
            self.clock.tick(cfg.FPS)
            time_current = time()
            cfg.DELTATIME = time_current - time_previous
            time_previous = time_current
        pygame.quit()


def main():
    Game().run()


if __name__ == "__main__":
    main()
