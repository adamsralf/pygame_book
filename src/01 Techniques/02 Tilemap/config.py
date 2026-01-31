import pygame

FPS = 60
DELTATIME = 1.0 / FPS
TILESIZE = pygame.math.Vector2(32, 32)
TILEMAP_NOF_COLS = 16
TILEMAP_NOF_ROWS = 12
TILEMAP_WINDOW = pygame.rect.Rect(0, 0, 
                                  TILEMAP_NOF_COLS * TILESIZE.x, 
                                  TILEMAP_NOF_ROWS * TILESIZE.y)
