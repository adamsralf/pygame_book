import os

import pygame

WINDOW = pygame.Rect(0, 0, 1000, 600)
FPS = 60
DELTATIME = 1.0 / FPS
KI = {"left": False, "right": False}    
SOUNDFLAG = True                                # Sound flag§\label{srcPong0701}§
PATH = {}
PATH["file"] = os.path.dirname(os.path.abspath(__file__))
PATH["sound"] = os.path.join(PATH["file"], "sounds")

def get_sound(filename: str) -> str:
    return os.path.join(PATH["sound"], filename)

class MyEvents:
    POINT_FOR = pygame.USEREVENT
    MYEVENT = pygame.event.Event(POINT_FOR, player=0)

