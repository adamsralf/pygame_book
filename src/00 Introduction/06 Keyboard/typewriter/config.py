import pygame

WINDOW = pygame.rect.Rect((0, 0), (1035, 345))
FPS = 30

ROWS = [
    ['Esc'] + [f'F{i}' for i in range(1, 13)],
    ['`','1','2','3','4','5','6','7','8','9','0','-','=','<--', 'KP7','KP8','KP9','KP/'],
    ['Tab','Q','W','E','R','T','Y','U','I','O','P','[',']','\\', 'KP4','KP5','KP6','KP*'],
    ['Caps','A','S','D','F','G','H','J','K','L',';','\'','Enter', 'KP1','KP2','KP3','KP-'],
    ['LShift','Z','X','C','V','B','N','M',',','.','/','RShift', 'KP0','KP0','.','KP+'],
    ['LCtrl','Win','Alt','Space','AltGr','Menu','RCtrl']
]

KEY = {'width': 50, 'height': 50, 'spacing': 5}
