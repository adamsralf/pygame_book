from os import path

import pygame

WINDOW = pygame.rect.Rect((0, 0), (300, 200))
FPS = 60
DELTATIME = 1.0 / FPS
TITLE = "Animation"
PATH: dict[str, str] = {}
PATH["file"] = path.dirname(path.abspath(__file__))
PATH["image"] = path.join(PATH["file"], "images")

@staticmethod
def filepath(name: str) -> str:
    return path.join(PATH["file"], name)

@staticmethod
def imagepath(name: str) -> str:
    return path.join(PATH["image"], name)
