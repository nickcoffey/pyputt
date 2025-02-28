# Example file showing a circle moving on screen
import pygame

from typing import Any
from pygame import Rect, Vector2

from libs.course.course import draw_course


# pygame setup
pygame.init()
SCREEN = pygame.display.set_mode((1280, 720))
CLOCK = pygame.time.Clock()
RUNNING = True
DELTA_TIME = 0

BALL_SPEED = 600
BALL_SIZE = 10
BALL_RADIUS = BALL_SIZE / 2
BALL_START_POS: Any = None
BALL_POS: Any = None

FONT = pygame.font.Font("Futura.ttc", 72)
WINNER_TEXT = FONT.render("You Win!!!", True, (255, 255, 255), (0, 0, 0))
WINNER_TEXT_RECT = WINNER_TEXT.get_rect(center=(1280 / 2, 720 / 2))


def check_bounds() -> None:
    # left & right bounds of screen
    if BALL_POS.x < BALL_SIZE:
        BALL_POS.x = BALL_SIZE
    elif BALL_POS.x > SCREEN.get_width() - BALL_SIZE:
        BALL_POS.x = SCREEN.get_width() - BALL_SIZE
    # top & bottom bounds of screen
    if BALL_POS.y < BALL_SIZE:
        BALL_POS.y = BALL_SIZE
    elif BALL_POS.y > SCREEN.get_height() - BALL_SIZE:
        BALL_POS.y = SCREEN.get_height() - BALL_SIZE


def detect_collision(course: list[Rect], hole: Rect, ball: Rect) -> None:
    if ball.collidelist(course) != -1:
        BALL_POS.x = BALL_START_POS.x
        BALL_POS.y = BALL_START_POS.y
    elif ball.colliderect(hole):
        SCREEN.blit(WINNER_TEXT, WINNER_TEXT_RECT)


def move_ball() -> None:
    keys = pygame.key.get_pressed()
    if keys[pygame.K_i] or keys[pygame.K_w]:
        BALL_POS.y -= BALL_SPEED * DELTA_TIME
    if keys[pygame.K_k] or keys[pygame.K_s]:
        BALL_POS.y += BALL_SPEED * DELTA_TIME
    if keys[pygame.K_j] or keys[pygame.K_a]:
        BALL_POS.x -= BALL_SPEED * DELTA_TIME
    if keys[pygame.K_l] or keys[pygame.K_d]:
        BALL_POS.x += BALL_SPEED * DELTA_TIME


def main():
    global RUNNING, DELTA_TIME, BALL_START_POS, BALL_POS
    is_first_loop = True

    while RUNNING:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUNNING = False

        # fill the screen with a color to wipe away anything from last frame
        SCREEN.fill("green")

        course, hole, ball_start_pos = draw_course(BALL_SIZE, SCREEN)
        if is_first_loop:
            BALL_START_POS = Vector2(ball_start_pos)
            BALL_POS = Vector2(ball_start_pos)

        ball = pygame.draw.circle(SCREEN, "white", BALL_POS, BALL_SIZE)

        move_ball()
        check_bounds()
        detect_collision(course, hole, ball)

        # flip() the display to put your work on screen
        pygame.display.flip()

        # limits FPS to 60
        # delta time in seconds since last frame, used for framerate-independent physics.
        DELTA_TIME = CLOCK.tick(60) / 1000

        if is_first_loop:
            is_first_loop = False

    pygame.quit()


main()
