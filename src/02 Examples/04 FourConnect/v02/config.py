import pygame

FPS = 60
DELTATIME = 1.0/FPS

MARGIN = 5          # §\label{srcV01Config00}§
COIN_RADIUS = 50    # §\label{srcV01Config01}§
NOF_COLS = 7        # §\label{srcV01Config02}§
NOF_ROWS = 6        # §\label{srcV01Config03}§
TITLE_BAR = pygame.Rect(MARGIN, MARGIN, NOF_COLS * COIN_RADIUS * 2, 50)             # §\label{srcV01Config05}§
PLAYGROUND = pygame.Rect(MARGIN, TITLE_BAR.bottom + 2*(MARGIN + COIN_RADIUS),       # §\label{srcV01Config05}§
                         NOF_COLS * COIN_RADIUS * 2, NOF_ROWS * COIN_RADIUS * 2)  
LETTER_BAR = pygame.Rect(MARGIN, PLAYGROUND.bottom + MARGIN, PLAYGROUND.width, 20)  # §\label{srcV01Config06}§
STATUS_BAR = pygame.Rect(MARGIN, LETTER_BAR.bottom + MARGIN, PLAYGROUND.width, 100) # §\label{srcV01Config07}§
WINDOW = pygame.Rect(0, 0, 2 * MARGIN + PLAYGROUND.width, STATUS_BAR.bottom+MARGIN) # §\label{srcV01Config08}§

COLOR = {                                                                           # §\label{srcV01Config09}§
    "BG": (245, 246, 250),

    # Title
    "TITLE_BG": (220, 224, 238),
    "TITLE_TEXT": (38, 44, 60),

    # Playground
    "PLAYGROUND_BG": (87, 112, 163),
    "PLAYGROUND_HOLE": (0, 0, 0, 0),

    # Players
    "PLAYER1": (224, 94, 94),
    "PLAYER2": (242, 196, 82),

    # Letters
    "LETTER_BG": (0, 0, 0, 0),
    "LETTER_TEXT": (38, 44, 60),

    # Status Bar
    "STATUS_BG": (87, 112, 163),
    "STATUS_TEXT": (40, 48, 68),
}



