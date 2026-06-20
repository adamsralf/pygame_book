import os
from typing import Dict

from pygame import FRect, Rect, Vector2

FPS = 60
DELTATIME = 1.0 / FPS
WINDOW: FRect = FRect(0, 0, 400, 400)
PATH: Dict[str, str] = {}
PATH["file"] = os.path.dirname(os.path.abspath(__file__))
PATH["image"] = os.path.join(PATH["file"], "images")

def get_file(filename: str) -> str:
    return os.path.join(PATH["file"], filename)

def get_image(filename: str) -> str:
    return os.path.join(PATH["image"], filename)

def get_sound(filename: str) -> str:
    return os.path.join(PATH["sound"], filename)    

def world2camera(rect: FRect|Rect|None, offset: Vector2) -> FRect:
    if rect is None:
        return FRect((0, 0), (0, 0))
    return FRect(rect.topleft - offset, rect.size)

def camera2world(rect: FRect|Rect|None, offset: Vector2) -> FRect:
    if rect is None:
        return FRect((0, 0), (0, 0))
    return FRect(rect.topleft + offset, rect.size)

