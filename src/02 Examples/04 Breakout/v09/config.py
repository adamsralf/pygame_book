import os

import pygame

BRICK = {
    "rect": pygame.rect.Rect(0, 0, 98, 32),
    "dist": {"x": 3, "y": 3},
    "rows": 10,
    "cols": 10
}
BALLSIZE = BRICK["rect"].height
STATUSHEIGHT = 50
WINDOW = pygame.rect.Rect(0, 
                          0, 
                          BRICK["rect"].width * BRICK["cols"] + BRICK["dist"]["x"] * (BRICK["cols"] + 1)  , 
                          BRICK["rect"].height * BRICK["rows"] + BRICK["dist"]["y"] * (BRICK["rows"] - 1) + STATUSHEIGHT + 12*BALLSIZE)
FPS = 60
DELTATIME = 1.0 / FPS
CAPTION = "Breakout Clone"
POINTS = 0
LEVEL = 1
BALLS = 3

AUTOPILOT = False

PATH: dict[str, str] = {}
PATH["file"] = os.path.dirname(os.path.abspath(__file__))
PATH["image"] = os.path.join(PATH["file"], "images")
def get_image(filename: str) -> str:
    return os.path.join(PATH["image"], filename)

def get_file(directory: str, filename: str) -> str:
    return os.path.join(PATH[directory], filename)


