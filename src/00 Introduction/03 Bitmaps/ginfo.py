import pygame


def main():
    pygame.init()
    screen=pygame.display.set_mode([200, 200])
    info = pygame.display.Info() #pygame.display.get_wm_info()
    pygame.display.message_box("Window System Information", repr(info), "info")
    pygame.quit()


if __name__ == "__main__":
    main()
