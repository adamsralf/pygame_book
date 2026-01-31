import sys

import pygame

WINDOW = pygame.rect.Rect(0, 0, 600, 800)
FPS = 60
DELTATIME = 1.0 / FPS 
HORIZONT = 50
# Physical constants (Moon conditions)
MOON_GRAVITY = 1.62                         # m/s²
EARTH_GRAVITY = 9.81                        # m/s²
PIXELS_PER_METER = 10                       # Scaling 1m = 10px
GRAVITY = MOON_GRAVITY * PIXELS_PER_METER   # = 16.2 px/s²
THRUST = -3 * PIXELS_PER_METER              # = 30.0 px/s²
LEVEL = {"easy":sys.maxsize, "fair":500, "hard":450, "ai":380} # §\label{moonlander0602}