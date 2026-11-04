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
        self.normal_image = self.image.copy()  ##
        self.selected_image = pygame.Surface((size, size), pygame.SRCALPHA)  
        pygame.draw.polygon(self.selected_image, cfg.MYCOLORS["selected"], points)  
        pygame.draw.polygon(self.selected_image, cfg.MYCOLORS["asteroid"], points, 2)  
        self.warning_image = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.polygon(self.warning_image, cfg.MYCOLORS["collision_warning"], points)
        pygame.draw.polygon(self.warning_image, cfg.MYCOLORS["asteroid"], points, 2)
        self.selection_mask = pygame.mask.from_surface(self.selected_image)
        self.rect : pygame.FRect = self.image.get_frect()
        self.rect.center = cfg.WINDOW.center
        self.totalspeed = randint(100, 250)                                 
        self.angle = randint(0, 359)                                        
        self.speed = pygame.Vector2(self.totalspeed, 0).rotate(self.angle) 

    def update(self, *args: Any, **kwargs: Any) -> None:
        position = pygame.Vector2(self.rect.center) 
        position += self.speed * cfg.DELTATIME      
        self.rect.center = position                 
        self.wrap()

    def wrap(self) -> None:
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
        self.rect.center = pygame.Vector2(self.rect.center) + self.speed * cfg.DELTATIME 
        self.remaining -= cfg.DELTATIME
        if self.remaining <= 0:
            self.kill()
        else:
            self.update_color()

    def update_color(self) -> None:
        if self.remaining <= 0:
            return
        progress = 1 - self.remaining / self.lifetime   
        color = tuple(
            int(start + (end - start) * progress)       
            for start, end in zip(self.start_color, self.end_color)
        )
        self.image.fill((0, 0, 0, 0))                   
        pygame.draw.circle(self.image, color, (3, 3), 3)
        self.image.set_alpha(int(255 * self.remaining / self.lifetime))


class Bullet(pygame.sprite.Sprite):

    def __init__(self, position: pygame.Vector2, speed: pygame.Vector2) -> None:
        super().__init__()
        self.image : pygame.Surface = pygame.Surface((3, 3), pygame.SRCALPHA)
        self.image.fill(cfg.MYCOLORS["bullet"])
        self.rect : pygame.FRect = self.image.get_frect(center=position)
        self.speed = speed

    def update(self, *args: Any, **kwargs: Any) -> None:
        self.rect.center = pygame.Vector2(self.rect.center) + self.speed * cfg.DELTATIME 
        if not self.rect.colliderect(cfg.WINDOW):
            self.kill()


class Spaceship(pygame.sprite.Sprite):

    def __init__(self, particles: pygame.sprite.Group, 
                       bullets: pygame.sprite.Group) -> None: 
        super().__init__()
        self.original_image_normal = pygame.Surface((40, 40), pygame.SRCALPHA)
        pygame.draw.polygon(self.original_image_normal, 
                            cfg.MYCOLORS["spaceship"], 
                            [(20, 2), (5, 35), (35, 35)], 2)
        self.original_image_stop = pygame.Surface((40, 40), pygame.SRCALPHA)
        pygame.draw.polygon(self.original_image_stop, 
                            cfg.MYCOLORS["spaceship_stop"], 
                            [(20, 2), (5, 35), (35, 35)], 4)
        self.image : pygame.Surface = self.original_image_normal
        self.rect : pygame.FRect = self.image.get_frect(center=cfg.WINDOW.center)
        self.speed = pygame.Vector2()
        self.angle = 0
        self.particles = particles
        self.bullets = bullets              
        self.rotation = 0
        self.thrust = 0
        self.is_stopping = False
        self.target : Asteroid | None = None 

    def update(self, *args: Any, **kwargs: Any) -> None:
        if "rotate" in kwargs:
            self.rotate(kwargs["rotate"])
        if "action" in kwargs:
            action = kwargs["action"]
            if action == "thrust":
                self.thrusting(True)
            elif action == "unthrust":
                self.thrusting(False)
            elif action == "move":
                self.move()
            elif action == "stop":
                self.target = None 
                self.is_stopping = not self.is_stopping
            elif action == "fire":      
                self.fire()             

    def rotate(self, direction: str="") -> None:
        if direction == "left":
            self.rotation = -cfg.ROTATION_SPEED
        elif direction == "right":
            self.rotation = cfg.ROTATION_SPEED
        elif direction == "stop":
            self.rotation = 0
        self.angle += self.rotation * cfg.DELTATIME         
        self.angle %= 360                                   
        image = self.original_image_stop if self.is_stopping else self.original_image_normal
        self.image = pygame.transform.rotate(image, -self.angle)  
   
    def move(self) -> None:
        if self.is_stopping:
            self.stop()
        if self.target is not None:  
            self.aim_at_target()
        else:
            self.rotate()
        self.thrusting(None)
        position = pygame.Vector2(self.rect.center) + self.speed * cfg.DELTATIME
        self.rect = self.image.get_frect(center=position)
        self.wrap()

    def wrap(self) -> None:
        if self.rect.left > cfg.WINDOW.right:
            self.rect.right = cfg.WINDOW.left + 1
        elif self.rect.right < cfg.WINDOW.left:
            self.rect.left = cfg.WINDOW.right - 1
        if self.rect.top > cfg.WINDOW.bottom:
            self.rect.bottom = cfg.WINDOW.top + 1
        elif self.rect.bottom < cfg.WINDOW.top:
            self.rect.top = cfg.WINDOW.bottom - 1

    def thrusting(self, flag: bool|None) -> None:
        if flag is not None:
            self.thrust = cfg.THRUST if flag else 0
        direction = pygame.Vector2(0, -1).rotate(self.angle)               
        if self.thrust > 0:
            particle_position = pygame.Vector2(self.rect.center) - direction * 15    
            particle_speed = self.speed - direction.rotate(uniform(-30, 30)) * uniform(100, 180) 
            self.particles.add(Particle(particle_position, particle_speed))
        self.speed += direction * self.thrust * cfg.DELTATIME              
        if self.speed.length_squared() > cfg.MAX_SPEED ** 2:    # Limit spaceship speed
            self.speed.scale_to_length(cfg.MAX_SPEED)           # Preserve the flight direction

    def stop(self) -> None:
        speed = self.speed.length()                         
        if speed <= 10:                                     # nearly stopped
            self.speed = pygame.Vector2(0,0)                
            self.rotate("stop")
            self.thrusting(False)
            self.is_stopping = False
        else:                                               # still stopping
            target_angle = pygame.Vector2(0, -1).angle_to(-self.speed) % 360 
            angle_difference = (target_angle - self.angle + 180) % 360 - 180
            frame_rotation = cfg.ROTATION_SPEED * cfg.DELTATIME              
            if abs(angle_difference) <= 2 * frame_rotation: # opposite direction nearly reached
                self.angle = target_angle
                self.rotate("stop")
                self.thrusting(True)
            elif angle_difference > 0:                      # not reached
                self.rotate("right")
            else:
                self.rotate("left")

    def aim_at_target(self) -> None:
        offset = pygame.Vector2(self.target.rect.center) - pygame.Vector2(self.rect.center)
        self.rotation = 0
        if offset.length_squared() > 0:
            target_angle = pygame.Vector2(0, -1).angle_to(offset) % 360
            angle_difference = (target_angle - self.angle + 180) % 360 - 180
            frame_rotation = cfg.ROTATION_SPEED * cfg.DELTATIME
            if abs(angle_difference) <= frame_rotation:
                self.angle = target_angle
                self.rotate(direction="stop")
            elif angle_difference > 0:
                self.rotate(direction="right")
            else:
                self.rotate(direction="left")

    def fire(self) -> None:        
        direction = pygame.Vector2(0, -1).rotate(self.angle)
        bullet_position = pygame.Vector2(self.rect.center) + direction * 18
        bullet_speed = self.speed + direction * cfg.BULLET_SPEED        
        self.bullets.add(Bullet(bullet_position, bullet_speed))


class Game:

    def __init__(self) -> None:
        pygame.init()
        self.window = pygame.Window(size=cfg.WINDOW.size, title=cfg.TITLE)
        self.screen = self.window.get_surface()
        self.clock = pygame.time.Clock()
        self.asteroid = pygame.sprite.Group()
        self.particles = pygame.sprite.Group()                                  
        self.bullets = pygame.sprite.Group()    
        self.spaceship = pygame.sprite.GroupSingle(Spaceship(self.particles, self.bullets))
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
                elif event.key == pygame.K_LEFT:            
                    spaceship.update(rotate="left")
                elif event.key == pygame.K_RIGHT:
                    spaceship.update(rotate="right")
                elif event.key == pygame.K_UP:
                    spaceship.update(action="thrust")
                elif event.key == pygame.K_DOWN:
                    spaceship.update(action="stop")
                elif event.key == pygame.K_f:           
                    spaceship.update(action = "fire")
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:  
                self.select_asteroid(event.pos)  
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    spaceship.update(action="unthrust")
                elif event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                    spaceship.update(rotate="stop")

    def select_asteroid(self, position: tuple[int, int]) -> None:  
        spaceship : Spaceship = self.spaceship.sprite  
        if spaceship.target is not None:
            spaceship.target.image = spaceship.target.normal_image
            spaceship.target = None  
        spaceship.rotation = 0  
        for asteroid in self.asteroid:  
            if asteroid.rect.collidepoint(position):  
                local = pygame.Vector2(position) - pygame.Vector2(asteroid.rect.topleft)  
                pixel = (int(local.x), int(local.y))  
                if asteroid.selection_mask.get_at(pixel):  
                    spaceship.target = asteroid  
                    spaceship.is_stopping = False  
                    asteroid.image = asteroid.selected_image  
                    break  

    def update(self) -> None:
        self.asteroid.update()
        self.particles.update()                         
        self.bullets.update()      
        self.spaceship.update(action="move")
        self.update_collision_warnings()

    def update_collision_warnings(self) -> None:  
        spaceship : Spaceship = self.spaceship.sprite 
        for asteroid in self.asteroid: 
            if asteroid is spaceship.target: 
                asteroid.image = asteroid.selected_image 
            elif self.collision_expected(asteroid, spaceship):
                asteroid.image = asteroid.warning_image 
            else:  
                asteroid.image = asteroid.normal_image  

    def collision_expected(self, asteroid: Asteroid, spaceship: Spaceship) -> bool:
        return self.collision_positions(asteroid, spaceship) is not None

    def collision_positions(
        self, asteroid: Asteroid, spaceship: Spaceship
    ) -> tuple[pygame.Vector2, pygame.Vector2] | None:
        offset = pygame.Vector2(asteroid.rect.center) - pygame.Vector2(spaceship.rect.center)
        relative_speed = asteroid.speed - spaceship.speed
        radius = max(asteroid.rect.size) // 2
        radius += max(spaceship.rect.size) // 2 
        closest_time = 0.0
        if relative_speed.length_squared() > 0:
            closest_time = -offset.dot(relative_speed) / relative_speed.length_squared()
            closest_time = pygame.math.clamp(closest_time, 0.0, max(0.0, cfg.COLLISION_WARNING_TIME))
        closest_offset = offset + relative_speed * closest_time
        if closest_offset.length_squared() > radius ** 2:
            return None
        asteroid_pos = pygame.Vector2(asteroid.rect.center)+asteroid.speed*closest_time    #§\label{asteroid0802}§
        spaceship_pos = pygame.Vector2(spaceship.rect.center)+spaceship.speed*closest_time #§\label{asteroid0803}§
        return asteroid_pos, spaceship_pos  #§\label{asteroid0804}§

    def draw(self) -> None:
        self.screen.fill(cfg.MYCOLORS["background"])
        self.asteroid.draw(self.screen)
        self.particles.draw(self.screen)                
        self.bullets.draw(self.screen)                  
        self.spaceship.draw(self.screen)                
        if cfg.SHOW_VELOCITY:
            for asteroid in self.asteroid:
                self.draw_velocity(asteroid)            
            self.draw_target()                          
            spaceship = self.spaceship.sprite
            if spaceship is not None:
                self.draw_velocity(spaceship)
                for asteroid in self.asteroid:                                                 #§\label{asteroid0805}§
                    self.draw_collision_prediction(asteroid, spaceship)
        self.window.flip()

    def draw_collision_prediction(self, asteroid: Asteroid, spaceship: Spaceship) -> None:
        positions = self.collision_positions(asteroid, spaceship)
        if positions is None:
            return
        asteroid_position, spaceship_position = positions
        color = cfg.MYCOLORS["collision_prediction"]
        pygame.draw.line(self.screen, color, asteroid.rect.center, asteroid_position, 2)
        pygame.draw.line(self.screen, color, spaceship.rect.center, spaceship_position, 2)
        collision_point = (asteroid_position + spaceship_position) / 2
        pygame.draw.circle(self.screen, color, collision_point, 5)

    def draw_velocity(self, mobs) -> None:
        start = pygame.Vector2(mobs.rect.center)
        if mobs.speed.length() > 0.0:                   
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

    def draw_target(self) -> None:
        spaceship : Spaceship = self.spaceship.sprite  
        if spaceship.target is not None:  
            direction = pygame.Vector2(0, -1).rotate(spaceship.angle)  
            tip = pygame.Vector2(spaceship.rect.center) + direction * 18  
            pygame.draw.line(self.screen, cfg.MYCOLORS["target_line"], tip, spaceship.target.rect.center, 2) 



def main():
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
