import pygame

WINDOW = pygame.rect.Rect((0, 0), (600, 150))
FPS = 60
DELTATIME = 1.0 / FPS
STARTNOFPARTICLES = 999
NOFBOXES = 3
BOXWIDTH = 50

class MyEvents:                                     # Only for autocompletion (convenience)§\label{srcEvent0100}§
    BUTTONPRESSED = pygame.USEREVENT + 0            # Event id for button presses§\label{srcEvent0101}§
    OVERFLOW = pygame.USEREVENT + 1                 # Event id for overflow§\label{srcEvent0102}§



