# Example file showing a circle moving on screen
import pygame
import json

from typing import Any
from pygame.math import Vector2
from pygame.rect import Rect


with open("course.json", encoding="utf-8") as f_in:
    COURSE = json.load(f_in)

# pygame setup
pygame.init()
SCREEN = pygame.display.set_mode((1280, 720))
CLOCK = pygame.time.Clock()
RUNNING = True
DELTA_TIME = 0

BALL_SPEED = 600
BALL_SIZE = 10
BALL_RADIUS = BALL_SIZE / 2
PLAYER_START: Any = None  # type: ignore
PLAYER_POS: Any = None  # type: ignore


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
    if temp_course.colliderect(temp_ball):
        PLAYER_POS.x = PLAYER_START.x
        PLAYER_POS.y = PLAYER_START.y


def move_ball() -> None:
    keys = pygame.key.get_pressed()
    if keys[pygame.K_i] or keys[pygame.K_w]:
        PLAYER_POS.y -= BALL_SPEED * DELTA_TIME
    if keys[pygame.K_k] or keys[pygame.K_s]:
        PLAYER_POS.y += BALL_SPEED * DELTA_TIME
    if keys[pygame.K_j] or keys[pygame.K_a]:
        PLAYER_POS.x -= BALL_SPEED * DELTA_TIME
    if keys[pygame.K_l] or keys[pygame.K_d]:
        PLAYER_POS.x += BALL_SPEED * DELTA_TIME


def draw_course():
    global PLAYER_START, PLAYER_POS
    box_size = 40
    for y, row in enumerate(COURSE):
        for x, value in enumerate(row):
            if value == 1:
                pygame.draw.rect(
                    SCREEN,
                    "brown",
                    pygame.Rect(x * box_size, y * box_size, box_size, box_size),
                    box_size,
                )
            elif value == 2 and PLAYER_START is None:
                PLAYER_START = Vector2(
                    (x * box_size) + (BALL_SIZE * 2), y * box_size + BALL_SIZE
                )
                PLAYER_POS = Vector2(PLAYER_START)
            if value == 3:
                hole_size = 20
                hole_pos = Vector2(x * box_size + hole_size, y * box_size + hole_size)
                pygame.draw.circle(SCREEN, "black", hole_pos, hole_size)


def draw_hole() -> Rect:
    hole_pos = Vector2(SCREEN.get_width() - 120, SCREEN.get_height() - 120)
    return pygame.draw.circle(SCREEN, "black", hole_pos, 20)


while RUNNING:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNNING = False

    # fill the screen with a color to wipe away anything from last frame
    SCREEN.fill("green")
    draw_course()
    ball = pygame.draw.circle(SCREEN, "white", PLAYER_POS, BALL_SIZE)

    # draw_hole()
    move_ball()
    check_bounds()
    # detect_collision(course, ball)

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # delta time in seconds since last frame, used for framerate-independent physics.
    DELTA_TIME = CLOCK.tick(60) / 1000

pygame.quit()
