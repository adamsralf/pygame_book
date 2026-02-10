from random import randint

import pygame


class Circle:
    GRAVITY = 0.3
    RADIUS_INC = -0.1                                       # Radius increment§\label{srcCircles0600}§

    def __init__(self, pos) -> None:
        self.posx = pos[0] + randint(-4, 4)                 # Changed spread§\label{srcCircles0601}§
        self.posy = pos[1] + randint(-4, 4)
        self.radius = 8
        self.color = [randint(100, 255), randint(50, 255), 0]
        self.speedx = randint(-15, 15) / 10.01              # Fountain wider§\label{srcCircles0602}§
        self.speedy = randint(-100, 0) / 10.01
        self.todelete = False

    def update(self, window: pygame.Window) -> None:
        self.speedy -= Circle.GRAVITY
        self.posx += self.speedx
        self.posy += self.speedy
        self.radius += Circle.RADIUS_INC
        if self.posx - self.radius < 0:
            self.todelete = True
        elif self.posx + self.radius > window.size[0]:
            self.todelete = True
        elif self.posy - self.radius > window.size[1]:
            self.todelete = True
        elif self.radius <= 0.0:                            # Can be removed§\label{srcCircles0603}§
            self.todelete = True

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.circle(screen, self.color, (self.posx, self.posy), self.radius)


def main():
    size = (300, 600)
    pygame.init()
    window = pygame.Window( size=size, title = "Particle swarm", position = (10, 50))         
    screen = window.get_surface()                   
    clock = pygame.time.Clock()
    circles = []

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if pygame.mouse.get_pressed()[0]:
            for i in range(5):
                circles.append(Circle(pygame.mouse.get_pos()))

        todelete = []
        for p in circles:
            p.update(window)
            if p.todelete:
                todelete.append(p)
        for p in todelete:
            circles.remove(p)

        screen.fill("white")
        for p in circles:
            p.draw(screen)

        window.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == '__main__':
    main()
