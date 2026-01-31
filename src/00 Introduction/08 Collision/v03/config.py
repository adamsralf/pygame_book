from os import path

import pygame

WINDOW = pygame.rect.Rect((0, 0), (700, 200))
FPS = 60
TITLE = "Collision Types"
PATH: dict[str, str] = {}
PATH["file"] = path.dirname(path.abspath(__file__))
PATH["image"] = path.join(PATH["file"], "images")
MODE = "rect"

@staticmethod
def filepath(name: str) -> str:
    return path.join(PATH["file"], name)

@staticmethod
def imagepath(name: str) -> str:
    return path.join(PATH["image"], name)

