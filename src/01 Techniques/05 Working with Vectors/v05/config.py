import pygame

WINDOW = pygame.Rect((0, 0), (800, 600))
FPS = 60
DELTATIME = 1.0 / FPS
TITLE = "Working with Vector2: A Drifting Asteroid"
SHOW_VELOCITY = False
ROTATION_SPEED = 180            # Degrees per second
THRUST = 200                    # Pixels per second squared
MAX_SPEED = 600                 # Maximum spaceship speed in pixels per second§\label{asteroid0501}§
BULLET_SPEED = 250              # Bullet speed in pixels per second§\label{asteroid0502}§


# Print-friendly colors: white background and dark, unfilled outlines.
MYCOLORS = {
    "background": "white",
    "asteroid": (125, 125, 125),
    "velocity": "red",
    "spaceship": (0, 65, 180),
    "spaceship_stop": (0, 125, 45),
    "bullet": (210, 0, 35),
    "particle_start": (190, 100, 0),
    "particle_end": (225, 185, 110),
}
