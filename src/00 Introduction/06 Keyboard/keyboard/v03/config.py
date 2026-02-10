import pygame

WINDOW = pygame.Rect((0, 0), (300, 300))
FPS = 60
DELTATIME = 1.0 / FPS
DIRECTIONS = {
    "stop": pygame.math.Vector2(0, 0),
    "right": pygame.math.Vector2(1, 0),
    "left": pygame.math.Vector2(-1, 0),
    "up": pygame.math.Vector2(0, -1),
    "down": pygame.math.Vector2(0, 1),
}
