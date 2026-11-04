import pygame

WINDOW = pygame.Rect((0, 0), (800, 600))
FPS = 60
DELTATIME = 1.0 / FPS
TITLE = "Working with Vector2: Reflection at Slanted Walls"  
SHOW_VELOCITY = False
ROTATION_SPEED = 180            # Degrees per second
THRUST = 200                    # Pixels per second squared
MAX_SPEED = 600                 # Maximum spaceship speed in pixels per second
BULLET_SPEED = 250              # Bullet speed in pixels per second
COLLISION_WARNING_TIME = 2.0    # Prediction horizon in seconds
WALL_SEGMENTS = [((140, 160), (360, 80)), ((470, 100), (680, 260)),  #§\label{asteroid0902}§
                 ((120, 420), (340, 520)), ((490, 500), (710, 370))]  
BOUNCE_DISPLAY_TIME = 0.8       # Seconds to show the vectors after a reflection.§\label{asteroid0903}§


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
    "collision_warning": "lightblue",  
    "collision_prediction": "magenta", 
    "wall": (50, 50, 50),  # §\label{asteroid0901}§
    "wall_normal": "blue",
    "bounce_incoming": "orange",
    "bounce_normal": "blue",
    "bounce_tangent": "green",
    "bounce_outgoing": "magenta",
}
