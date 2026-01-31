"""
Camera view and scrolling strategies for pygame.

This module implements a small camera system and three scrolling strategies
using the Strategy pattern:

- CenteredCamera:   keeps the player centered (clamped to world bounds)
- AutoCamera:       moves the camera automatically in a given direction
- PagewiseCamera:   jumps page-wise once the player exits an inner "safe" rectangle

The classes are designed to be lightweight and easy to integrate with a
pygame-based 2D game.
"""

from __future__ import annotations  # forward references for type hints

import logging
from abc import ABC, abstractmethod
from typing import Optional

import pygame


class CamScroll(ABC):
    """Abstract base for camera scrolling strategies.

    A scrolling strategy receives references to the camera, the player rect,
    and the world/view rectangles and updates the camera's offset when
    :meth:`scroll` is called.

    Args:
        camera: The camera instance that owns the scrolling strategy.
        player: The player's rectangle in world coordinates (FRect for floats).
        rect_world: The world bounds (everything that can be shown).
        rect_view: The current visible area size (camera viewport size).
    """

    def __init__(
        self,
        camera: Camera,
        player: pygame.rect.FRect,
        rect_world: pygame.rect.FRect,
        rect_view: pygame.rect.FRect,
    ) -> None:
        super().__init__()
        self.camera = camera
        self.player = player
        self.rect_world = rect_world
        self.rect_view = rect_view

    @abstractmethod
    def scroll(self) -> None:
        """Update the camera offset.

        Implementations should modify ``self.camera.offset`` in place.
        """
        raise NotImplementedError
    

class CenteredCamera(CamScroll):
    """Scrolling strategy that keeps the player centered when possible.

    The camera tries to center on the player but is clamped to the world
    bounds so that the viewport never shows outside the world.
    """

    def __init__(
        self,
        camera: Camera,
        player: pygame.rect.FRect,
        rect_world: pygame.rect.FRect,
        rect_view: pygame.rect.FRect,
    ) -> None:
        super().__init__(camera, player, rect_world, rect_view)

    def scroll(self) -> None:
        """Center on the player and clamp to the world bounds."""
        # Compute desired top-left so the player is approximately in the center
        self.camera.offset.x = max(0, self.player.x - self.rect_view.width / 2)
        self.camera.offset.y = max(0, self.player.y - self.rect_view.height / 2)

        # Clamp right/bottom so we do not scroll past the world edges
        self.camera.offset.x = min(
            self.rect_world.right - self.rect_view.width, self.camera.offset.x
        )
        self.camera.offset.y = min(
            self.rect_world.bottom - self.rect_view.height, self.camera.offset.y
        )


class AutoCamera(CamScroll):
    """Scrolling strategy that moves the camera by a constant vector.

    This can be used for auto-scrolling levels (e.g., side scrollers).

    Args:
        direction: The per-tick offset added to the camera (world units/frame).
    """

    def __init__(
        self,
        camera: Camera,
        player: pygame.rect.FRect,
        direction: pygame.Vector2,
        rect_world: pygame.rect.FRect,
        rect_view: pygame.rect.FRect,
    ) -> None:
        super().__init__(camera, player, rect_world, rect_view)
        self.direction = direction

    def scroll(self) -> None:
        """Advance the camera by the configured direction vector."""
        # Note: No clamping here—some games want to allow scrolling past
        # the player. If needed, clamp like in CenteredCamera.scroll().
        self.camera.offset += self.direction 
        self.camera.offset.x = max(0, self.camera.offset.x)
        self.camera.offset.y = max(0, self.camera.offset.y)
        self.camera.offset.x = min(
            self.rect_world.right - self.rect_view.width, self.camera.offset.x
        )
        self.camera.offset.y = min(
            self.rect_world.bottom - self.rect_view.height, self.camera.offset.y
        )


class PagewiseCamera(CamScroll):
    """Scrolling strategy that jumps when leaving an inner safe rectangle.

    The camera remains fixed while the player moves inside an inner rectangle
    (the "safe area"). When the player exits this area, the camera jumps so
    that the player is centered again (clamped to world bounds).

    Args:
        inner: Half-size of the inner rectangle around the viewport center
            (Vector2 where x = half-width, y = half-height of the safe area).
    """

    def __init__(
        self,
        camera: Camera,
        player: pygame.rect.FRect,
        inner: pygame.Vector2,
        rect_world: pygame.rect.FRect,
        rect_view: pygame.rect.FRect,
    ) -> None:
        super().__init__(camera, player, rect_world, rect_view)
        self.inner = inner
        self.inner_rect = pygame.rect.FRect(self.rect_view.centerx - self.inner.x,
                                            self.rect_view.centery - self.inner.y,
                                            2 * self.inner.x,
                                            2 * self.inner.y)

    def scroll(self) -> None:
        """Jump the camera when the player exits the inner safe rectangle."""
        # Transform the player's rect into camera/view coordinates.
        player_in_view = self.camera.world2camera(self.player)

        # If the player leaves the safe area, re-center (with clamping).
        if not player_in_view.colliderect(self.inner_rect):
            self.camera.offset.x = max(0, self.player.x - self.rect_view.width / 2)
            self.camera.offset.y = max(0, self.player.y - self.rect_view.height / 2)
            self.camera.offset.x = min(
                self.rect_world.right - self.rect_view.width, self.camera.offset.x
            )
            self.camera.offset.y = min(
                self.rect_world.bottom - self.rect_view.height, self.camera.offset.y
            )



class Camera:
    """A minimal camera that tracks a 2D viewport in world space.

    The camera maintains an offset (top-left of the view in world coordinates)
    and a floating-point rectangle representing the current viewport.

    Args:
        size_view: Width and height of the viewport in pixels (floats allowed). 
    """

    def __init__(self, size_view: tuple[float, float]) -> None:
        # Offset of the viewport's top-left corner in world coordinates.
        self.offset = pygame.Vector2(0, 0)

        # Float-precision rectangle representing the viewport.
        self.rect = pygame.rect.FRect((0, 0), size_view)

        # The active scrolling strategy. Must be set via set_scroller().
        self.scroller: Optional[CamScroll] = None

    def set_scroller(self, scroller: CamScroll) -> None:
        """Assign the scrolling strategy to control this camera.

        Args:
            scroller: An instance implementing the scrolling behavior.
        """
        self.scroller = scroller

    def scroll(self) -> None:
        """Apply the currently set scrolling strategy and sync the viewport.

        The strategy updates :attr:`offset`. After that, the camera updates its
        :attr:`rect.topleft` accordingly.

        Logs:
            An error is logged if no scroller has been set.
        """
        if self.scroller is None:
            logging.error("No scroller set on camera.")
            return
        self.scroller.scroll()
        self.rect.topleft = self.offset

    def world2camera(self, rect: pygame.rect.FRect) -> pygame.rect.FRect:
        """Convert a world-space rectangle into camera/view coordinates.

        Args:
            rect: Rectangle in world coordinates.

        Returns:
            A new FRect positioned relative to the current camera offset.
        """
        return pygame.rect.FRect(rect.topleft - self.offset, rect.size)

    def camera2world(self, rect: pygame.rect.FRect) -> pygame.rect.FRect:
        """Convert a camera/view-space rectangle into world coordinates.

        Args:
            rect: Rectangle in camera/view coordinates.

        Returns:
            A new FRect positioned in world coordinates.
        """
        return pygame.rect.FRect(rect.topleft + self.offset, rect.size)
