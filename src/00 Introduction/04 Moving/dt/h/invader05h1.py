from statistics import fmean, median

import pygame
import pygame.time


class Settings:
    WINDOW = pygame.Rect((0, 0), (120, 650))
    FPS = 10  # 10 30 60 120 240 300 600
    LIMIT = 500
    DELTATIME = 1.0 / FPS


def main():
    pygame.init()
    window = pygame.Window(size=Settings.WINDOW.size, title="Movement", position=(10, 50))
    screen = window.get_surface()
    clock = pygame.time.Clock()

    defender_image = pygame.image.load("images/defender01.png").convert_alpha()
    defender_image = pygame.transform.scale(defender_image, (30, 30))
    defender_rect = pygame.FRect(defender_image.get_rect())
    result = {}
    for fps in range(10, 610, 10):
        Settings.FPS = fps
        Settings.DELTATIME = 1.0 / Settings.FPS
        messures = []
        for index in range(10):
            defender_rect.centerx = Settings.WINDOW.centerx
            defender_rect.bottom = Settings.WINDOW.bottom - 5
            defender_speed = 600
            defender_direction_v = -1

            clock.tick(Settings.FPS)
            start_time = pygame.time.get_ticks() 
            running = True
            while running:
                if pygame.time.get_ticks() > start_time + Settings.LIMIT:
                    defender_speed = 0
                    break
                # Events
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False

                # Update
                defender_rect.top += defender_direction_v * defender_speed * Settings.DELTATIME
                if defender_rect.bottom >= Settings.WINDOW.bottom:
                    defender_direction_v *= -1
                elif defender_rect.top <= 0:
                    defender_direction_v *= -1

                # Draw
                screen.fill("white")
                pygame.draw.line(screen, "red", (0, 315), (Settings.WINDOW.width, 315), 2)
                screen.blit(defender_image, defender_rect)
                window.flip()
                Settings.DELTATIME = clock.tick(Settings.FPS) / 1000.0
            messures.append(defender_rect.top)
            if fps in (10, 30, 60, 120, 240, 300, 600):
                pygame.image.save(screen, f"fps_05h_{Settings.FPS:03d}_{index:02d}.png")
        avg = fmean(messures)  
        med = median(messures) 
        mad = 0.0  
        for val in messures:
            mad += abs(val - 315)
        mad /= len(messures)
        messures.append(avg)
        messures.append(med)
        messures.append(mad)
        result[Settings.FPS] = messures
    with open("result_05h.txt", "w") as f:
        for key in result.keys():
            f.write(f"{key}")
            for i in range(len(result[key])):
                f.write(f" {result[key][i]}")
            f.write("\n")
    print(result)
    pygame.quit()


if __name__ == "__main__":
    main()
