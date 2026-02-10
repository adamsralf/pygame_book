from random import choice, randint
from time import time
from typing import Any, Tuple

import config as cfg
import pygame
from config import MyEvents
from pygame.constants import (K_ESCAPE, KEYDOWN, MOUSEBUTTONDOWN, QUIT,
                              WINDOWPOS_CENTERED)


class Button(pygame.sprite.Sprite):

    def __init__(self, text: str, position: Tuple[int], *groups: Tuple[pygame.sprite.Group]) -> None:
        super().__init__(*groups)
        self.font = pygame.font.SysFont(None, 30)
        self.centerxy = (cfg.WINDOW.centerx, self.font.get_height() // 2)
        self.text = text
        self.image = self.font.render(self.text, True, "black")
        self.rect = self.image.get_rect(topleft=(position))

    def update(self, *args: Any, **kwargs: Any) -> None:
        if "action" in kwargs.keys():
            if kwargs["action"] == "pressed":
                pygame.event.post(pygame.event.Event(MyEvents.BUTTONPRESSED, text=self.text))
        return super().update(*args, **kwargs)


class Particle(pygame.sprite.Sprite):
    r, g, b = 0, 0, 0
    halted = False

    def __init__(self, *groups: Tuple[pygame.sprite.Group]) -> None:
        super().__init__(*groups)
        self.image = pygame.Surface((randint(3, 6), randint(3, 6)))
        self.image.fill((Particle.r, Particle.g, Particle.b))
        self.nextcolor()
        self.rect = pygame.FRect(self.image.get_rect())
        self.rect.topleft = (
            randint(30, cfg.WINDOW.right - 30),
            randint(30, cfg.WINDOW.bottom - 30),
        )
        self.speed = randint(100, 400)
        self.direction = pygame.Vector2(choice((-1, 1)), choice((-1, 1)))

    def update(self, *args: Any, **kwargs: Any) -> None:
        if "action" in kwargs.keys():
            if kwargs["action"] == "move":
                if not Particle.halted:
                    self.move()
            elif kwargs["action"] == "Start":
                Particle.halted = False
            elif kwargs["action"] == "Stop":
                Particle.halted = True

    def move(self) -> None:
        self.rect.move_ip(self.speed * self.direction * cfg.DELTATIME)
        if self.rect.left < cfg.WINDOW.left or self.rect.right > cfg.WINDOW.right:
            self.direction[0] *= -1
        if self.rect.top < cfg.WINDOW.top or self.rect.bottom > cfg.WINDOW.bottom:
            self.direction[1] *= -1
        self.rect.clamp_ip(cfg.WINDOW)

    def nextcolor(self):
        Particle.r += 5
        if Particle.r > 254:
            Particle.r = 0
            Particle.g += 5
            if Particle.g > 254:
                Particle.g = 5
                Particle.b += 5
                if Particle.b > 254:
                    Particle.b = 5


class Box(pygame.sprite.Sprite):

    def __init__(self, index: int, position: Tuple[int], *groups: Tuple[pygame.sprite.Group]) -> None:
        super().__init__(*groups)
        self.image = pygame.Surface((cfg.BOXWIDTH, 20))
        self.rect = self.image.get_rect(center=position)
        self.font = pygame.font.SysFont(None, 30)
        self.counter = 0
        self.index = index
        self.fill()

    def update(self, *args: Any, **kwargs: Any) -> None:
        if "counter" in kwargs.keys():
            if kwargs["counter"] == "inc":
                self.counter += 1
                if self.counter == 10:
                    pygame.event.post(pygame.event.Event(MyEvents.OVERFLOW, index=self.index))
                    self.counter = 0
                self.fill()
        return super().update(*args, **kwargs)

    def fill(self) -> None:
        self.image.fill("gray")
        number = self.font.render(f"{self.counter}", False, "Blue")
        self.image.blit(number, (18, 1))


class Game:

    def __init__(self) -> None:
        pygame.init()
        self.window = pygame.Window(size=cfg.WINDOW.size, title="Event (2)", position=WINDOWPOS_CENTERED)
        self.screen = self.window.get_surface()
        self.clock = pygame.time.Clock()
        self.all_sprites = pygame.sprite.Group()
        self.all_particles = pygame.sprite.Group()
        self.generate_particles(cfg.STARTNOFPARTICLES)
        self.all_buttons = pygame.sprite.Group()
        self.all_buttons.add(Button("Start", (30, cfg.WINDOW.bottom - 30), self.all_sprites))
        self.all_buttons.add(Button("Stop", (100, cfg.WINDOW.bottom - 30), self.all_sprites))
        self.all_boxes = pygame.sprite.Group()
        self.generate_boxes(cfg.NOFBOXES)
        pygame.time.set_timer(MyEvents.NEWPARTICLES, 500)  # Periodic event§\label{srcEvent0201}§
        self.running = True

    def run(self) -> None:
        time_previous = time()
        while self.running:
            self.watch_for_events()
            self.update()
            self.draw()
            self.clock.tick(cfg.FPS)
            time_current = time()
            cfg.DELTATIME = time_current - time_previous
            time_previous = time_current
        pygame.quit()

    def watch_for_events(self) -> None:
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.running = False
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.check_button_pressed(event.pos)
            elif event.type == MyEvents.BUTTONPRESSED:
                self.all_particles.update(action=event.text)
            elif event.type == MyEvents.OVERFLOW:
                if event.index < cfg.NOFBOXES - 1:
                    self.all_boxes.sprites()[event.index + 1].update(counter="inc")
            elif event.type == MyEvents.NEWPARTICLES:  # Periodisches Event §\label{srcEvent0202}§
                self.generate_particles(cfg.NEWNOFPARTICLES)

    def update(self):
        self.all_buttons.update()
        self.all_particles.update(action="move")
        self.check_boxcollision()

    def draw(self) -> None:
        self.screen.fill("white")
        self.all_sprites.draw(self.screen)
        self.window.flip()

    def generate_boxes(self, number: int) -> None:
        for i in range(number):
            self.all_boxes.add(Box(i, (cfg.WINDOW.right - 50 - i * 100, cfg.WINDOW.centery), self.all_sprites))

    def generate_particles(self, number: int) -> None:
        for i in range(number):
            self.all_particles.add(Particle(self.all_sprites))

    def check_button_pressed(self, position: Tuple[int]) -> None:
        for b in self.all_buttons.sprites():
            if b.rect.collidepoint(position):
                b.update(action="pressed")

    def check_boxcollision(self) -> None:
        c = pygame.sprite.groupcollide(self.all_particles, self.all_boxes, True, False) 
        for _ in c:
            self.all_boxes.sprites()[0].update(counter="inc")

def main():
    Game().run()


if __name__ == "__main__":
    main()
