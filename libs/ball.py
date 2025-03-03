import math
import pygame
import libs

from typing import Any
from pygame import Rect, Surface, Vector2


class Ball:
    def __init__(self):
        self.speed = 600
        self.temp_speed = (0.0, 0.0)
        self.deceleration_amt = 25
        self.size = 10
        self.radius = self.size / 2
        self.start_position = Vector2(0, 0)
        self.position = Vector2(0, 0)
        self.collidables: list[libs.Collidable] = []
        self.rect: Rect

    # FIXME: weird tailing off bug
    def draw(self, screen: Surface, delta_time: float) -> None:
        self.position.x += self.temp_speed[0]
        self.position.y += self.temp_speed[1]

        x_speed = self.temp_speed[0]
        y_speed = self.temp_speed[1]
        if x_speed > 0:
            x_speed -= self.deceleration_amt * delta_time
            x_speed = x_speed if x_speed > 0 else 0
        elif x_speed < 0:
            x_speed += self.deceleration_amt * delta_time
            x_speed = x_speed if x_speed < 0 else 0
        if y_speed > 0:
            y_speed -= self.deceleration_amt * delta_time
            y_speed = y_speed if y_speed > 0 else 0
        elif y_speed < 0:
            y_speed += self.deceleration_amt * delta_time
            y_speed = y_speed if y_speed < 0 else 0
        self.temp_speed = (math.trunc(x_speed), math.trunc(y_speed))
        print(self.temp_speed)

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

    def mouse_move(self, power: tuple[int, int]) -> None:
        self.temp_speed = (power[0] / 5, power[1] / 5)

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
