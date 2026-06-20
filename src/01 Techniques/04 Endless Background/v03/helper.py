class Landscape(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        self.image = pygame.Surface(cfg.WINDOW.size, pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self._create_gradient_background()
        pygame.image.save(self.image, "backgroundtile.png")
        
    def _create_gradient_background(self) -> None:
        width, height = self.image.get_size()
        horizontal = pygame.Surface((width, height), pygame.SRCALPHA)
        vertical = pygame.Surface((width, height), pygame.SRCALPHA)

        for x in range(width):
            if x < width / 2:
                t = x / (width / 2)
                color = self._lerp_color((255, 255, 0), (255, 255, 255), t)
            else:
                t = (x - width / 2) / (width / 2)
                color = self._lerp_color((255, 255, 255), (255, 255, 0), t)
            pygame.draw.line(horizontal, color, (x, 0), (x, height))

        for y in range(height):
            if y < height / 2:
                t = y / (height / 2)
                color = self._lerp_color((0, 0, 255), (255, 255, 255), t)
            else:
                t = (y - height / 2) / (height / 2)
                color = self._lerp_color((255, 255, 255), (0, 0, 255), t)
            pygame.draw.line(vertical, color, (0, y), (width, y))

        self.image.blit(horizontal, (0, 0))
        vertical.set_alpha(160)
        self.image.blit(vertical, (0, 0))

    @staticmethod
    def _lerp_color(first: tuple[int, int, int], second: tuple[int, int, int], t: float) -> tuple[int, int, int]:
        return tuple(
            round(first[i] + (second[i] - first[i]) * min(max(t, 0.0), 1.0))
            for i in range(3)
        )