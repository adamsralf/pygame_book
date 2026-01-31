"""
Demo and test harness for the camera and scrolling strategies.

This module boots a small pygame application that visualizes:
- A tiled world (grayscale gradient towards the center)
- A player sprite that can be moved with arrow keys
- Three camera views, each with a different scrolling strategy:
  1) CenteredCamera   -> keeps the player centered, clamped to the world
  2) AutoCamera       -> moves the camera automatically by a constant vector
  3) PagewiseCamera   -> jumps once the player exits an inner safe rectangle

Windows:
- Main/plain:             the full world region at 1:1 within the window size
- Birdeye:                scaled-down world with overlays of the three camera rects
- Centered/Auto/Pagewise: individual viewports driven by their strategies
"""

from time import time
from typing import Any, Union

import pygame
from cameraview import AutoCamera, Camera, CenteredCamera, PagewiseCamera


class Settings:
    """Static configuration for timing, world size, and window layout.

    Attributes:
        FPS: Target frames per second for the game loop.
        DELTATIME: Frame delta in seconds (updated each frame).
        TILESIZE_WORLD: Size of a single world tile in pixels.
        TILESIZE_BIRD:  Size of one tile in the bird's-eye view (unused here).
        NOF_COLS/NOF_ROWS: Grid size of the world in tiles.
        WORLD: Rect describing the full world bounds (in pixels).
        WINDOW: Rect describing the size of each viewport window.
        TILE_WITH_BORDER: Draw Rectangle around the tile (0=no border, >0 bordersize)
    """

    FPS = 60
    DELTATIME = 1.0 / FPS
    TILESIZE_WORLD = pygame.Vector2(24, 24)
    TILESIZE_BIRD = pygame.Vector2(4, 4)
    NOF_COLS = 90
    NOF_ROWS = 70
    WORLD : pygame.rect.FRect = pygame.rect.FRect(
        0, 0, NOF_COLS * TILESIZE_WORLD.y, NOF_ROWS * TILESIZE_WORLD.y
    )
    WINDOW : pygame.rect.FRect = pygame.rect.FRect(
        0, 0, NOF_COLS * TILESIZE_WORLD.x // 4, NOF_ROWS * TILESIZE_WORLD.y // 4
    )
    TILE_WITH_BORDER = 0


class Tile(pygame.sprite.Sprite):
    """A single world tile, shaded by distance to the world center."""

    def __init__(self, position: tuple[float, float]) -> None:
        """Create the tile sprite at a given world position (top-left).

        The fill color is a grayscale value brighter near the world center,
        darker near the edges. This helps visually distinguish camera motion.
        """
        super().__init__()
        self.image = pygame.Surface(Settings.TILESIZE_WORLD)

        # Compute a grayscale value based on distance to the world center.
        v1 = pygame.Vector2(position)
        v2 = pygame.Vector2(Settings.WORLD.center)
        distance = v2.distance_to(v1)
        max_distance = v2.length()
        rel_dist_center = min(1.0, distance / max_distance)
        gray_value = int(255 * (1 - rel_dist_center))
        self.image.fill([gray_value] * 3)
        if Settings.TILE_WITH_BORDER > 0:
            pygame.draw.rect(self.image, "Black", ((0,0), Settings.TILESIZE_WORLD), Settings.TILE_WITH_BORDER)

        # Store integer pixel rect for sprite batching.
        self.rect = self.image.get_rect(topleft=position)


class Player(pygame.sprite.Sprite):
    """The controllable player sprite (a red circle)."""

    def __init__(self, position: tuple[float, float]) -> None:
        """Create the player centered at the given world position."""
        super().__init__()
        self.image : pygame.surface.Surface = pygame.surface.Surface(Settings.TILESIZE_WORLD)
        self.image.set_colorkey((0, 0, 0))

        # Draw a simple red disc.
        self.radius = int(Settings.TILESIZE_WORLD.x // 2)
        pygame.draw.circle(self.image, (255, 0, 0), (self.radius, self.radius), self.radius)

        # Player world-rect (integer precision is fine for drawing).
        self.rect : pygame.rect.FRect = self.image.get_frect(center=position)

        # Movement configuration.
        self.speed = 400.0  # pixels per second
        self.directions = {
            "left": pygame.Vector2(-1, 0),
            "right": pygame.Vector2(1, 0),
            "up": pygame.Vector2(0, -1),
            "down": pygame.Vector2(0, 1),
            "stop": pygame.Vector2(0, 0),
        }
        self.direction = self.directions["stop"]

    def update(self, *args: Any, **kwargs: Any) -> None:
        """Advance the player based on current direction and clamp to world.

        Kwargs (optional):
            position: If provided, hard-sets the player's center position.
            move:     One of {"up","down","left","right","stop"} to change
                      the current movement direction for subsequent frames.
        """
        # Allow external callers to override position and direction.
        if "position" in kwargs:
            self.rect.center = kwargs["position"]
        if "move" in kwargs:
            self.direction = self.directions[kwargs["move"]]

        # Integrate movement using current DELTATIME.
        new_position = pygame.Vector2(self.rect.center) + self.direction * (
            self.speed * Settings.DELTATIME
        )
        self.rect.center = new_position

        # Prevent leaving the world bounds.
        self.rect.clamp_ip(Settings.WORLD)

        # Let Sprite subclasses hook into pygame internals if needed.
        return super().update(*args, **kwargs)


class Game:
    """Top-level pygame application that runs the camera demo."""

    def __init__(self) -> None:
        """Initialize pygame, build the world, and create all windows."""
        pygame.init()
        self.clock = pygame.time.Clock()

        # World content (tiles + player).
        self.tiles = pygame.sprite.Group()
        self.create_plain()
        self.player = Player(Settings.WORLD.center)

        # Windows and cameras.
        self.create_window_birdeye()
        self.create_follow()
        self.create_auto()
        self.create_pagewise()

        self.running = True

    def run(self) -> None:
        """Main loop: handle events, update, render, and maintain FPS."""
        time_previous = time()
        while self.running:
            self.watch_for_events()
            if self.running:
                self.update()
                self.draw()
                self.clock.tick(Settings.FPS)

                # Update global DELTATIME with actual frame time.
                time_current = time()
                Settings.DELTATIME = time_current - time_previous
                time_previous = time_current
        pygame.quit()

    def watch_for_events(self) -> None:
        """Process OS/window events and keyboard input for movement/quit."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.WINDOWCLOSE:
                # When a sub-window closes, shut down gracefully.
                self.running = False
                event.window.destroy()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_UP:
                    self.player.update(move="up")
                elif event.key == pygame.K_DOWN:
                    self.player.update(move="down")
                elif event.key == pygame.K_LEFT:
                    self.player.update(move="left")
                elif event.key == pygame.K_RIGHT:
                    self.player.update(move="right")

            elif event.type == pygame.KEYUP:
                if event.key in (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT):
                    self.player.update(move="stop")

    def update(self) -> None:
        """Update player and advance all cameras by their strategies."""
        self.window_main.title = f"Camera View - FPS: {self.clock.get_fps():.0f}"
        self.player.update()
        self.camera_follow.scroll()
        self.camera_auto.scroll()
        self.camera_pagewise.scroll()

    def draw(self) -> None:
        """Draw all windows in order (plain, bird's-eye, and strategy views)."""
        self.draw_window_plain()
        self.draw_window_birdeye()
        self.draw_window_follow()
        self.draw_window_auto()
        self.draw_window_pagewise()
        self.window_main.flip()

    def create_plain(self) -> None:
        """Create the main/plain window and build the tiled world."""
        self.window_main = pygame.Window(size=Settings.WINDOW.size, title="Plain Camera View")
        self.window_main.position = (0, 30)
        self.screen_main : pygame.surface.Surface = self.window_main.get_surface()

        # Fill the world sprite group with tiles laid out on a grid.
        for row in range(Settings.NOF_ROWS):
            for col in range(Settings.NOF_COLS):
                self.tiles.add(
                    Tile((col * Settings.TILESIZE_WORLD.x, row * Settings.TILESIZE_WORLD.y))
                )

    def create_follow(self) -> None:
        """Create the Follow camera/window pair."""
        self.camera_follow = Camera(Settings.WINDOW.size)
        self.camera_follow.set_scroller(
            CenteredCamera(self.camera_follow, self.player.rect, Settings.WORLD, Settings.WINDOW)
        )
        self.window_follow = pygame.Window(size=Settings.WINDOW.size, title="Player Centered Camera View")
        self.window_follow.position = (Settings.WINDOW.width + 10, 30)
        self.screen_follow = self.window_follow.get_surface()

    def create_auto(self) -> None:
        """Create the Auto camera/window pair with a constant scroll vector."""
        self.camera_auto = Camera(Settings.WINDOW.size)
        self.camera_auto.set_scroller(
            AutoCamera(self.camera_auto, self.player.rect, pygame.Vector2(1, 1), Settings.WORLD, Settings.WINDOW)
        )
        self.window_auto = pygame.Window(size=Settings.WINDOW.size, title="Auto Camera View")
        self.window_auto.position = (2 * (Settings.WINDOW.width + 10), 30)
        self.screen_auto : pygame.surface.Surface = self.window_auto.get_surface()

    def create_pagewise(self) -> None:
        """Create the Pagewise camera/window pair with the inner safe area."""
        self.camera_pagewise = Camera(Settings.WINDOW.size)
        self.camera_pagewise.set_scroller(
            PagewiseCamera(
                self.camera_pagewise,
                self.player.rect,
                pygame.Vector2(200, 150),
                Settings.WORLD,
                Settings.WINDOW,
            )
        )
        self.window_pagewise = pygame.Window(
            size=Settings.WINDOW.size, title="Pagewise Camera View"
        )
        self.window_pagewise.position = (1 * (Settings.WINDOW.width + 10), Settings.WINDOW.height + 60)
        self.screen_pagewise : pygame.surface.Surface = self.window_pagewise.get_surface()

    def create_window_birdeye(self) -> None:
        """Create the bird's-eye window and compute a world→screen zoom factor."""
        zx = Settings.WINDOW.width / Settings.WORLD.width
        zy = Settings.WINDOW.height / Settings.WORLD.height
        self.zoom = pygame.Vector2(zx, zy)
        self.window_birdeye = pygame.Window(
            size=Settings.WINDOW.size, title="Birdeye Camera View"
        )
        self.window_birdeye.position = (0, Settings.WINDOW.height + 60)
        self.screen_birdeye : pygame.surface.Surface = self.window_birdeye.get_surface()

    def draw_window_plain(self) -> None:
        """Render the full world into the main window, then the player."""
        self.tiles.draw(self.screen_main)
        pygame.draw.rect(self.screen_main, "yellow", self.screen_main.get_rect(), 5)
        self.screen_main.blit(self.player.image, self.player.rect)

    def draw_window_birdeye(self) -> None:
        """Render the scaled-down world plus overlays of the camera views."""
        # Draw scaled tiles and player (world -> birdeye transform).
        for sprite in self.tiles:
            image = pygame.transform.scale_by(sprite.image, self.zoom)
            self.screen_birdeye.blit(image, self.zoom_rect(sprite.rect))
        image = pygame.transform.scale_by(self.player.image, self.zoom)
        self.screen_birdeye.blit(image, self.zoom_rect(self.player.rect))

        # Outline the plain window view (yellow) in bird's-eye coordinates.
        pygame.draw.rect(self.screen_birdeye, "yellow", self.zoom_rect(Settings.WINDOW), 2)

        # Follow camera rectangle (red).
        pygame.draw.rect(self.screen_birdeye, "red", self.zoom_rect(self.camera_follow.rect), 2)

        # Pagewise camera rectangle (green) + its inner safe rectangle (dark green).
        inner_rect = self.camera_pagewise.camera2world(self.camera_pagewise.scroller.inner_rect)
        pygame.draw.rect(self.screen_birdeye, "darkgreen", self.zoom_rect(inner_rect), 2)
        pygame.draw.rect(self.screen_birdeye, "green", self.zoom_rect(self.camera_pagewise.rect), 2)

        # Auto camera rectangle (blue).
        pygame.draw.rect(self.screen_birdeye, "blue", self.zoom_rect(self.camera_auto.rect), 2)

        self.window_birdeye.flip()

    def draw_window_follow(self) -> None:
        """Render the Follow camera view: visible tiles and player."""
        lefttop = f"({self.player.rect.left:.0f},{self.player.rect.top:.0f})"
        offset = f"({self.camera_follow.offset.x:.0f},{self.camera_follow.offset.y:.0f})"
        self.window_follow.title = (f"Follow with Player={lefttop} and offset={offset}")

        sprites = self.get_visible_sprites(self.camera_follow)
        for sprite in sprites:
            self.screen_follow.blit(sprite.image, self.camera_follow.world2camera(sprite.rect))

        # Draw the player relative to the camera.
        self.screen_follow.blit(self.player.image, self.camera_follow.world2camera(self.player.rect))
        pygame.draw.rect(self.screen_follow, "red", self.screen_follow.get_rect(), 5)
        self.window_follow.flip()

    def draw_window_auto(self) -> None:
        """Render the Auto camera view: visible tiles and player."""
        lefttop = f"({self.player.rect.left:.0f},{self.player.rect.top:.0f})"
        offset = f"({self.camera_auto.offset.x:.0f},{self.camera_auto.offset.y:.0f})"
        self.window_auto.title = (
            f"Auto with Player={lefttop} and offset={offset}"
        )
        sprites = self.get_visible_sprites(self.camera_auto)
        for sprite in sprites:
            self.screen_auto.blit(sprite.image, self.camera_auto.world2camera(sprite.rect))
        self.screen_auto.blit(self.player.image, self.camera_auto.world2camera(self.player.rect))
        pygame.draw.rect(self.screen_auto, "blue", self.screen_auto.get_rect(), 5)
        self.window_auto.flip()

    def draw_window_pagewise(self) -> None:
        """Render the Pagewise camera view: visible tiles and player."""
        lefttop = f"({self.player.rect.left:.0f},{self.player.rect.top:.0f})"
        offset = f"({self.camera_pagewise.offset.x:.0f},{self.camera_pagewise.offset.y:.0f})"
        self.window_pagewise.title = (f"Pagewise with Player={lefttop} and offset={offset}")
        sprites = self.get_visible_sprites(self.camera_pagewise)
        for sprite in sprites:
            self.screen_pagewise.blit(sprite.image, self.camera_pagewise.world2camera(sprite.rect))
        self.screen_pagewise.blit(self.player.image, self.camera_pagewise.world2camera(self.player.rect))
        pygame.draw.rect(self.screen_pagewise, "green", self.screen_pagewise.get_rect(), 5)
        self.window_pagewise.flip()

    def zoom_rect(self, rect: Union[pygame.rect.Rect, pygame.rect.FRect]) -> pygame.rect.FRect:
        """Scale a world-space rect into bird's-eye view coordinates.

        Args:
            rect: Rectangle in world coordinates.

        Returns:
            A new FRect scaled by the current bird's-eye zoom factor.
        """
        x = rect.x * self.zoom.x
        y = rect.y * self.zoom.y
        w = rect.w * self.zoom.x
        h = rect.h * self.zoom.y
        return pygame.rect.FRect(x, y, w, h)
    
    def get_visible_sprites(self, camera: Camera) -> list[pygame.sprite.Sprite]:
        """Return a list of all world sprites currently visible in a camera view.

        This function filters the game's tile sprites and returns only those whose
        world rectangles intersect with the camera's viewport rectangle.
        This makes drawing faster because only visible tiles are blitted.

        Args:
            camera: The Camera instance whose view area should be checked.

        Returns:
            A list of pygame.sprite.Sprite objects (tiles) that are inside or
            partially inside the camera's visible area.
        """
        # Filter the tile sprites that are within or intersecting the camera rect
        visible = [sprite for sprite in self.tiles.sprites() if camera.rect.colliderect(sprite.rect)]

        # (Optional) Could be cached or spatially optimized for large maps
        return visible

def main() -> None:
    """Entrypoint: construct and run the Game."""
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
