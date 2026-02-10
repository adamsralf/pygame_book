import pygame

WINDOW = pygame.Rect(0, 0, 1000, 600)
FPS = 60
DELTATIME = 1.0 / FPS
KI = {"left": False, "right": False}            # Flag computer player§\label{srcPong0602}§

class MyEvents:
    POINT_FOR = pygame.USEREVENT
    MYEVENT = pygame.event.Event(POINT_FOR, player=0)

