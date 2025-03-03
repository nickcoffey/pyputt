from typing import Callable
import libs

from abc import abstractmethod


class Collidable:
    def __init__(self, collision_check: Callable, collision_action: Callable):
        self.collision_check = collision_check
        self.collision_action = collision_action

    @abstractmethod
    def collision_check(self, ball: libs.Ball) -> bool:
        pass

    @abstractmethod
    def collision_action(self, ball: libs.Ball):
        pass
