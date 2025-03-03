from typing import Any
import pygame
import libs

from pygame import Rect, Surface, Vector2


class Ball:
    def __init__(self):
        self.speed = 600
        self.size = 10
        self.radius = self.size / 2
        self.start_position = Vector2(0, 0)
        self.position = Vector2(0, 0)
        self.collidables: list[libs.Collidable] = []
        self.rect: Rect

    def draw(self, screen: Surface) -> Rect:
        self.rect = pygame.draw.circle(screen, "white", self.position, self.size)
        return self.rect

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
