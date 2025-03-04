import pygame
import libs
from typing import Any, List, Optional, Tuple
from pygame import Rect, Surface, Vector2
from dataclasses import dataclass
from enum import Enum
import math

@dataclass
class BallConfig:
    """Configuration settings for Ball"""
    speed: float = 600
    size: int = 10
    deceleration: float = 16
    max_speed_multiplier: float = 15
    color: str = "white"
    bounce_factor: float = 0.8  # For realistic bouncing
    gravity: float = 9.81       # m/s² for physics simulation

class BallState(Enum):
    """States the ball can be in"""
    IDLE = "idle"
    MOVING = "moving"
    BOUNCING = "bouncing"

class Ball:
    def __init__(self, config: Optional[BallConfig] = None):
        """Initialize ball with optional configuration"""
        self.config = config or BallConfig()
        self.speed = self.config.speed
        self.velocity = Vector2(0.0, 0.0)
        self.speed_multiplier = 0.0
        self.size = self.config.size
        self.radius = self.size / 2
        self.start_position = Vector2(0, 0)
        self.position = Vector2(0, 0)
        self.collidables: List[libs.Collidable] = []
        self.rect: Optional[Rect] = None
        self.state = BallState.IDLE
        self.last_collision_time = 0.0
        self.collision_cooldown = 0.1  # Seconds
        self.mass = 1.0  # For physics calculations
        
    def draw(self, screen: Surface, delta_time: float) -> None:
        """Draw and update ball position with physics"""
        # Apply gravity if enabled
        if self.config.gravity > 0:
            self.velocity.y += self.config.gravity * delta_time

        # Update position with velocity
        self.position += self.velocity * self.speed_multiplier * delta_time

        # Apply deceleration
        if self.speed_multiplier > 0:
            self.speed_multiplier -= self.config.deceleration * delta_time
            if self.speed_multiplier < 0:
                self.speed_multiplier = 0
                self.state = BallState.IDLE

        # Draw the ball
        self.rect = pygame.draw.circle(
            screen, 
            self.config.color, 
            (int(self.position.x), int(self.position.y)), 
            self.size
        )

    def move(self, delta_time: float) -> None:
        """Handle keyboard movement"""
        keys = pygame.key.get_pressed()
        direction = Vector2(0, 0)
        
        if keys[pygame.K_i] or keys[pygame.K_w]:
            direction.y -= 1
        if keys[pygame.K_k] or keys[pygame.K_s]:
            direction.y += 1
        if keys[pygame.K_j] or keys[pygame.K_a]:
            direction.x -= 1
        if keys[pygame.K_l] or keys[pygame.K_d]:
            direction.x += 1

        if direction.length() > 0:
            direction.normalize_ip()
            self.velocity = direction
            self.speed_multiplier = self.config.max_speed_multiplier
            self.state = BallState.MOVING

    def launch(self, power: Tuple[int, int], max_power: int) -> None:
        """Launch ball with mouse-based power"""
        self.velocity.x = power[0] / max_power
        self.velocity.y = power[1] / max_power
        if self.velocity.length() > 0:
            self.velocity.normalize_ip()
        self.speed_multiplier = self.config.max_speed_multiplier
        self.state = BallState.MOVING

    def move_to_start(self) -> None:
        """Reset to starting position"""
        self.position = self.start_position.copy()
        self.velocity = Vector2(0, 0)
        self.speed_multiplier = 0
        self.state = BallState.IDLE

    def check_bounds(self, screen: Surface) -> None:
        """Handle screen boundaries with bouncing"""
        screen_rect = screen.get_rect()
        current_time = pygame.time.get_ticks() / 1000.0
        
        # Left & Right bounds
        if self.position.x - self.radius < 0:
            self.position.x = self.radius
            if current_time - self.last_collision_time > self.collision_cooldown:
                self.velocity.x = -self.velocity.x * self.config.bounce_factor
                self.last_collision_time = current_time
                self.state = BallState.BOUNCING
        elif self.position.x + self.radius > screen_rect.width:
            self.position.x = screen_rect.width - self.radius
            if current_time - self.last_collision_time > self.collision_cooldown:
                self.velocity.x = -self.velocity.x * self.config.bounce_factor
                self.last_collision_time = current_time
                self.state = BallState.BOUNCING

        # Top & Bottom bounds
        if self.position.y - self.radius < 0:
            self.position.y = self.radius
            if current_time - self.last_collision_time > self.collision_cooldown:
                self.velocity.y = -self.velocity.y * self.config.bounce_factor
                self.last_collision_time = current_time
                self.state = BallState.BOUNCING
        elif self.position.y + self.radius > screen_rect.height:
            self.position.y = screen_rect.height - self.radius
            if current_time - self.last_collision_time > self.collision_cooldown:
                self.velocity.y = -self.velocity.y * self.config.bounce_factor
                self.last_collision_time = current_time
                self.state = BallState.BOUNCING

    def add_collidable(self, new_collidable: 'libs.Collidable') -> None:
        """Add a collidable object with proper typing"""
        self.collidables.append(new_collidable)

    def check_collidables(self) -> None:
        """Check and handle collisions with cooldown"""
        current_time = pygame.time.get_ticks() / 1000.0
        if current_time - self.last_collision_time < self.collision_cooldown:
            return

        for collidable in self.collidables:
            if collidable.collision_check(self):
                collidable.collision_action(self)
                self.last_collision_time = current_time
                self.handle_collision(collidable)
                break

    def handle_collision(self, collidable: 'libs.Collidable') -> None:
        """Handle physics-based collision response"""
        # Simple elastic collision response
        normal = (self.position - collidable.position).normalize()
        relative_velocity = self.velocity
        impulse = 2 * relative_velocity.dot(normal) / (self.mass + collidable.mass)
        
        self.velocity -= impulse * normal * self.config.bounce_factor
        self.state = BallState.BOUNCING

    def get_kinetic_energy(self) -> float:
        """Calculate current kinetic energy"""
        speed = self.velocity.length() * self.speed_multiplier
        return 0.5 * self.mass * speed * speed

    def set_position(self, x: float, y: float) -> None:
        """Set position directly"""
        self.position = Vector2(x, y)
