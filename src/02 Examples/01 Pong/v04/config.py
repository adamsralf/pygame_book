import pygame

WINDOW = pygame.Rect(0, 0, 1000, 600)
FPS = 60
DELTATIME = 1.0 / FPS

class MyEvents:                                     # User events§\label{srcPong0400}§
    POINT_FOR = pygame.USEREVENT
    MYEVENT = pygame.event.Event(POINT_FOR, player=0)

