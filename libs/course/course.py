import json
import pygame

from pygame import Rect, Surface, Vector2


with open("libs/course/data/level_1.json", encoding="utf-8") as f_in:
    COURSE_GRID = json.load(f_in)


def draw_course(ball_size: int, screen: Surface) -> tuple[list[Rect], Rect, Vector2]:
    ball_start_pos = Vector2(0, 0)
    box_size = 40
    hole_size = 20
    course: list[Rect] = []
    hole: Rect = pygame.draw.circle(
        screen, "black", Vector2(hole_size, hole_size), hole_size
    )

    for y, row in enumerate(COURSE_GRID):
        for x, value in enumerate(row):
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
                ball_start_pos = Vector2(
                    (x * box_size) + (ball_size * 2), y * box_size + ball_size
                )
            elif value == 3:
                hole_pos = Vector2(x * box_size + hole_size, y * box_size + hole_size)
                hole = pygame.draw.circle(screen, "black", hole_pos, hole_size)

    return course, hole, ball_start_pos
