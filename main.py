# Example file showing a circle moving on screen
import pygame

from pygame import Vector2

from libs.ball import Ball
from libs.collidable import Collidable
from libs.course.course import draw_course, load_next_level, MAX_LEVEL
from libs.mouse import Mouse
from libs.par_tracker import ParTracker
from libs.pause_handler import PauseHandler


# pygame setup
pygame.init()
pygame.display.set_caption("PyPutt", "PyPutt")

SCREEN = pygame.display.set_mode((1280, 720))
CLOCK = pygame.time.Clock()
RUNNING = True
GAME_OVER = False
DELTA_TIME = 0
COURSE_COLLISION_IDX_LIST = []
FONT = pygame.font.Font("Futura.ttc", 72)
SMALL_FONT = pygame.font.Font("Futura.ttc", 24)
WINNER_TEXT_LIST = [
    FONT.render(f"Level {level} Complete!", True, (255, 255, 255), (0, 0, 0))
    for level in range(1, MAX_LEVEL + 1)
]
WINNER_TEXT_RECT_LIST = [
    winner_text.get_rect(center=(1280 / 2, 720 / 2)) for winner_text in WINNER_TEXT_LIST
]


def hole_pause_action():
    from libs.course.course import (  # pylint: disable=import-outside-toplevel
        LEVEL_NUM,
    )

    level_idx = LEVEL_NUM - 1
    SCREEN.blit(WINNER_TEXT_LIST[level_idx], WINNER_TEXT_RECT_LIST[level_idx])


def hole_resume_action():
    global GAME_OVER
    is_game_over = load_next_level()
    GAME_OVER = is_game_over


def main():
    global RUNNING, DELTA_TIME, GAME_OVER
    is_first_loop = True
    pause_handler = PauseHandler()
    par_tracker = ParTracker()
    ball = Ball()

    def move_ball(power: tuple[int, int], max_power: int):
        ball.mouse_move(power, max_power)
        par_tracker.shots += 1

    def course_collision_check(ball: Ball):
        global COURSE_COLLISION_IDX_LIST
        COURSE_COLLISION_IDX_LIST = ball.rect.collidelistall(course)
        return COURSE_COLLISION_IDX_LIST != []

    def course_collision_action(ball: Ball):
        for index in COURSE_COLLISION_IDX_LIST:
            collided_wall = course[index]
            if ball.y_speed < 0 and collided_wall.collidepoint(ball.rect.midtop):
                ball.y_speed = ball.y_speed * -1
                ball.position.y = collided_wall.bottom + (ball.rect.height / 2)
                break
            elif ball.y_speed > 0 and collided_wall.collidepoint(ball.rect.midbottom):
                ball.y_speed = ball.y_speed * -1
                ball.position.y = collided_wall.top - (ball.rect.height / 2)
                break
            elif ball.x_speed < 0 and collided_wall.collidepoint(ball.rect.midleft):
                ball.x_speed = ball.x_speed * -1
                ball.position.x = collided_wall.right + (ball.rect.width / 2)
                break
            elif ball.x_speed > 0 and collided_wall.collidepoint(ball.rect.midright):
                ball.x_speed = ball.x_speed * -1
                ball.position.x = collided_wall.left - (ball.rect.width / 2)
                break

    course_collidable = Collidable(
        collision_check=course_collision_check,
        collision_action=course_collision_action,
    )
    ball.add_collidable(course_collidable)

    hole_collidable = Collidable(
        collision_check=lambda ball: hole.collidepoint(ball.rect.center),
        collision_action=lambda _: pause_handler.start_pause(
            3,
            hole_resume_action,
            hole_pause_action,
        ),
    )
    ball.add_collidable(hole_collidable)

    mouse = Mouse()

    mouse_collidable = Collidable(
        collision_check=lambda ball: ball.rect.colliderect(mouse.rect),
        collision_action=lambda _: mouse.ball_collision_action(),
    )
    ball.add_collidable(mouse_collidable)

    while RUNNING:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUNNING = False

        if GAME_OVER:
            par_tracker.show_game_over_screen(SCREEN, FONT)
            pygame.display.flip()
            continue

        course, hole, ball_start_pos = draw_course(SCREEN)

        if is_first_loop or ball_start_pos != ball.start_position:
            ball.start_position = Vector2(ball_start_pos)
            ball.position = Vector2(ball_start_pos)

        ball.draw(SCREEN, DELTA_TIME)
        mouse.update(SCREEN, ball.rect, move_ball)

        if pause_handler.is_paused:
            ball.speed_multiplier = 0
            pause_handler.decrement_frames(DELTA_TIME)
        else:
            ball.move(DELTA_TIME)
            ball.check_bounds(SCREEN)
            ball.check_collidables()

        shot_text = SMALL_FONT.render(
            f"Par: {par_tracker.par} | Shots: {par_tracker.shots}",
            True,
            (255, 255, 255),
            (0, 0, 0),
        )
        shot_text_rect = shot_text.get_rect(topleft=(0, 0))
        SCREEN.blit(shot_text, shot_text_rect)

        # flip() the display to put your work on screen
        pygame.display.flip()

        # limits FPS to 60
        # delta time in seconds since last frame, used for framerate-independent physics.
        DELTA_TIME = CLOCK.tick(60) / 1000

        if is_first_loop:
            is_first_loop = False

    pygame.quit()


main()
