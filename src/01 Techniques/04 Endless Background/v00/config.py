import os
from typing import Dict

from pygame import FRect, Vector2

FPS = 600
DELTATIME = 1.0 / FPS
TILESIZE_WORLD = Vector2(24, 24)
TILESIZE_WINDOW = Vector2(6, 6) 
NOF_COLS = 180
NOF_ROWS = 30
WORLD: FRect = FRect(0, 0, NOF_COLS * TILESIZE_WORLD.y, NOF_ROWS * TILESIZE_WORLD.y) 
WINDOW: FRect = FRect(0, 0, NOF_COLS * TILESIZE_WINDOW.x, NOF_ROWS * TILESIZE_WINDOW.y)
TILE_WITH_BORDER = 0
NOF_MOBS = 50
ZOOM_BIRDEYE = Vector2(TILESIZE_WINDOW.elementwise() / TILESIZE_WORLD)
PATH: Dict[str, str] = {}
PATH["file"] = os.path.dirname(os.path.abspath(__file__))
PATH["image"] = os.path.join(PATH["file"], "images")
PATH["sound"] = os.path.join(PATH["file"], "sounds")

def get_file(filename: str) -> str:
    return os.path.join(PATH["file"], filename)

def get_image(filename: str) -> str:
    return os.path.join(PATH["image"], filename)

def get_sound(filename: str) -> str:
    return os.path.join(PATH["sound"], filename)    