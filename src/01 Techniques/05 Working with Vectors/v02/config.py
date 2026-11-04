import pygame

WINDOW = pygame.Rect((0, 0), (800, 600))
FPS = 60
DELTATIME = 1.0 / FPS
TITLE = "Working with Vector2: Velocity vector"
SHOW_VELOCITY = False

# Print-friendly colors: white background and dark, unfilled outlines.
MYCOLORS = {
    "background": "white",
    "asteroid": (125, 125, 125),
    "velocity": "red",
}
