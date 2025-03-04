# Example file showing a circle moving on screen
import pygame

from pygame import Vector2

from libs.ball import Ball
from libs.collidable import Collidable
from libs.course.course import draw_course
from libs.mouse import Mouse
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

COURSE_COLLISION_IDX = -1


def main():
    global RUNNING, DELTA_TIME
    is_first_loop = True
    pause_handler = PauseHandler()
    ball = Ball()

    def course_collision_check(ball: Ball):
        global COURSE_COLLISION_IDX
        coll = ball.rect.collidelist(course)
        print(ball.rect.collidelistall(course))
        COURSE_COLLISION_IDX = coll
        return coll != -1

    def course_collision_action(ball: Ball):
        collided_wall = course[COURSE_COLLISION_IDX]
        # print(collided_wall.right, collided_wall.bottom)
        # print(
        #     ball.rect.midtop, ball.rect.midbottom, ball.rect.midleft, ball.rect.midright
        # )
        if ball.y_speed < 0 and collided_wall.collidepoint(ball.rect.midtop):
            print("HIT TOP")
            ball.y_speed = ball.y_speed * -1
            ball.position.y = collided_wall.bottom + (ball.rect.height / 2)
        elif ball.y_speed > 0 and collided_wall.collidepoint(ball.rect.midbottom):
            print("HIT BOTTOM")
            ball.y_speed = ball.y_speed * -1
            ball.position.y = collided_wall.top - (ball.rect.height / 2)
        elif ball.x_speed < 0 and collided_wall.collidepoint(ball.rect.midleft):
            print("HIT LEFT")
            ball.x_speed = ball.x_speed * -1
            ball.position.x = collided_wall.right + (ball.rect.width / 2)
        elif ball.x_speed > 0 and collided_wall.collidepoint(ball.rect.midright):
            print("HIT RIGHT")
            ball.x_speed = ball.x_speed * -1
            ball.position.x = collided_wall.left - (ball.rect.width / 2)
        else:
            print("HIT INTERSECTION")
            pygame.quit()
        #     # ball.position.x = collided_wall.x
        #     ball.x_speed = ball.x_speed * -1
        #     ball.position.x = collided_wall.x + ball.x_speed
        # ball.move_to_start()

    course_collidable = Collidable(
        collision_check=course_collision_check,
        collision_action=course_collision_action,
    )
    ball.add_collidable(course_collidable)

    hole_collidable = Collidable(
        collision_check=lambda ball: ball.rect.colliderect(hole),
        collision_action=lambda ball: pause_handler.start_pause(
            3,
            ball.move_to_start,
            lambda: SCREEN.blit(WINNER_TEXT, WINNER_TEXT_RECT),
        ),
    )
    ball.add_collidable(hole_collidable)

    mouse = Mouse()

    mouse_collidable = Collidable(
        collision_check=lambda ball: ball.rect.colliderect(mouse.rect),
        collision_action=lambda ball: mouse.ball_collision_action(),
    )
    ball.add_collidable(mouse_collidable)

    while RUNNING:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUNNING = False

        # fill the screen with a color to wipe away anything from last frame
        SCREEN.fill("green")

        course, hole, ball_start_pos = draw_course(ball.size, SCREEN)

        if is_first_loop:
            ball.start_position = Vector2(ball_start_pos)
            ball.position = Vector2(ball_start_pos)

        ball.draw(SCREEN, DELTA_TIME)
        mouse.update(SCREEN, ball.rect, ball.mouse_move)

        if pause_handler.is_paused:
            pause_handler.decrement_frames(DELTA_TIME)
        else:
            ball.move(DELTA_TIME)
            ball.check_bounds(SCREEN)
            ball.check_collidables()

        # flip() the display to put your work on screen
        pygame.display.flip()

        # limits FPS to 60
        # delta time in seconds since last frame, used for framerate-independent physics.
        DELTA_TIME = CLOCK.tick(60) / 1000

        if is_first_loop:
            is_first_loop = False

    pygame.quit()


main()
