from random import randint, uniform
from time import time
from typing import Any, ClassVar

import pygame

import config as cfg


class Asteroid(pygame.sprite.Sprite):

    SHAPES : ClassVar[list[tuple[int, list[tuple[int, int]]]]] = [
        (30, [(9, 2), (23, 4), (28, 14), (21, 27), (5, 24), (2, 12)]),
        (45, [(14, 2), (37, 5), (42, 20), (30, 25),
              (35, 40), (13, 42), (2, 25)]),
        (60, [(18, 3), (40, 6), (56, 22), (48, 43),
              (32, 56), (10, 48), (3, 27)]),
        (75, [(23, 3), (48, 8), (70, 25), (57, 38),
              (68, 56), (42, 71), (17, 62), (3, 35)]),
        (90, [(30, 3), (60, 7), (85, 28), (73, 47),
              (83, 65), (54, 86), (34, 70), (10, 78), (3, 34)]),
    ]

    def __init__(self, number : int) -> None:
        super().__init__()
        size, points = self.SHAPES[number]
        self.image = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.polygon(self.image, cfg.MYCOLORS["asteroid"], points, 2)
        self.rect : pygame.FRect = self.image.get_frect()
        self.rect.center = cfg.WINDOW.center
        self.totalspeed = randint(100, 250)                                 
        self.angle = randint(0, 359)                                        
        self.speed = pygame.Vector2(self.totalspeed, 0).rotate(self.angle) 

    def update(self, *args: Any, **kwargs: Any) -> None:
        position = pygame.Vector2(self.rect.center) 
        position += self.speed * cfg.DELTATIME      
        self.rect.center = position                 
        if self.rect.left > cfg.WINDOW.right:
            self.rect.right = cfg.WINDOW.left + 1
        elif self.rect.right < cfg.WINDOW.left:
            self.rect.left = cfg.WINDOW.right - 1
        if self.rect.top > cfg.WINDOW.bottom:
            self.rect.bottom = cfg.WINDOW.top + 1
        elif self.rect.bottom < cfg.WINDOW.top:
            self.rect.top = cfg.WINDOW.bottom - 1


class Particle(pygame.sprite.Sprite):

    def __init__(self, position: pygame.Vector2, speed: pygame.Vector2) -> None:
        super().__init__()
        self.start_color = cfg.MYCOLORS["particle_start"]
        self.end_color = cfg.MYCOLORS["particle_end"]
        self.image : pygame.Surface = pygame.Surface((6, 6), pygame.SRCALPHA)
        self.rect : pygame.FRect = self.image.get_frect(center=position)
        self.speed = speed
        self.lifetime = uniform(0.4, 0.9)
        self.remaining = self.lifetime
        self.update_color()

    def update(self, *args: Any, **kwargs: Any) -> None:
        self.rect.center = pygame.Vector2(self.rect.center) + self.speed * cfg.DELTATIME # §\label{asteroid0304}§
        self.remaining -= cfg.DELTATIME
        if self.remaining <= 0:
            self.kill()
        else:
            self.update_color()

    def update_color(self) -> None:
        if self.remaining <= 0:
            return
        progress = 1 - self.remaining / self.lifetime   # §\label{asteroid0301}§
        color = tuple(
            int(start + (end - start) * progress)       # §\label{asteroid0302}§
            for start, end in zip(self.start_color, self.end_color)
        )
        self.image.fill((0, 0, 0, 0))                   # §\label{asteroid0303}§
        pygame.draw.circle(self.image, color, (3, 3), 3)
        self.image.set_alpha(int(255 * self.remaining / self.lifetime))


class Spaceship(pygame.sprite.Sprite):

    def __init__(self, particles: pygame.sprite.Group) -> None:
        super().__init__()
        self.original_image = pygame.Surface((40, 40), pygame.SRCALPHA)
        pygame.draw.polygon(self.original_image, cfg.MYCOLORS["spaceship"], [(20, 2), (5, 35), (35, 35)], 2)
        self.image = self.original_image
        self.rect : pygame.FRect = self.image.get_frect(center=cfg.WINDOW.center)
        self.speed = pygame.Vector2()
        self.angle = 0
        self.particles = particles
        self.rotation = 0
        self.thrust = 0

    def update(self, *args: Any, **kwargs: Any) -> None:
        if "rotate" in kwargs:
            if kwargs["rotate"] == "left":
                self.rotation = -cfg.ROTATION_SPEED
            elif kwargs["rotate"] == "right":
                self.rotation = cfg.ROTATION_SPEED
            elif kwargs["rotate"] == "stop":
                self.rotation = 0
            self.angle +=  self.rotation
            self.angle %= 360                       # §\label{asteroid0305}§
        if "action" in kwargs:
            if kwargs["action"] == "thrust":
                self.thrust = cfg.THRUST
            elif kwargs["action"] == "unthrust":
                self.thrust = 0
            elif kwargs["action"] == "move":
                self.move()

    def move(self) -> None:
        direction = pygame.Vector2(0, -1).rotate(self.angle)                            #§\label{asteroid0306}§
        if self.thrust > 0:
            position = pygame.Vector2(self.rect.center) - direction * 15                #§\label{asteroid0307}§
            speed = self.speed - direction.rotate(uniform(-30, 30)) * uniform(100, 180) #§\label{asteroid0308}§
            self.particles.add(Particle(position, speed))
        self.speed += direction * self.thrust * cfg.DELTATIME                           #§\label{asteroid0309}§
        position = pygame.Vector2(self.rect.center) + self.speed * cfg.DELTATIME
        self.image = pygame.transform.rotate(self.original_image, -self.angle)          #§\label{asteroid0310}§
        self.rect = self.image.get_frect(center=position)
        if self.rect.left > cfg.WINDOW.right:
            self.rect.right = cfg.WINDOW.left + 1
        elif self.rect.right < cfg.WINDOW.left:
            self.rect.left = cfg.WINDOW.right - 1
        if self.rect.top > cfg.WINDOW.bottom:
            self.rect.bottom = cfg.WINDOW.top + 1
        elif self.rect.bottom < cfg.WINDOW.top:
            self.rect.top = cfg.WINDOW.bottom - 1


class Game:

    def __init__(self) -> None:
        pygame.init()
        self.window = pygame.Window(size=cfg.WINDOW.size, title=cfg.TITLE)
        self.screen = self.window.get_surface()
        self.clock = pygame.time.Clock()
        self.asteroid = pygame.sprite.Group()
        self.particles = pygame.sprite.Group()                                  # §\label{asteroid0311}§
        self.spaceship = pygame.sprite.GroupSingle(Spaceship(self.particles))   # §\label{asteroid0312}§
        self.size_by_key = {
            pygame.K_1: 0,
            pygame.K_2: 1,
            pygame.K_3: 2,
            pygame.K_4: 3,
            pygame.K_5: 4,
        }
        self.running = False

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

    def watch_for_events(self) -> None:
        spaceship : Spaceship = self.spaceship.sprite 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_F1:
                    cfg.SHOW_VELOCITY = not cfg.SHOW_VELOCITY
                elif event.key == pygame.K_SPACE:
                    if len(self.asteroid) > 0:
                        self.asteroid.remove(self.asteroid.sprites()[0])
                elif event.key in (pygame.K_1, pygame.K_2, 
                                   pygame.K_3, pygame.K_4, 
                                   pygame.K_5):
                    self.asteroid.add(Asteroid(self.size_by_key[event.key]))
                elif event.key == pygame.K_LEFT:            # §\label{asteroid0313}§
                    spaceship.update(rotate="left")
                elif event.key == pygame.K_RIGHT:
                    spaceship.update(rotate="right")
                elif event.key == pygame.K_UP:
                    spaceship.update(action="thrust")
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    spaceship.update(action="unthrust")
                

    def update(self) -> None:
        self.asteroid.update()
        self.particles.update()
        self.spaceship.update(action="move")

    def draw(self) -> None:
        self.screen.fill(cfg.MYCOLORS["background"])
        self.asteroid.draw(self.screen)
        self.particles.draw(self.screen)                # §\label{asteroid0315}§
        self.spaceship.draw(self.screen)                # §\label{asteroid0316}§
        if cfg.SHOW_VELOCITY:
            for asteroid in self.asteroid:
                self.draw_velocity(asteroid)            # §\label{asteroid0317}§
            self.draw_velocity(self.spaceship.sprite)   # §\label{asteroid0318}§
        self.window.flip()

    def draw_velocity(self, mobs) -> None:
        start = pygame.Vector2(mobs.rect.center)
        if mobs.speed.length() > 0.0:                   # §\label{asteroid0314}§
            direction = mobs.speed.normalize()
            end = start + mobs.speed * 0.15
            arrow_base = end - direction * 7
            arrow_side = direction.rotate(90) * 4
            pygame.draw.line(self.screen, cfg.MYCOLORS["velocity"], start, end, 2)
            pygame.draw.polygon(
                self.screen,
                cfg.MYCOLORS["velocity"],
                (end, arrow_base + arrow_side, arrow_base - arrow_side),
            )



def main():
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
