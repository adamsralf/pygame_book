from pygame import Rect

TITLE = "TicTacToe with State Machine"
WINDOW = Rect(0, 0, 480, 480)
PLAYGROUND = Rect(0, 0, 400, 400)
PLAYGROUND.center = WINDOW.center   
CELL_SIZE = PLAYGROUND.width // 3
COLORS = {
    'BG': (20, 20, 28),
    'TEXT': (235, 235, 245),
    'TITLE': (255, 220, 120),
    'GRID': (190, 190, 210),
    'PLAYGROUND': (32, 32, 46),
    'O': (238, 214, 130),
    'X': (238, 132, 146),
}

FPS = 60
