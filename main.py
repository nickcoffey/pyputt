# Example file showing a circle moving on screen
import pygame

from typing import Callable
from pygame import Rect, Vector2

from libs.ball import Ball
from libs.course.course import draw_course
from libs.pause_handler import PauseHandler


# pygame setup
pygame.init()
SCREEN = pygame.display.set_mode((1280, 720))
CLOCK = pygame.time.Clock()
RUNNING = True
DELTA_TIME = 0

FONT = pygame.font.Font("Futura.ttc", 72)
WINNER_TEXT = FONT.render("You Win!!!", True, (255, 255, 255), (0, 0, 0))
WINNER_TEXT_RECT = WINNER_TEXT.get_rect(center=(1280 / 2, 720 / 2))


def detect_collision(
    course: list[Rect],
    hole: Rect,
    ball: Rect,
    pause_handler: PauseHandler,
    move_ball_to_start: Callable,
) -> None:
    if ball.collidelist(course) != -1:
        move_ball_to_start()
    elif ball.colliderect(hole):
        pause_handler.start_pause(
            3, move_ball_to_start, lambda: SCREEN.blit(WINNER_TEXT, WINNER_TEXT_RECT)
        )


def main():
    global RUNNING, DELTA_TIME
    is_first_loop = True
    pause_handler = PauseHandler()
    ball = Ball()

    while RUNNING:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUNNING = False

        # fill the screen with a color to wipe away anything from last frame
        SCREEN.fill("green")

        # is_mouse_down = bool(pygame.mouse.get_pressed(3)[0])
        # print(is_mouse_down)
        # pygame.draw.circle(SCREEN, "pink", pygame.mouse.get_pos(), 5)

        course, hole, ball_start_pos = draw_course(ball.size, SCREEN)
        if is_first_loop:
            ball.start_position = Vector2(ball_start_pos)
            ball.position = Vector2(ball_start_pos)

        ball_rect = ball.draw(SCREEN)

        if pause_handler.is_paused:
            pause_handler.decrement_frames(DELTA_TIME)
        else:
            ball.move(DELTA_TIME)
            ball.check_bounds(SCREEN)
            detect_collision(course, hole, ball_rect, pause_handler, ball.move_to_start)

        # flip() the display to put your work on screen
        pygame.display.flip()

        # limits FPS to 60
        # delta time in seconds since last frame, used for framerate-independent physics.
        DELTA_TIME = CLOCK.tick(60) / 1000

        if is_first_loop:
            is_first_loop = False

    pygame.quit()


main()
