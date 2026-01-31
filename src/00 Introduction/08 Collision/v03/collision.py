import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill((50, 200, 50))
        self.rect = self.image.get_rect(center=pos)

    def update(self, keys):
        speed = 4
        if keys[pygame.K_LEFT]:
            self.rect.x -= speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += speed
        if keys[pygame.K_UP]:
            self.rect.y -= speed
        if keys[pygame.K_DOWN]:
            self.rect.y += speed


class Block(pygame.sprite.Sprite):
    def __init__(self, pos, color=(200, 50, 50)):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(color)
        self.rect = self.image.get_rect(center=pos)


def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    clock = pygame.time.Clock()

    player = Player((320, 240))
    blocks = pygame.sprite.Group()
    for x in range(100, 541, 80):
        for y in (120, 200, 280):
            blocks.add(Block((x, y)))

    all_sprites = pygame.sprite.Group(player, *blocks.sprites())

    font = pygame.font.SysFont(None, 24)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        keys = pygame.key.get_pressed()
        player.update(keys)

        pygame.sprite.spritecollide(player, blocks, True)   # spritecollide(sprite, group, dokill)§\label{srcCollision05a}§

        screen.fill((30, 30, 30))
        all_sprites.draw(screen)
        text = font.render(f"Blocks remaining: {len(blocks)}", True, (200, 200, 200))
        screen.blit(text, (10, 10))

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
