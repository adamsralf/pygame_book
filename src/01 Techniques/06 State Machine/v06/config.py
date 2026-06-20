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

MSGSTRINGS = {}
MSGSTRINGS["start"] = {"headline": "Welcome to Tic Tac Toe!", 
                       "message": [
                                    "Place three of your symbols in one straight line to win.",
                                    "The line can be horizontal, vertical, or diagonal.",                                  "After each move, the other player takes a turn.",
                                    "",
                                    "Player 1:  X",
                                    "Player 2:  O",
                                    "",
                                    "Keys:",
                                    "SPACE    - start",
                                    "P        - pause",
                                    "H        - help",
                                    "ESC / Q  - quit",
                    ]
                }
MSGSTRINGS["win"] = {"headline": "Player Wins!", 
                     "message": [
                                  "Congratulations!",
                                  "You have won the game.",
                                  "",
                                  "Press Y to play again.",
                                  "Press N / Q / ESC to quit.",
                     ]
                 }
MSGSTRINGS["draw"] = {"headline": "It's a Draw!", 
                       "message": [
                                    "The game ended in a draw.",
                                    "",
                                    "Press Y to play again.",
                                    "Press N / Q / ESC to quit.",
                        ]
                    }

