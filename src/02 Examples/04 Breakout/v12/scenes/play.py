import pygame

import config as cfg
from scenes.state import State
from sprites import Ball, Brick, BrickFragment, Paddle, Status, TrailBall


class PlayState(State):
    def __init__(self, game):
        super().__init__(game)
        cfg.POINTS = 0
        cfg.LEVEL = 1
        cfg.BALLS = 3
        cfg.AUTOPILOT = False
        self.bricks = pygame.sprite.Group()
        paddle = Paddle()
        self.paddle = pygame.sprite.GroupSingle(paddle)
        self.ball = pygame.sprite.GroupSingle(Ball(paddle))
        self.status = pygame.sprite.GroupSingle(Status())
        self.trail = pygame.sprite.Group()                  
        self.trail_freq = 20
        self.trail_next =  pygame.time.get_ticks() + self.trail_freq
        self.fragments = pygame.sprite.Group()  # §\label{breakoutplay1201}§

        self.create_bricks()
        self.ball.update(action="launch")

    def watch_for_events(self, events: list[pygame.event.Event]) -> None:
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.ball.update(action="launch")
                elif event.key == pygame.K_RIGHT and not cfg.AUTOPILOT:
                    self.paddle.update(action="right")
                elif event.key == pygame.K_LEFT and not cfg.AUTOPILOT:
                    self.paddle.update(action="left")
                elif event.key == pygame.K_F2:
                    cfg.AUTOPILOT = not cfg.AUTOPILOT
                elif event.key == pygame.K_p:
                    self.paddle.update(action="stop")
                    pygame.event.post(pygame.event.Event(self.game.events["PAUSE"]))
                elif event.key == pygame.K_h:
                    self.paddle.update(action="stop")
                    pygame.event.post(pygame.event.Event(self.game.events["HELP"]))
            elif event.type == pygame.KEYUP:
                if event.key in (pygame.K_RIGHT, pygame.K_LEFT) and not cfg.AUTOPILOT:
                    self.paddle.update(action="stop")

    def update(self) -> None:
        ball : Ball = self.ball.sprite
        paddle : Paddle = self.paddle.sprite
        if cfg.AUTOPILOT:
            if ball.speedxy.length() != 0:
                if ball.rect.right > paddle.rect.left:
                    paddle.update(action="right")
                elif ball.rect.left < paddle.rect.right:
                    paddle.update(action="left")
                else:
                    paddle.update(action="stop")
        paddle.update(action="move")
        ball.update(action="move")
        if pygame.time.get_ticks() > self.trail_next:       # Next TrailBall?
            self.trail.add(TrailBall(ball))
            self.trail_next = pygame.time.get_ticks() + self.trail_freq
        self.trail.update()

        if ball.is_lost():
            cfg.BALLS -= 1
            if cfg.BALLS <= 0:
                pygame.event.post(pygame.event.Event(self.game.events["GAME_OVER"]))
            else:
                paddle.update(action="reset")
                ball.update(action="reset")
                self.trail.empty()

        collided_bricks = pygame.sprite.spritecollide(ball, self.bricks, False)
        for brick in collided_bricks:
            ball.update(action="bounce", brick=brick)
            brick.update(action="hit")
            if not brick.alive():
                self.fragments.add(
                    *(
                        BrickFragment(brick, column, row)
                        for row in range(cfg.BRICK["fragy"])
                        for column in range(cfg.BRICK["fragx"])
                    )
                )

        if not self.bricks and cfg.BALLS > 0:
            cfg.LEVEL += 1
            cfg.BALLS += 1
            self.create_bricks()
            paddle.update(action="reset")
            ball.update(action="reset")
            self.trail.empty()
        self.bricks.update()
        self.fragments.update()             
        self.status.update()

    def draw(self) -> None:
        if cfg.AUTOPILOT:
            self.game.screen.fill("springgreen4")
        else:
            self.game.screen.fill("black")
        self.status.draw(self.game.screen)
        self.bricks.draw(self.game.screen)
        self.paddle.draw(self.game.screen)
        self.trail.draw(self.game.screen)
        self.ball.draw(self.game.screen)
        self.fragments.draw(self.game.screen)   

    def create_bricks(self) -> None:
        rows = min(cfg.LEVEL + 2, cfg.BRICK["rows"])
        self.bricks.empty()
        for row in range(rows):
            for col in range(cfg.BRICK["cols"]):
                self.bricks.add(Brick((col, row)))
