import json
import pygame

from pygame import Rect, Surface, Vector2
from libs.par_tracker import ParTracker

COURSE_GRID = [[]]
LEVEL_NUM = 0
MAX_LEVEL = 9

par_tracker = ParTracker()


def load_next_level() -> bool:
    global COURSE_GRID, LEVEL_NUM
    LEVEL_NUM += 1

    if LEVEL_NUM > MAX_LEVEL:
        return True

    with open(f"libs/course/data/level_{LEVEL_NUM}.json", encoding="utf-8") as f_in:
        level = json.load(f_in)
        COURSE_GRID = level["course"]
        par_tracker.next_hole(level["par"])

    return False


load_next_level()


def draw_course(screen: Surface) -> tuple[list[Rect], Rect, Vector2]:
    ball_start_pos = Vector2(0, 0)
    box_size = 40
    hole_size = 15
    course: list[Rect] = []
    hole: Rect = pygame.draw.circle(
        screen, "black", Vector2(hole_size, hole_size), hole_size
    )

    for y, row in enumerate(COURSE_GRID):
        for x, value in enumerate(row):
            current_box = pygame.draw.rect(
                screen,
                "green",
                pygame.Rect(x * box_size + 1, y * box_size + 1, box_size, box_size),
                box_size,
            )

            if value == 1:
                course.append(
                    pygame.draw.rect(
                        screen,
                        "brown",
                        pygame.Rect(x * box_size, y * box_size, box_size, box_size),
                        box_size,
                    )
                )
            elif value == 2:
                ball_start_pos = Vector2(current_box.center)
            elif value == 3:
                hole = pygame.draw.circle(
                    screen, "black", current_box.center, hole_size
                )

    return course, hole, ball_start_pos
