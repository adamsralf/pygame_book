from math import ceil

import pygame

import config as cfg


class KeySprite(pygame.sprite.Sprite):
    def __init__(self, label: str, key: int, left: int, top: int) -> None:
        super().__init__()
        self.font = pygame.font.SysFont(None, 20)
        self.label = label
        self.key = key
        if label == 'Enter':
            factor_width = 2.0
        elif label == 'Tab' or label == 'Caps' or label == '<--' or label == 'Menu':
            factor_width = 1.5
        elif label == 'LShift':
            factor_width = 2.5
        elif label == 'RShift':
            factor_width = 2.0
        elif label == 'Space':
            factor_width = 10.0
        else:                                           # Normal key§\label{keyboard0201}§
            factor_width = 1.0
        factor_spacing = ceil(factor_width - 1)         # Used space§\label{keyboard0202}§ 
        width = int(factor_width * cfg.KEY['width'] + (factor_spacing * cfg.KEY['spacing']))
        self.image = pygame.Surface((width, cfg.KEY['height']))
        self.pressed = False
        self.rect = self.image.get_rect(topleft=(left, top))
        self.txt_surf = self.font.render(label, True, (255, 255, 255))
        self.txt_rect = self.txt_surf.get_rect()
        self.txt_rect.center = self.image.get_rect().center
        self.update()

    def update(self) -> None:
        if self.pressed:
            self.image.fill((200, 0, 0))
            self.image.blit(self.txt_surf, self.txt_rect)
        else:
            self.image.fill((100, 100, 100))
            self.image.blit(self.txt_surf, self.txt_rect)


class Game(object):

    def __init__(self) -> None:
        pygame.init()
        self.window = pygame.Window(size=cfg.WINDOW.size, title="Typewiter")
        self.screen = self.window.get_surface()
        self.clock = pygame.time.Clock()
        self.running = False
        self.all_sprites = pygame.sprite.Group()
        self.keyboard = self.generate_sprites()

    def run(self) -> None:
        self.running = True
        while self.running:
            self.watch_for_events()
            if self.running:
                self.update()
                self.draw()
                self.clock.tick(cfg.FPS)
        pygame.quit()

    def watch_for_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key in self.keyboard:
                    self.keyboard[event.key].pressed = True
            if event.type == pygame.KEYUP:
                if event.key in self.keyboard:
                    self.keyboard[event.key].pressed = False

    def update(self) -> None:
        self.all_sprites.update()

    def draw(self) -> None:
        self.screen.fill((30, 30, 30))
        self.all_sprites.draw(self.screen)
        self.window.flip()

    def label2key(self, label: str) -> int | None:
        specials = {
            'Space': pygame.K_SPACE,
            'Enter': pygame.K_RETURN,
            '<--': pygame.K_BACKSPACE,
            'Tab': pygame.K_TAB,
            'LShift': pygame.K_LSHIFT,
            'LCtrl': pygame.K_LCTRL,
            'RShift': pygame.K_RSHIFT,
            'RCtrl': pygame.K_RCTRL,
            'Alt': pygame.K_LALT,
            'Caps': pygame.K_CAPSLOCK,
            'Esc': pygame.K_ESCAPE,
        }
        for i in range(1, 13):
            specials[f'F{i}'] = getattr(pygame, f'K_F{i}')
        
        numpad = {
            'KP+': pygame.K_KP_PLUS,
            'KP-': pygame.K_KP_MINUS,
            'KP*': pygame.K_KP_MULTIPLY,
            'KP/': pygame.K_KP_DIVIDE,
        }
        for i in [0,1,2,3,4,5,6,7,8,9]:
            numpad[f'KP{i}'] = getattr(pygame, f'K_KP{i}')

        if label in specials:
            return specials[label]
        elif label in numpad:
            return numpad[label]
        try:
            return pygame.key.key_code(label.lower())   # Alphanumeric keys§\label{keyboard0205}§
        except Exception:
            return None

    def generate_sprites(self) -> dict[int, KeySprite]:
        keyboard = {}
        left = top = 2 * cfg.KEY['spacing']
        for row in cfg.ROWS:
            for label in row:
                key = self.label2key(label)             # Get pygame key constant§\label{keyboard0203}§
                if key is not None:
                    keysprite = KeySprite(label, key, left, top)
                    self.all_sprites.add(keysprite)
                    left += keysprite.rect.width + cfg.KEY['spacing']
                    keyboard[keysprite.key] = keysprite # Map key constant to sprite§\label{keyboard0204}§
            left = 2 * cfg.KEY['spacing']
            top += cfg.KEY['height'] + cfg.KEY['spacing']
        return keyboard


def main():
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
