import pygame


class MyEvents:
    BUTTONPRESSED = pygame.event.custom_type()
    OVERFLOW = pygame.event.custom_type()
    NEWPARTICLES = pygame.event.custom_type()


WINDOW = pygame.Rect((0, 0), (600, 150))
FPS = 60
DELTATIME = 1.0 / FPS
STARTNOFPARTICLES = 500
NEWNOFPARTICLES = 10
NOFBOXES = 5
BOXWIDTH = 50


