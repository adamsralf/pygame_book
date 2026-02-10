"""A simple desktop game implemented with Pygame.

Credits:
 * Fishtank image: https://www.pngwing.com/en/free-png-vadpk
 * Sound: https://www.fesliyanstudios.com/royalty-free-sound-effects-download
"""

import os
from math import sqrt
from random import randint
from time import time
from typing import Any, Dict, Tuple

import pygame


class Settings:
    WINDOW = pygame.Rect(0, 0, 1220, 1002)
    FPS = 60
    DELTATIME = 1.0 / FPS
    PATH: Dict[str, str] = {}
    PATH["file"] = os.path.dirname(os.path.abspath(__file__))
    PATH["image"] = os.path.join(PATH["file"], "images")
    PATH["sound"] = os.path.join(PATH["file"], "sounds")
    CAPTION = 'Bubbles'
    RADIUS = {"min": 15, "max": 240}
    DISTANCE = 50
    PLAYGROUND = pygame.Rect(90, 90, 1055, 615)
    MAX_BUBBLES = PLAYGROUND.height * PLAYGROUND.width // 10000
    BOX = pygame.Rect(90, 770, 1055, 1300)
    POINTS = 0

    @staticmethod
    def get_file(filename: str) -> str:
        """Full path of the file in the main path.

        Args:
            filename (str): Name of the file

        Returns:
            str: Absolute path with filename
        """
        return os.path.join(Settings.PATH["file"], filename)

    @staticmethod
    def get_image(filename: str) -> str:
        """Full path of the image file.

        Args:
            filename (str): Name of the file

        Returns:
            str: Absolute path with filename of the image file
        """
        return os.path.join(Settings.PATH["image"], filename)

    @staticmethod
    def get_sound(filename: str) -> str:
        """Full path of the sound file.

        Args:
            filename (str): Name of the file

        Returns:
            str: Absolute path with filename of the sound file
        """
        return os.path.join(Settings.PATH["sound"], filename)


class BubbleContainer:
    """A simple container class to manage the bubbles of different sizes."""

    def __init__(self, filename: str) -> None:
        """Constructor.

        Args:
            filename (str): Filename of the bubble picture file
        """
        imagename = Settings.get_image(filename)
        image: pygame.Surface = pygame.image.load(imagename).convert_alpha()
        self.images = {i: pygame.transform.scale(image, (i * 2, i * 2)) for i in range(Settings.RADIUS["min"], Settings.RADIUS["max"] + 1)}

    def get(self, radius: int) -> pygame.Surface:
        """Gets the bubble image with the radius <radius>.

        Args:
            radius (int): radius of the bubble

        Returns:
            pygame.Surface: Scaled image of the bubble
        """
        radius = max(Settings.RADIUS["min"], radius)
        radius = min(Settings.RADIUS["max"], radius)
        return self.images[radius]


class Timer:
    """Timer in order to check time periodes."""

    def __init__(self, duration: int, with_start: bool = True) -> None:
        """Constructor

        Args:
            duration (int): duration of the time interval in milli seconds
            with_start (bool, optional): Controls if the first period will count (True) or not (False). Defaults to True.
        """
        self.duration = duration
        if with_start:
            self.next = pygame.time.get_ticks()
        else:
            self.next = pygame.time.get_ticks() + self.duration

    def is_next_stop_reached(self) -> bool:
        """Checks if the end of a time period is reached or exceeded.

        Returns:
            bool: True if the end of the period is reached or exceeded; otherwise False
        """
        if pygame.time.get_ticks() > self.next:
            self.next = pygame.time.get_ticks() + self.duration
            return True
        return False


class Background(pygame.sprite.Sprite):
    """Sprite class with nearly no function for drawing the background image."""

    def __init__(self) -> None:
        """Constructor."""
        super().__init__()
        imagename = Settings.get_image("aquarium.png")
        self.image: pygame.Surface = pygame.image.load(imagename).convert()
        self.image = pygame.transform.scale(self.image, Settings.WINDOW.size)
        self.rect = self.image.get_rect()


class Message(pygame.sprite.Sprite):
    """Draws a shadow and a text in the foreground of the game."""

    def __init__(self, filename: str) -> None:
        super().__init__()
        imagename = Settings.get_image(filename)
        self.image: pygame.Surface = pygame.image.load(imagename).convert_alpha()
        self.rect = self.image.get_rect()


class Bubble(pygame.sprite.Sprite):
    """The sprite class of the bubble."""

    def __init__(self, speed: int) -> None:
        """Constructor."""
        super().__init__()
        self.mode = "blue"
        self.radius = Settings.RADIUS["min"]
        self.image = Game.BUBBLE_CONTAINER[self.mode].get(self.radius)
        self.rect: pygame.Rect = self.image.get_rect()
        self.fradius = float(self.radius)
        self.speed = speed

    def update(self, *args: Any, **kwargs: Any) -> None:
        """Let the bubble grow.

        Args:
            *args (Tuple[int]): not used
            **kwargs Dict[str, Any]: possible key/value pairs:
                                      (action/grow), (action/sting),
                                      (mode/blue), (mode/red))
        """
        if "action" in kwargs.keys():
            if kwargs["action"] == "grow":
                self.fradius += self.speed * Settings.DELTATIME
                self.fradius = min(self.fradius, Settings.RADIUS["max"])
                self.radius = round(self.fradius)
                center = self.rect.center
                self.image = Game.BUBBLE_CONTAINER[self.mode].get(self.radius)
                self.rect = self.image.get_rect()
                self.rect.center = center
            elif kwargs["action"] == "sting":
                self.stung()
        elif "mode" in kwargs.keys():
            self.set_mode(kwargs["mode"])

    def set_mode(self, mode: str) -> None:
        """Sets the bubble in the mode "red" or "blue".

        Args:
            mode (str): "red" oder "blue"
        """
        if mode != self.mode:
            self.mode = mode
            self.image = Game.BUBBLE_CONTAINER[self.mode].get(self.radius)

    def randompos(self) -> None:
        """Computes a new position of the center by random."""
        bubbledistance = Settings.DISTANCE + Settings.RADIUS["min"]
        centerx = randint(Settings.PLAYGROUND.left + bubbledistance, Settings.PLAYGROUND.right - bubbledistance)
        centery = randint(Settings.PLAYGROUND.top + bubbledistance, Settings.PLAYGROUND.bottom - bubbledistance)
        self.rect.center = (centerx, centery)

    def stung(self):
        """The bubble removes itself and the score increases."""
        self.kill()
        Settings.POINTS += self.radius


class Points(pygame.sprite.Sprite):
    """Class in order to generate a image of the score."""

    def __init__(self) -> None:
        """Constructor"""
        super().__init__()
        self.font = pygame.font.Font(pygame.font.get_default_font(), 18)
        self.oldpoints = -1

    def update(self, *args: Any, **kwargs: Any) -> None:
        """Let the bubble grow.

        Args:
            *args (Tuple[int]): not used
            **kwargs Dict[str, Any]: not used
        """
        if self.oldpoints != Settings.POINTS:
            self.image = self.font.render(f"Points: {Settings.POINTS}", True, "red")
            self.rect = self.image.get_rect()
            self.rect.left = Settings.BOX.left
            self.rect.top = Settings.BOX.top


class Game:
    """The class Game is main starting class of the game."""

    BUBBLE_CONTAINER: Dict[str, BubbleContainer] = {}
    SOUND_CONTAINER: Dict[str, pygame.mixer.Sound] = {}

    def __init__(self) -> None:
        """Constructor."""
        pygame.init()
        self.window = pygame.Window(size=Settings.WINDOW.size, title=Settings.CAPTION)
        self.screen = self.window.get_surface()
        self.clock = pygame.time.Clock()
        Game.BUBBLE_CONTAINER["blue"] = BubbleContainer("bubble1.png")
        Game.BUBBLE_CONTAINER["red"] = BubbleContainer("bubble2.png")
        Game.SOUND_CONTAINER["bubble"] = pygame.mixer.Sound(Settings.get_sound("plopp1.mp3"))  # §\label{srcBubble1302}§
        Game.SOUND_CONTAINER["burst"] = pygame.mixer.Sound(Settings.get_sound("burst.mp3"))
        Game.SOUND_CONTAINER["clash"] = pygame.mixer.Sound(Settings.get_sound("glas.wav"))
        self.background = pygame.sprite.GroupSingle(Background())
        self.all_sprites = pygame.sprite.Group()
        self.running = True
        self.pausing = False
        self.msgpause = Message("pause.png")
        self.msgrestart = Message("restart.png")

        self.restart()

    def watch_for_events(self) -> None:
        """Looking for any type of event and poke a reaction."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_p:
                    self.setpause()
                elif event.key == pygame.K_j:
                    self.do_start = True
                elif event.key == pygame.K_n:
                    self.running = False
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 3:
                    self.setpause()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # left
                    self.sting(pygame.mouse.get_pos())

    def draw(self) -> None:
        """Draws all sprite on the screen."""
        self.background.draw(self.screen)
        self.all_sprites.draw(self.screen)
        # pygame.draw.rect(self.screen, "red", Settings.playground, 2)
        # for b in self.all_bubbles:
        #     pygame.draw.rect(self.screen, "red", b.rect, 2)  # type: ignore
        self.window.flip()

    def update(self) -> None:
        """This method is responsible for the main game logic."""
        if self.do_start:
            self.restart()
        if not self.pausing and self.running:
            if self.check_bubblecollision():
                if not self.restarting:
                    Game.SOUND_CONTAINER["clash"].play()
                    self.all_sprites.add(self.msgrestart)
                    self.restarting = True
            else:
                self.all_sprites.update(action="grow")
                self.spawn_bubble()
            self.set_mousecursor()

    def restart(self):
        """Resets all attributes in order to start/restart the game."""
        Settings.POINTS = 0
        self.all_sprites.empty()
        self.all_sprites.add(Points())
        self.bubble_speed = 10
        self.timer_bubble = Timer(500, False)
        self.timer_bubble_speed = Timer(10000, False)
        self.do_start = False
        self.restarting = False

    def setpause(self):
        """Manages the pause mode."""
        if not self.pausing:
            self.all_sprites.add(self.msgpause)
        else:
            self.msgpause.kill()
        self.pausing = not self.pausing

    def spawn_bubble(self) -> None:
        """Spawns a new bubble and checks if there is enough space around the bubble."""
        if self.timer_bubble_speed.is_next_stop_reached():
            if self.bubble_speed < 100:
                self.bubble_speed += 5
        if self.timer_bubble.is_next_stop_reached():
            if len(self.all_sprites) <= Settings.MAX_BUBBLES:
                b = Bubble(self.bubble_speed)
                for _ in range(100):
                    b.randompos()
                    b.radius += Settings.DISTANCE
                    collided = pygame.sprite.spritecollide(b, self.all_sprites, False, pygame.sprite.collide_circle)
                    b.radius -= Settings.DISTANCE
                    if not collided:
                        self.all_sprites.add(b)
                        Game.SOUND_CONTAINER["bubble"].play()
                        break

    def collidepoint(self, point: Tuple[int, int], sprite: pygame.sprite.Sprite) -> bool:
        """Checks if a point is inside or on the edge of the circle.

        Args:
            point (Tuple[int, int]): Coordinates of the point
            sprite (pygame.sprite.Sprite): Sprite with self.radius attribute

        Returns:
            bool: True if the point is inside or on the edge; otherwise False
        """
        if hasattr(sprite, "radius"):
            deltax = point[0] - sprite.rect.centerx  # type: ignore
            deltay = point[1] - sprite.rect.centery  # type: ignore
            return sqrt(deltax * deltax + deltay * deltay) <= sprite.radius  # type: ignore
        return False

    def set_mousecursor(self) -> None:
        """Changes the mouse cursor depending if it is inside or on the edge of a bubble."""
        is_over = False
        pos = pygame.mouse.get_pos()
        for b in self.all_sprites:
            if self.collidepoint(pos, b):
                is_over = True
                break
        if is_over:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_CROSSHAIR)

    def sting(self, mousepos: Tuple[int, int]) -> None:
        """If the mouse position is inside a bubble, burst it."""
        for bubble in self.all_sprites:
            if self.collidepoint(mousepos, bubble):
                Game.SOUND_CONTAINER["burst"].play()
                bubble.update(action="sting")

    def check_bubblecollision(self) -> bool:
        """Checks if two bubbles collide or a bubble the playground border reaches.

        Returns:
            bool: True if bubbles or a bubble collides; otherwise False
        """
        for index1 in range(0, len(self.all_sprites) - 1):
            for index2 in range(index1 + 1, len(self.all_sprites)):
                bubble1 = self.all_sprites.sprites()[index1]
                bubble2 = self.all_sprites.sprites()[index2]
                if type(bubble1).__name__ == "Bubble" and type(bubble2).__name__ == "Bubble":
                    if pygame.sprite.collide_circle(bubble1, bubble2):
                        bubble1.update(mode="red")
                        bubble2.update(mode="red")
                        return True
                    if not Settings.PLAYGROUND.contains(bubble1):
                        bubble1.update(mode="red")
                        return True
                    if not Settings.PLAYGROUND.contains(bubble2):
                        bubble2.update(mode="red")
                        return True
        return False

    def run(self) -> None:
        """Starting point and main loop of the game."""
        time_previous = time()
        self.running = True
        while self.running:
            self.watch_for_events()
            self.update()
            self.draw()
            self.clock.tick(Settings.FPS)
            time_current = time()
            Settings.DELTATIME = time_current - time_previous
            time_previous = time_current
        pygame.quit()


def main():
    Game().run()


if __name__ == "__main__":
    main()
