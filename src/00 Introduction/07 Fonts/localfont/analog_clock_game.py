import pygame
import time
import os

# Constants
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 500
FPS = 60
CLOCK_RADIUS = 200
CLOCK_CENTER = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)  

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

def load_high_score():
    if os.path.exists("highscore.txt"):
        with open("highscore.txt", "r") as f:
            try:
                return int(f.read().strip())
            except ValueError:
                return 0
    return 0

def save_high_score(high_score):
    with open("highscore.txt", "w") as f:
        f.write(str(high_score))

def draw_clock(screen, center, radius):
    # Draw clock face
    pygame.draw.circle(screen, WHITE, center, radius, 2)
    clock_font = pygame.font.SysFont(None, 36)
    # Draw hour markers and numbers
    for i in range(12):
        angle = i * 30  # 360 / 12
        rad_angle = pygame.math.Vector2(0, -radius + 20).rotate(angle)
        start_pos = (center[0] + rad_angle.x, center[1] + rad_angle.y)
        rad_angle2 = pygame.math.Vector2(0, -radius + 10).rotate(angle)
        end_pos = (center[0] + rad_angle2.x, center[1] + rad_angle2.y)
        pygame.draw.line(screen, BLACK, start_pos, end_pos, 3)
        # Draw hour number
        hour_num = 12 if i == 0 else i
        text = clock_font.render(str(hour_num), True, BLACK)
        rad_angle3 = pygame.math.Vector2(0, -radius + 40).rotate(angle)
        text_pos = (center[0] + rad_angle3.x - text.get_width() // 2, center[1] + rad_angle3.y - text.get_height() // 2)
        screen.blit(text, text_pos)
    # Get current time
    current_time = time.localtime()
    hours = current_time.tm_hour % 12
    minutes = current_time.tm_min
    seconds = current_time.tm_sec
    # Draw hour hand
    hour_angle = (hours * 30) + (minutes * 0.5)
    hour_rad = pygame.math.Vector2(0, -radius * 0.5).rotate(hour_angle)
    pygame.draw.line(screen, BLACK, center, (center[0] + hour_rad.x, center[1] + hour_rad.y), 6)
    # Draw minute hand
    minute_angle = minutes * 6
    minute_rad = pygame.math.Vector2(0, -radius * 0.7).rotate(minute_angle)
    pygame.draw.line(screen, BLACK, center, (center[0] + minute_rad.x, center[1] + minute_rad.y), 4)
    # Draw second hand
    second_angle = seconds * 6
    second_rad = pygame.math.Vector2(0, -radius * 0.9).rotate(second_angle)
    pygame.draw.line(screen, RED, center, (center[0] + second_rad.x, center[1] + second_rad.y), 2)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Analog Clock Game")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 24)

    # Status variables
    lives = 3
    score = 0
    high_score = load_high_score()
    start_time = time.time()
    game_title = "Analog Clock Game"
    last_score_update = start_time

    running = True
    while running:
        current_time_val = time.time()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update score every second
        if current_time_val - last_score_update >= 1:
            score += 1
            last_score_update = current_time_val
            if score > high_score:
                high_score = score
                save_high_score(high_score)

        screen.fill(WHITE)

        # Draw title line
        current_date = time.strftime("%Y-%m-%d")
        current_time_str = time.strftime("%H:%M:%S")
        title_date = font.render(current_date, True, BLACK)
        title_text = font.render(game_title, True, BLACK)
        title_time = font.render(current_time_str, True, BLACK)
        screen.blit(title_date, (10, 10))
        screen.blit(title_text, (WINDOW_WIDTH // 2 - title_text.get_width() // 2, 10))
        screen.blit(title_time, (WINDOW_WIDTH - title_time.get_width() - 10, 10))

        # Draw analog clock
        draw_clock(screen, CLOCK_CENTER, CLOCK_RADIUS)

        # Draw status line at bottom
        elapsed_seconds = int(current_time_val - start_time)
        status_lives = font.render(f"Lives: {lives}", True, BLACK)
        status_score = font.render(f"Score: {score} / High: {high_score}", True, BLACK)
        status_time = font.render(f"Time: {elapsed_seconds}s", True, BLACK)
        screen.blit(status_lives, (10, WINDOW_HEIGHT - 30))
        screen.blit(status_score, (WINDOW_WIDTH // 2 - status_score.get_width() // 2, WINDOW_HEIGHT - 30))
        screen.blit(status_time, (WINDOW_WIDTH - status_time.get_width() - 10, WINDOW_HEIGHT - 30))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()