import math
from time import time
from typing import Any

import pygame

import config as cfg


class Brick(pygame.sprite.Sprite):
    def __init__(self, position: tuple[int, int]):
        super().__init__()
        filename = cfg.get_image(f"brick{position[1]:02d}00.png")
        self.image : pygame.Surface = pygame.image.load(filename).convert_alpha()
        self.image = pygame.transform.scale(self.image, cfg.BRICK["rect"].size)
        self.rect : pygame.FRect = self.image.get_frect()
        self.rect.left = cfg.BRICK["dist"]["x"] 
        self.rect.left += position[0] * (cfg.BRICK["rect"].width + cfg.BRICK["dist"]["x"])
        self.rect.top = 2 * cfg.BALLSIZE 
        self.rect.top += position[1] * (cfg.BRICK["rect"].height + cfg.BRICK["dist"]["y"])
        self.points = (cfg.BRICK["rows"] - position[1]) * 10  # Points for hitting this brick

    def update(self, *args: Any, **kwargs: Any) -> None:
        if "action" in kwargs:
            if kwargs["action"] == "hit":
                self.hit()
        return super().update(*args, **kwargs)

    def hit(self) -> None:
        cfg.POINTS += self.points
        self.kill()  # Remove the brick from all groups


class Paddle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image : pygame.Surface = pygame.image.load(cfg.get_image("bar.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, cfg.BRICK["rect"].size)
        self.rect : pygame.FRect = self.image.get_frect()
        self.rect.bottom = cfg.WINDOW.bottom - cfg.STATUSHEIGHT
        self.rect.centerx = cfg.WINDOW.centerx
        self.speed_max = 500                # px/s
        self.speed_now = 0                  # px/s

    def update(self, *args: Any, **kwargs: Any) -> None:
        if "action" in kwargs:
            if kwargs["action"] == "right":
                   self.speed_now = self.speed_max
            elif kwargs["action"] == "left":
                    self.speed_now = -self.speed_max
            elif kwargs["action"] == "stop":
                 self.speed_now = 0 
            elif kwargs["action"] == "move":
                self.rect.left += self.speed_now * cfg.DELTATIME
                self.rect.clamp_ip(cfg.WINDOW)
        return super().update(*args, **kwargs)

    
class Ball(pygame.sprite.Sprite):
    def __init__(self, paddle: Paddle):
        super().__init__()
        self.paddle = paddle
        self.image = pygame.image.load(cfg.get_image("ball.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, (cfg.BALLSIZE, cfg.BALLSIZE))
        self.rect : pygame.FRect = self.image.get_frect()
        self.speed = 500                # px/s
        self.speedxy : pygame.Vector2 = pygame.Vector2(0, 0)
        self.reset()

    def update(self, *args: Any, **kwargs: Any) -> None:
        if "action" in kwargs:
            if kwargs["action"] == "launch":
                if self.speedxy.length() == 0:            # ball is not moving
                    self.launch()
            elif kwargs["action"] == "move":
                if self.speedxy.length() > 0:             # ball is moving
                    self.rect.move_ip(self.speedxy * cfg.DELTATIME)
                    if self.rect.left <= cfg.WINDOW.left or self.rect.right >= cfg.WINDOW.right:
                        self.speedxy.x *= -1
                    if self.rect.top <= cfg.WINDOW.top or self.rect.bottom >= cfg.WINDOW.bottom:
                        self.speedxy.y *= -1
                    self.rect.clamp_ip(cfg.WINDOW)
                    self.bounce_paddle()
                else:                                   # ball is not moving
                    self.reset()
            elif kwargs["action"] == "reset":
                self.reset()
            elif kwargs["action"] == "bounce":
                if "brick" in kwargs:
                    self.bounce(kwargs["brick"])
        return super().update(*args, **kwargs)

    def launch(self) -> None:
        self.reset()
        self.speedxy = pygame.Vector2(self.speed, -self.speed)  # px/s

    def reset(self) -> None:
        self.rect.centerx = self.paddle.rect.centerx
        self.rect.bottom = self.paddle.rect.top + 2
        self.speedxy = pygame.Vector2(0, 0)  # px/s

    def bounce_paddle(self) -> None:
        if self.speedxy.y <= 0:                           # ball is moving upwards
            return
        if not self.rect.colliderect(self.paddle.rect):    # ball is not colliding with the paddle
            return

        self.rect.bottom = self.paddle.rect.top            # move the ball above the bar
        offset = (self.rect.centerx - self.paddle.rect.centerx) / (self.paddle.rect.width / 2)
        offset = pygame.math.clamp(offset, -1.0, 1.0)   # Limit the offset to [-1, 1]

        speed = self.speed * (1 + abs(offset) * 0.75)          # new speed of the ball
        angle = math.radians(offset * 60)               # angle of the ball in radians
        self.speedxy.x = speed * math.sin(angle)
        self.speedxy.y = -speed * math.cos(angle)

    def bounce(self, brick: Brick) -> None:
        overlap_x = min(self.rect.right, brick.rect.right) - max(self.rect.left, brick.rect.left)
        overlap_y = min(self.rect.bottom, brick.rect.bottom) - max(self.rect.top, brick.rect.top)
        if overlap_x < overlap_y:                       # horizontal collision
            if self.rect.centerx < brick.rect.centerx:  # from left
                self.rect.right = brick.rect.left
            else:                                       # from right
               self.rect.left = brick.rect.right
            self.speedxy.x *= -1
        else:                                           # vertical collision
            if self.rect.centery < brick.rect.centery:  # from top
                self.rect.bottom = brick.rect.top
            else:                                       # from bottom
                self.rect.top = brick.rect.bottom
            self.speedxy.y *= -1


class Status(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image : pygame.Surface = pygame.surface.Surface((cfg.WINDOW.width, cfg.STATUSHEIGHT))
        self.image_ball = pygame.image.load(cfg.get_image("ball.png")).convert_alpha()
        self.image_ball = pygame.transform.scale_by(self.image_ball, 0.125)
        self.rect : pygame.Rect = self.image.get_rect()
        self.rect.bottom = cfg.WINDOW.bottom
        self.points = 0
        self.level = 0  
        self.balls = 0

    def update(self, *args: Any, **kwargs: Any) -> None:
        if self.points != cfg.POINTS or self.level != cfg.LEVEL or self.balls != cfg.BALLS:
            self.balls = cfg.BALLS
            self.level = cfg.LEVEL
            self.points = cfg.POINTS
            self.render()

    def render(self) -> None:
        self.image.fill("black")
        font = pygame.font.Font(None, 36)

        balls_text = font.render("Balls: ", True, "white")
        balls_rect = balls_text.get_rect()
        balls_rect.centery = self.image.get_rect().centery
        balls_rect.left =  10
        self.image.blit(balls_text, balls_rect)
        for i in range(self.balls):
            ball_rect = self.image_ball.get_rect()
            ball_rect.centery = self.image.get_rect().centery
            ball_rect.left = balls_rect.right + 10 + i * (ball_rect.width + 5)
            self.image.blit(self.image_ball, ball_rect)

        points_text = font.render(f"Points: {self.points}", True, "white")
        points_rect = points_text.get_rect()
        points_rect.centery = self.image.get_rect().centery
        points_rect.centerx = self.image.get_rect().centerx
        self.image.blit(points_text, points_rect)

        level_text = font.render(f"Level: {self.level}", True, "white")
        level_rect = level_text.get_rect()
        level_rect.centery = self.image.get_rect().centery
        level_rect.right = self.image.get_rect().right - 10
        self.image.blit(level_text, level_rect)


class Game:
    def __init__(self):
        pygame.init()
        cfg.POINTS = 0  
        self.window = pygame.Window(size=cfg.WINDOW.size)
        self.window.title = cfg.CAPTION
        self.screen = self.window.get_surface()
        self.clock = pygame.time.Clock()
        self.running = True

        self.bricks = pygame.sprite.Group()
        for row in range(cfg.BRICK["rows"]):        
            for col in range(cfg.BRICK["cols"]):
                self.bricks.add(Brick((col, row))) 

        self.paddle = pygame.sprite.GroupSingle(Paddle())
        self.ball = pygame.sprite.GroupSingle(Ball(self.paddle.sprite))    # setup ball
        self.status = pygame.sprite.GroupSingle(Status())               # setup status bar 

    def run(self):
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

    def watch_for_events(self)-> None:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                         self.running = False
                    elif event.key == pygame.K_RIGHT and not cfg.AUTOPILOT: #§\label{breakout0702}§
                          self.paddle.update(action="right")   
                    elif event.key == pygame.K_LEFT and not cfg.AUTOPILOT:  #§\label{breakout0703}§
                        self.paddle.update(action="left")  
                    elif event.key == pygame.K_SPACE:
                        self.ball.update(action="launch")   
                    elif event.key == pygame.K_F2:                          #§\label{breakout0704}§
                        cfg.AUTOPILOT = not cfg.AUTOPILOT
                elif event.type == pygame.KEYUP:
                    if event.key in (pygame.K_RIGHT, pygame.K_LEFT) and not cfg.AUTOPILOT:
                        self.paddle.update(action="stop")      

    def update(self) -> None:
        if cfg.AUTOPILOT:                                   # §\label{breakout0701}§
            ball = self.ball.sprite
            if ball.speedxy.length() != 0:                    # ball is not moving 
                if ball.rect.centerx > self.paddle.sprite.rect.centerx:
                    self.paddle.update(action="right")
                elif ball.rect.centerx < self.paddle.sprite.rect.centerx:
                    self.paddle.update(action="left")
                else:
                    self.paddle.update(action="stop")
        self.paddle.update(action="move")                      
        self.ball.update(action="move")                     # move ball
        # Check for collisions between the ball and the bricks
        ball = self.ball.sprite
        collided_bricks = pygame.sprite.spritecollide(ball, self.bricks, False) 
        for brick in collided_bricks:  
            ball.update(action="bounce", brick=brick)  # Bounce the ball off the brick
            brick.update(action="hit")  # Update the brick (e.g., remove it if hit)
        self.bricks.update()
        self.status.update()                                # Update the status bar if needed 

    def draw(self) -> None:
            if cfg.AUTOPILOT:
                self.screen.fill("springgreen4")
            else:
                self.screen.fill("black")
            self.status.draw(self.screen)                   # draw status bar
            self.bricks.draw(self.screen)
            self.paddle.draw(self.screen)                      
            self.ball.draw(self.screen)                     # draw ball
            self.window.flip()



def main():
    game = Game()
    game.run()

if __name__ == "__main__":
    main()