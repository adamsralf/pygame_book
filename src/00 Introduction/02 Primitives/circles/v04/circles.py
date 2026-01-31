from random import randint

import pygame


class Circle:
    GRAVITY = 0.3

    def __init__(self, pos) -> None:
        self.posx = pos[0] + randint(-2, 2)
        self.posy = pos[1] + randint(-2, 2)
        self.radius = 2
        self.color = [randint(100, 255), randint(50, 255), 0]
        self.speedx = randint(-10, 10) / 10.01
        self.speedy = randint(-100, 0) / 10.01

    def update(self) -> None:
        self.speedy += Circle.GRAVITY
        self.posx += self.speedx
        self.posy += self.speedy

    def draw(self, screen: pygame.surface.Surface) -> None:
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
            circles.append(Circle(pygame.mouse.get_pos()))

        for p in circles:
            p.update()

        screen.fill("white")
        for p in circles:
            p.draw(screen)

        window.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == '__main__':
    main()
