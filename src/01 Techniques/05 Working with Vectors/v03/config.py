import pygame

WINDOW = pygame.Rect((0, 0), (800, 600))
FPS = 60
DELTATIME = 1.0 / FPS
TITLE = "Working with Vector2: Discrete Rotation"
SHOW_VELOCITY = False
ROTATION_SPEED = 15  # Degrees per second
THRUST = 200  # Pixels per second squared

# Print-friendly colors: white background and dark, unfilled outlines.
MYCOLORS = {
    "background": "white",
    "asteroid": (125, 125, 125),
    "velocity": "red",
    "spaceship": (0, 65, 180),
    "particle_start": (190, 100, 0),
    "particle_end": (225, 185, 110),
}
