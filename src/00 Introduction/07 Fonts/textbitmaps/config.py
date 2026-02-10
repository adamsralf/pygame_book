import os

import pygame

WINDOW = pygame.Rect((0, 0), (700, 650))
PATH: dict[str, str] = {}
PATH["file"] = os.path.dirname(os.path.abspath(__file__))
PATH["image"] = os.path.join(PATH["file"], "images")
FPS = 60

def filepath(name: str) -> str:
    return os.path.join(PATH["file"], name)

def imagepath(name: str) -> str:
    return os.path.join(PATH["image"], name)
