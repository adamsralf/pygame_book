from os import path

import pygame

WINDOW: pygame.Rect = pygame.Rect(0, 0, 400, 200)   # Rect
FPS = 60
DELTATIME = 1.0 / FPS
PATH: dict[str, str] = {}
PATH["file"] = path.dirname(path.abspath(__file__))
PATH["image"] = path.join(PATH["file"], "images")
PATH["sound"] = path.join(PATH["file"], "sounds")
START_DISTANCE = 20
VOLUME_STEP = 0.05

def get_file(filename: str) -> str:
    return path.join(PATH["file"], filename)

def get_image(filename: str) -> str:
    return path.join(PATH["image"], filename)

def get_sound(filename: str) -> str:
    return path.join(PATH["sound"], filename)
