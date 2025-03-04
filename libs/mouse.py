import pygame

from typing import Callable
from pygame import Rect, Surface


class Mouse:
    def __init__(self) -> None:
        self.rect: Rect
        self.is_left_click_down = False
        self.is_dragging = False
        self.mouse_color = "red"
        self.shot_power = (0, 0)
        self.line_max = 150

    def update(
        self,
        screen: Surface,
        ball_rect: Rect,
        move_ball: Callable[[tuple[int, int], int], None],
    ) -> None:
        position = pygame.mouse.get_pos()

        self.rect = pygame.draw.circle(screen, self.mouse_color, position, 5)
        self.is_left_click_down = bool(pygame.mouse.get_pressed(3)[0])

        if self.is_dragging is True and not self.is_left_click_down:
            self.is_dragging = False
            move_ball(self.shot_power, self.line_max)

        if self.is_dragging:
            x_diff = ball_rect.center[0] - position[0]
            y_diff = ball_rect.center[1] - position[1]

            x_max = self.line_max - 2
            if x_diff < -x_max:
                x_diff = -x_max
            elif x_diff > x_max:
                x_diff = x_max

            y_max = self.line_max - 1
            if y_diff < -y_max:
                y_diff = -y_max
            elif y_diff > y_max:
                y_diff = y_max

            flipped_mouse_x = ball_rect.center[0] + x_diff
            flipped_mouse_y = ball_rect.center[1] + y_diff

            oppo_mouse = pygame.draw.circle(
                screen, self.mouse_color, (flipped_mouse_x, flipped_mouse_y), 5
            )
            line = pygame.draw.line(
                screen, self.mouse_color, ball_rect.center, oppo_mouse.center, 2
            )
            x_power = line.size[0]
            if x_diff < 0:
                x_power = -x_power

            y_power = line.size[1]
            if y_diff < 0:
                y_power = -y_power

            self.shot_power = (x_power, y_power)

    def ball_collision_action(self):
        if self.is_left_click_down:
            self.is_dragging = True
