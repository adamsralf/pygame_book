import pygame

WINDOW = pygame.Rect((0, 0), (800, 600))
FPS = 60
DELTATIME = 1.0 / FPS
TITLE = "Working with Vector2: Collision Warning"
SHOW_VELOCITY = False
ROTATION_SPEED = 180            # Degrees per second
THRUST = 200                    # Pixels per second squared
MAX_SPEED = 600                 # Maximum spaceship speed in pixels per second
BULLET_SPEED = 250              # Bullet speed in pixels per second
COLLISION_WARNING_TIME = 2.0    # Prediction horizon in seconds§\label{asteroid0701}§


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
    "selected": "yellow",  
    "target_line": "brown",
    "collision_warning": "lightblue",  #§\label{asteroid0702}§
}
