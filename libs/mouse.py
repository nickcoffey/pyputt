import pygame

from pygame import Rect, Surface


class Mouse:
    def __init__(self) -> None:
        self.rect: Rect
        self.is_left_click_down = False
        self.is_dragging = False
        self.mouse_color = "red"

    def update(self, screen: Surface, ball_rect: Rect) -> None:
        self.rect = pygame.draw.circle(
            screen, self.mouse_color, pygame.mouse.get_pos(), 5
        )
        self.is_left_click_down = bool(pygame.mouse.get_pressed(3)[0])

        if not self.is_left_click_down:
            self.is_dragging = False

        if self.is_dragging:
            temp_mouse_pos = pygame.mouse.get_pos()
            flipped_mouse_x = ball_rect.center[0] + (
                ball_rect.center[0] - temp_mouse_pos[0]
            )
            flipped_mouse_y = ball_rect.center[1] + (
                ball_rect.center[1] - temp_mouse_pos[1]
            )

            oppo_mouse = pygame.draw.circle(
                screen, self.mouse_color, (flipped_mouse_x, flipped_mouse_y), 5
            )
            pygame.draw.line(
                screen, self.mouse_color, ball_rect.center, oppo_mouse.center, 2
            )

    def ball_collision_action(self):
        if self.is_left_click_down:
            self.is_dragging = True
