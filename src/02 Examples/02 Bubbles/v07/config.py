import os
from typing import Dict

import pygame

WINDOW = pygame.Rect(0, 0, 1220, 1002)
FPS = 60
DELTATIME = 1.0 / FPS
PATH: Dict[str, str] = {}
PATH["file"] = os.path.dirname(os.path.abspath(__file__))
PATH["image"] = os.path.join(PATH["file"], "images")
PATH["sound"] = os.path.join(PATH["file"], "sounds")
CAPTION = 'Bubbles'
RADIUS = {"min": 15, "max": 240}
DISTANCE = 50
PLAYGROUND = pygame.Rect(90, 90, 1055, 615)
MAX_BUBBLES = PLAYGROUND.height * PLAYGROUND.width // 10000
POINTS = 0                                      # Score§\label{srcBubble0701}§
BOX = pygame.Rect(90, 770, 1055, 130)      # Messagebox§\label{srcBubble0700}§

@staticmethod
def get_file(filename: str) -> str:
    return os.path.join(PATH["file"], filename)

@staticmethod
def get_image(filename: str) -> str:
    return os.path.join(PATH["image"], filename)

@staticmethod
def get_sound(filename: str) -> str:
    return os.path.join(PATH["sound"], filename)

