import os
from typing import TypedDict

import pygame


class Message(TypedDict):
    headline: str
    message: list[str]


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
PATH["image"] = os.path.join(PATH["file"], "assets", "images")
def get_image(filename: str) -> str:
    return os.path.join(PATH["image"], filename)

def get_file(directory: str, filename: str) -> str:
    return os.path.join(PATH[directory], filename)


MSGSTRINGS: dict[str, Message] = {
    "start": {
        "headline": "BREAKOUT",
        "message": [
            "Break all bricks to advance to the next level.",
            "Keep the ball in play with the paddle.",
            "",
            "SPACE - start / launch the ball",
            "Arrow keys - move the paddle",
            "P - pause     H - help",
            "F2 - toggle autopilot",
            "ESC / Q - quit",
        ],
    },
    "pause": {
        "headline": "Paused",
        "message": [
            "The game is paused.",
            "",
            "P or SPACE - resume",
            "H - help",
            "ESC / Q - quit",
        ],
    },
    "help": {
        "headline": "How to play",
        "message": [
            "Use the paddle to bounce the ball into the bricks.",
            "Clear every brick to advance to the next level.",
            "You have three balls; don't let the ball fall.",
            "",
            "SPACE - launch the ball",
            "Arrow keys - move the paddle",
            "P - pause     F2 - toggle autopilot",
            "H - return     ESC / Q - quit",
        ],
    },
    "gameover": {
        "headline": "Game Over",
        "message": [
            "You have lost all your balls.",
            "",
            "Y - start a new game",
            "N - quit",
        ],
    },
}
