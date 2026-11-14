import pygame
import sys


pygame.init()


# Constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (160, 160, 160)
FPS = 60


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame Pong")
clock = pygame.time.Clock()


title_font = pygame.font.SysFont("monospace", 54, bold=True)
menu_font = pygame.font.SysFont("monospace", 28)
small_font = pygame.font.SysFont("monospace", 18)
score_font = pygame.font.SysFont("monospace", 36)


# Game Objects
left_paddle = pygame.Rect(30, HEIGHT // 2 - 50, 15, 100)
right_paddle = pygame.Rect(WIDTH - 45, HEIGHT // 2 - 50, 15, 100)
ball = pygame.Rect(WIDTH // 2 - 10, HEIGHT // 2 - 10, 20, 20)


ball_dx, ball_dy = 5, 5
paddle_speed = 7
ai_speed = 5  # Slightly slower than player so the AI is beatable
score_left, score_right = 0, 0


game_state = "MENU"  # "MENU" or "PLAYING"
vs_computer = False




def reset_game():
    global score_left, score_right, ball_dx, ball_dy
    score_left = 0
    score_right = 0
    left_paddle.centery = HEIGHT // 2
    right_paddle.centery = HEIGHT // 2
    ball.center = (WIDTH // 2, HEIGHT // 2)
    ball_dx = 5
    ball_dy = 5




while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


        if event.type == pygame.KEYDOWN:
            if game_state == "MENU":
                if event.key == pygame.K_1:
                    vs_computer = True
                    reset_game()
                    game_state = "PLAYING"
                elif event.key == pygame.K_2:
                    vs_computer = False
                    reset_game()
                    game_state = "PLAYING"
            elif game_state == "PLAYING":
                if event.key == pygame.K_ESCAPE:
                    game_state = "MENU"


    screen.fill(BLACK)


    if game_state == "MENU":
        title_text = title_font.render("BIT BOUNCE", True, WHITE)
        opt1_text = menu_font.render("Press 1: Single Player (vs Computer)", True, WHITE)
        opt2_text = menu_font.render("Press 2: 2 Players (Local)", True, WHITE)
        controls_text = small_font.render("P1: W/S   |   P2: Up/Down   |   ESC: Menu", True, GRAY)


        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 130))
        screen.blit(opt1_text, (WIDTH // 2 - opt1_text.get_width() // 2, 260))
        screen.blit(opt2_text, (WIDTH // 2 - opt2_text.get_width() // 2, 320))
        screen.blit(controls_text, (WIDTH // 2 - controls_text.get_width() // 2, 430))


    elif game_state == "PLAYING":
        keys = pygame.key.get_pressed()


        # Left Paddle (Player 1)
        if keys[pygame.K_w] and left_paddle.top > 0:
            left_paddle.y -= paddle_speed
        if keys[pygame.K_s] and left_paddle.bottom < HEIGHT:
            left_paddle.y += paddle_speed


        # Right Paddle (Computer AI or Player 2)
        if vs_computer:
            # AI tracks the ball only when the ball moves toward the right side
            if ball_dx > 0:
                if right_paddle.centery < ball.centery - 10 and right_paddle.bottom < HEIGHT:
                    right_paddle.y += ai_speed
                elif right_paddle.centery > ball.centery + 10 and right_paddle.top > 0:
                    right_paddle.y -= ai_speed
        else:
            if keys[pygame.K_UP] and right_paddle.top > 0:
                right_paddle.y -= paddle_speed
            if keys[pygame.K_DOWN] and right_paddle.bottom < HEIGHT:
                right_paddle.y += paddle_speed


        # Move ball
        ball.x += ball_dx
        ball.y += ball_dy


        # Wall collision
        if ball.top <= 0 or ball.bottom >= HEIGHT:
            ball_dy *= -1


        # Paddle collision
        if ball.colliderect(left_paddle) and ball_dx < 0:
            ball_dx *= -1
        if ball.colliderect(right_paddle) and ball_dx > 0:
            ball_dx *= -1


        # Scoring
        if ball.left <= 0:
            score_right += 1
            ball.center = (WIDTH // 2, HEIGHT // 2)
            ball_dx *= -1
        if ball.right >= WIDTH:
            score_left += 1
            ball.center = (WIDTH // 2, HEIGHT // 2)
            ball_dx *= -1


        # Draw arena and paddles
        pygame.draw.rect(screen, WHITE, left_paddle)
        pygame.draw.rect(screen, WHITE, right_paddle)
        pygame.draw.ellipse(screen, WHITE, ball)
        pygame.draw.aaline(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))


        # Draw score and mode label
        score_text = score_font.render(f"{score_left}   {score_right}", True, WHITE)
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 20))


        mode_label = "VS COMPUTER (ESC: Menu)" if vs_computer else "2 PLAYERS (ESC: Menu)"
        mode_text = small_font.render(mode_label, True, GRAY)
        screen.blit(mode_text, (WIDTH // 2 - mode_text.get_width() // 2, HEIGHT - 30))


    pygame.display.flip()
    clock.tick(FPS)