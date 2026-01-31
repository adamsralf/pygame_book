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
        self.todelete = False                       # Delete flag§\label{srcCircles0500}§

    def update(self, window: pygame.Window) -> None:
        self.speedy += Circle.GRAVITY
        self.posx += self.speedx
        self.posy += self.speedy
        if self.posx - self.radius < 0:             # Left side out§\label{srcCircles0501}§
            self.todelete = True
        elif self.posx + self.radius > window.size[0]:  # Right side out§\label{srcCircles0502}§
            self.todelete = True
        elif self.posy - self.radius > window.size[1]:  # Bottom out§\label{srcCircles0503}§
            self.todelete = True

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
            for i in range(5):                      # 5 particles at once§\label{srcCircles0504}§
                circles.append(Circle(pygame.mouse.get_pos()))

        todelete = []                               # Temporary storag§\label{srcCircles0505}§
        for p in circles:
            p.update(window)
            if p.todelete:                          # Marked for deletion?§\label{srcCircles0506}§
                todelete.append(p)
        for p in todelete:                          # Delete§\label{srcCircles0507}§
            circles.remove(p)

        screen.fill("white")
        for p in circles:
            p.draw(screen)

        window.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == '__main__':
    main()
