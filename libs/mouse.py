import pygame

from pygame import Rect, Surface


class Mouse:
    def __init__(self) -> None:
        self.rect: Rect
        self.is_left_click_down = False
        self.is_dragging = False

    def update(self, screen: Surface) -> None:
        self.rect = pygame.draw.circle(screen, "pink", pygame.mouse.get_pos(), 5)
        self.is_left_click_down = bool(pygame.mouse.get_pressed(3)[0])

        if not self.is_left_click_down:
            self.is_dragging = False

        if self.is_dragging:
            print("DRAGGING")

    def ball_collision_action(self):
        if self.is_left_click_down:
            self.is_dragging = True
