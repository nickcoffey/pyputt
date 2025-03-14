import pygame
import libs

from typing import Any
from pygame import Rect, Surface, Vector2

SPEED_MULTIPLIER = 15
DECELERATION = 16


class Ball:
    def __init__(self):
        self.speed = 600
        self.x_speed = 0.0
        self.y_speed = 0.0
        self.speed_multiplier = SPEED_MULTIPLIER
        self.size = 10
        self.radius = self.size / 2
        self.start_position = Vector2(0, 0)
        self.position = Vector2(0, 0)
        self.collidables: list[libs.Collidable] = []
        self.rect: Rect

    def draw(self, screen: Surface, delta_time: float) -> None:
        self.position.x += self.speed_multiplier * self.x_speed
        self.position.y += self.speed_multiplier * self.y_speed

        self.speed_multiplier -= DECELERATION * delta_time
        if self.speed_multiplier < 0:
            self.speed_multiplier = 0

        self.rect = pygame.draw.circle(screen, "white", self.position, self.size)

    def move(self, delta_time: float) -> None:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_i] or keys[pygame.K_w]:
            self.position.y -= self.speed * delta_time
        if keys[pygame.K_k] or keys[pygame.K_s]:
            self.position.y += self.speed * delta_time
        if keys[pygame.K_j] or keys[pygame.K_a]:
            self.position.x -= self.speed * delta_time
        if keys[pygame.K_l] or keys[pygame.K_d]:
            self.position.x += self.speed * delta_time

    def mouse_move(self, power: tuple[int, int], max_power: int) -> None:
        self.x_speed = power[0] / max_power
        self.y_speed = power[1] / max_power
        self.speed_multiplier = SPEED_MULTIPLIER

    def move_to_start(self) -> None:
        self.position.x = self.start_position.x
        self.position.y = self.start_position.y

    def check_bounds(self, screen: Surface) -> None:
        # left & right bounds of screen
        if self.position.x < self.size:
            self.position.x = self.size
        elif self.position.x > screen.get_width() - self.size:
            self.position.x = screen.get_width() - self.size
        # top & bottom bounds of screen
        if self.position.y < self.size:
            self.position.y = self.size
        elif self.position.y > screen.get_height() - self.size:
            self.position.y = screen.get_height() - self.size

    # TODO: fix this typing. this is fixing weird import errors
    def add_collidable(self, new_collidable: Any):
        self.collidables.append(new_collidable)

    def check_collidables(self):
        for collidable in self.collidables:
            if collidable.collision_check(self):
                collidable.collision_action(self)
                break
