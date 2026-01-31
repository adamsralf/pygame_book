from random import randint
from time import time
from typing import Any, Dict, Tuple

import config as cfg
import pygame


class BubbleContainer:
    def __init__(self, filename: str) -> None:
        imagename = cfg.get_image(filename)
        image: pygame.surface.Surface = pygame.image.load(imagename).convert_alpha()
        self.images = {i: pygame.transform.scale(image, (i * 2, i * 2)) for i in range(cfg.RADIUS["min"], cfg.RADIUS["max"] + 1)}

    def get(self, radius: int) -> pygame.surface.Surface:
        radius = max(cfg.RADIUS["min"], radius)
        radius = min(cfg.RADIUS["max"], radius)
        return self.images[radius]


class Timer:
    def __init__(self, duration: int, with_start: bool = True) -> None:
        self.duration = duration
        if with_start:
            self.next = pygame.time.get_ticks()
        else:
            self.next = pygame.time.get_ticks() + self.duration

    def is_next_stop_reached(self) -> bool:
        if pygame.time.get_ticks() > self.next:
            self.next = pygame.time.get_ticks() + self.duration
            return True
        return False


class Background(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        imagename = cfg.get_image("aquarium.png")
        self.image: pygame.surface.Surface = pygame.image.load(imagename).convert()
        self.image = pygame.transform.scale(self.image, cfg.WINDOW.size)
        self.rect = self.image.get_rect()


class Message(pygame.sprite.Sprite):
    def __init__(self, filename: str) -> None:      # §\label{srcBubble1202}§
        super().__init__()
        imagename = cfg.get_image(filename)
        self.image: pygame.surface.Surface = pygame.image.load(imagename).convert_alpha()
        self.rect = self.image.get_rect()


class Bubble(pygame.sprite.DirtySprite):
    def __init__(self, speed: int) -> None:
        super().__init__()
        self.mode = "blue"
        self.radius = cfg.RADIUS["min"]
        self.image = Game.BUBBLE_CONTAINER[self.mode].get(self.radius)
        self.rect: pygame.rect.Rect = self.image.get_rect()
        self.fradius = float(self.radius)
        self.speed = speed

    def update(self, *args: Any, **kwargs: Any) -> None:
        if "action" in kwargs.keys():
            if kwargs["action"] == "grow":
                self.fradius += self.speed * cfg.DELTATIME
                self.fradius = min(self.fradius, cfg.RADIUS["max"])
                self.radius = round(self.fradius)
                center = self.rect.center
                self.image = Game.BUBBLE_CONTAINER[self.mode].get(self.radius)
                self.rect = self.image.get_rect()
                self.rect.center = center
            elif kwargs["action"] == "sting":
                self.stung()
        elif "mode" in kwargs.keys():
            self.set_mode(kwargs["mode"])

    def set_mode(self, mode: str) -> None:
        if mode != self.mode:
            self.mode = mode
            self.image = Game.BUBBLE_CONTAINER[self.mode].get(self.radius)

    def randompos(self) -> None:
        bubbledistance = cfg.DISTANCE + cfg.RADIUS["min"]
        centerx = randint(cfg.PLAYGROUND.left + bubbledistance, cfg.PLAYGROUND.right - bubbledistance)
        centery = randint(cfg.PLAYGROUND.top + bubbledistance, cfg.PLAYGROUND.bottom - bubbledistance)
        self.rect.center = (centerx, centery)

    def stung(self):
        self.kill()
        cfg.POINTS += self.radius


class Points(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        self.font = pygame.font.Font(pygame.font.get_default_font(), 18)
        self.oldpoints = -1

    def update(self, *args: Any, **kwargs: Any) -> None:
        if self.oldpoints != cfg.POINTS:
            self.image = self.font.render(f"Points: {cfg.POINTS}", True, "red")
            self.rect = self.image.get_rect()
            self.rect.left = cfg.BOX.left
            self.rect.top = cfg.BOX.top


class Game:
    BUBBLE_CONTAINER: Dict[str, BubbleContainer] = {}

    def __init__(self) -> None:
        pygame.init()
        self.window = pygame.Window(size=cfg.WINDOW.size, title=cfg.CAPTION)
        self.screen = self.window.get_surface()
        self.clock = pygame.time.Clock()
        Game.BUBBLE_CONTAINER["blue"] = BubbleContainer("bubble1.png")
        Game.BUBBLE_CONTAINER["red"] = BubbleContainer("bubble2.png")
        self.background = pygame.sprite.GroupSingle(Background())
        self.all_sprites = pygame.sprite.Group()
        self.running = True
        self.pausing = False
        self.msg_pause = Message("pause.png")       # §\label{srcBubble1203}§
        self.msg_restart = Message("restart.png")
        self.restart()

    def watch_for_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_p:
                    self.setpause()
                elif event.key == pygame.K_j:       # §\label{srcBubble1205}§
                    self.do_start = True
                elif event.key == pygame.K_n:       # §\label{srcBubble1206}§
                    self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:               # left
                    self.sting(pygame.mouse.get_pos())
                elif event.button == 3:               # right
                    self.setpause()

    def draw(self) -> None:
        self.background.draw(self.screen)
        self.all_sprites.draw(self.screen)
        self.window.flip()

    def update(self) -> None:
        if self.do_start:                           # Restart?§\label{srcBubble1208}§
            self.restart()
        if not self.pausing and self.running:
            if self.check_bubblecollision():
                if not self.restarting:
                    self.all_sprites.add(self.msg_restart)
                    self.restarting = True
            else:
                self.all_sprites.update(action="grow")
                self.spawn_bubble()
            self.set_mousecursor()

    def restart(self):
        cfg.POINTS = 0
        self.all_sprites.empty()
        self.all_sprites.add(Points())
        self.bubble_speed = 10
        self.timer_bubble = Timer(500, False)
        self.timer_bubble_speed = Timer(10000, False)
        self.do_start = False
        self.restarting = False

    def setpause(self):
        if not self.pausing:
            self.all_sprites.add(self.msg_pause)
        else:
            self.msg_pause.kill()
        self.pausing = not self.pausing

    def spawn_bubble(self) -> None:
        if self.timer_bubble_speed.is_next_stop_reached():
            if self.bubble_speed < 100:
                self.bubble_speed += 5
        if self.timer_bubble.is_next_stop_reached():
            if len(self.all_sprites) <= cfg.MAX_BUBBLES:
                b = Bubble(self.bubble_speed)
                for _ in range(100):
                    b.randompos()
                    b.radius += cfg.DISTANCE
                    collided = pygame.sprite.spritecollide(b, self.all_sprites, False, pygame.sprite.collide_circle)
                    b.radius -= cfg.DISTANCE
                    if not collided:
                        self.all_sprites.add(b)
                        break

    def collidepoint(self, point: Tuple[int, int], sprite: pygame.sprite.Sprite) -> bool:
        if hasattr(sprite, "radius"):
            deltax = point[0] - sprite.rect.centerx
            deltay = point[1] - sprite.rect.centery
            return deltax * deltax + deltay * deltay <= sprite.radius * sprite.radius
        return False

    def set_mousecursor(self) -> None:
        is_over = False
        pos = pygame.mouse.get_pos()
        for b in self.all_sprites:
            if self.collidepoint(pos, b):
                is_over = True
                break
        if is_over:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_CROSSHAIR)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)

    def sting(self, mousepos: Tuple[int, int]) -> None:
        for bubble in self.all_sprites:
            if self.collidepoint(mousepos, bubble):
                bubble.update(action="sting")

    def check_bubblecollision(self) -> bool:
        for index1 in range(0, len(self.all_sprites) - 1):
            for index2 in range(index1 + 1, len(self.all_sprites)):
                bubble1 = self.all_sprites.sprites()[index1]
                bubble2 = self.all_sprites.sprites()[index2]
                if type(bubble1).__name__ == "Bubble" and type(bubble2).__name__ == "Bubble":
                    if pygame.sprite.collide_circle(bubble1, bubble2):
                        bubble1.update(mode="red")
                        bubble2.update(mode="red")
                        return True
                    if not cfg.PLAYGROUND.contains(bubble1):
                        bubble1.update(mode="red")
                        return True
                    if not cfg.PLAYGROUND.contains(bubble2):
                        bubble2.update(mode="red")
                        return True
        return False

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
