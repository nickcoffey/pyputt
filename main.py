# Example file showing a circle moving on screen
import pygame
from pygame.rect import Rect

# pygame setup
pygame.init()
SCREEN = pygame.display.set_mode((1280, 720))
CLOCK = pygame.time.Clock()
RUNNING = True
DELTA_TIME = 0

PLAYER_POS = pygame.Vector2(SCREEN.get_width() / 2, SCREEN.get_height() / 2)
BALL_SPEED = 600
BALL_SIZE = 40
BALL_RADIUS = BALL_SIZE / 2


def check_bounds() -> None:
    # left & right bounds of screen
    if PLAYER_POS.x < BALL_SIZE:
        PLAYER_POS.x = BALL_SIZE
    elif PLAYER_POS.x > SCREEN.get_width() - BALL_SIZE:
        PLAYER_POS.x = SCREEN.get_width() - BALL_SIZE
    # top & bottom bounds of screen
    if PLAYER_POS.y < BALL_SIZE:
        PLAYER_POS.y = BALL_SIZE
    elif PLAYER_POS.y > SCREEN.get_height() - BALL_SIZE:
        PLAYER_POS.y = SCREEN.get_height() - BALL_SIZE


def detect_collision(temp_course: Rect, temp_ball: Rect) -> None:
    ball_left = (temp_ball.x, temp_ball.y - BALL_RADIUS)
    ball_right = (temp_ball.x + BALL_SIZE, temp_ball.y - BALL_RADIUS)
    ball_top = (temp_ball.x + BALL_RADIUS, temp_ball.y)
    ball_bottom = (temp_ball.x + BALL_RADIUS, temp_ball.y + BALL_SIZE)
    #
    # if temp_course.collidepoint(ball_left):
    #     PLAYER_POS.x = -BALL_SPEED * DELTA_TIME

    # print(temp_course.collidelistall([temp_ball]))

    rect_left = (temp_course.x, temp_course.y - BALL_RADIUS)
    rect_right = (temp_course.x + BALL_SIZE, temp_course.y - BALL_RADIUS)
    rect_top = (temp_course.x + BALL_RADIUS, temp_course.y)
    rect_bottom = (temp_course.x + BALL_RADIUS, temp_course.y + BALL_SIZE)
    if temp_course.colliderect(temp_ball):
        PLAYER_POS.x = LAST_POS.x
        PLAYER_POS.y = LAST_POS.y
        # if ball_left[0] < rect_right[0]:
        #     PLAYER_POS.x = rect_right[0] + BALL_SIZE
        # elif ball_right[0] > rect_left[0]:
        #     PLAYER_POS.x = rect_left[0] - BALL_SIZE
        # elif ball_top[1] > rect_bottom[1]:
        #     PLAYER_POS.y = rect_bottom[1] + BALL_SIZE
        # elif ball_bottom[1] < rect_top[1]:
        #     PLAYER_POS.y = rect_top[1] - BALL_SIZE


LAST_POS = pygame.Vector2(PLAYER_POS.x, PLAYER_POS.y)


def move_ball() -> None:
    LAST_POS.x = PLAYER_POS.x
    LAST_POS.y = PLAYER_POS.y

    keys = pygame.key.get_pressed()
    if keys[pygame.K_i]:
        PLAYER_POS.y -= BALL_SPEED * DELTA_TIME
    if keys[pygame.K_k]:
        PLAYER_POS.y += BALL_SPEED * DELTA_TIME
    if keys[pygame.K_j]:
        PLAYER_POS.x -= BALL_SPEED * DELTA_TIME
    if keys[pygame.K_l]:
        PLAYER_POS.x += BALL_SPEED * DELTA_TIME


def draw_course() -> Rect:
    return pygame.draw.rect(
        SCREEN,
        "brown",
        pygame.Rect(SCREEN.get_width() / 4, SCREEN.get_height() / 4, 20, 20),
        BALL_SIZE,
    )


while RUNNING:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNNING = False

    # fill the screen with a color to wipe away anything from last frame
    SCREEN.fill("green")
    course = draw_course()
    ball = pygame.draw.circle(SCREEN, "white", PLAYER_POS, BALL_SIZE)

    move_ball()
    print(f"POS: {PLAYER_POS}, LAST_POS: {LAST_POS}")
    check_bounds()
    detect_collision(course, ball)

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # delta time in seconds since last frame, used for framerate-independent physics.
    DELTA_TIME = CLOCK.tick(60) / 1000

pygame.quit()
