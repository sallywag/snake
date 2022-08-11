"""Recreation of the game Snake."""

import sys
import random
import itertools
from dataclasses import dataclass

import pygame

FPS = 10
WINDOW_SIZE = (640, 480)
CELL_SIZE = (32, 32)
START_LOCATION = (320, 224)
UP = "up"
DOWN = "down"
LEFT = "left"
RIGHT = "right"
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)


@dataclass
class Segment:
    """Simple class for storing information about a segment."""

    rect: pygame.Rect
    direction: str = None


class Game:
    """Contains all game logic."""

    def __init__(self):
        self.direction = None
        self.extender = None
        self.cell_locations = self.cell_locations = set(
            itertools.product(
                range(0, WINDOW_SIZE[0], CELL_SIZE[0]),
                range(0, WINDOW_SIZE[1], CELL_SIZE[1]),
            )
        )
        self.snake = [Segment(pygame.Rect(START_LOCATION, CELL_SIZE))]
        pygame.init()
        self.fps_clock = pygame.time.Clock()
        self.displaysurf = pygame.display.set_mode(WINDOW_SIZE)
        pygame.display.set_caption("Snake")

    def main(self) -> None:
        """Entry point for the game."""
        while True:
            self.update()
            self.render()
            self.fps_clock.tick(FPS)

    def update(self) -> None:
        """Update the game state here."""
        self.handle_input()
        self.update_snake_direction(self.direction)
        self.move_snake()

        if self.extender is None:
            snake_segments_locations = set(
                segment.rect.topleft for segment in self.snake
            )
            location = random.choice(
                list(self.cell_locations - snake_segments_locations)
            )
            self.extender = pygame.Rect(location, CELL_SIZE)

        if self.head_segment_collided_with_extender():
            self.extender = None
            self.add_segment_to_snake()

        if self.game_over():
            self.snake = [Segment(pygame.Rect(START_LOCATION, CELL_SIZE))]
            self.direction = None
            self.extender = None

    def handle_input(self) -> None:
        """Update the snakes direction based off keyboard input."""
        if self.input_manager.quit:
            pygame.quit()
            sys.exit()

        if self.input_manager.pressed(pygame.K_UP) and self.direction != DOWN:
            self.direction = UP
        elif self.input_manager.pressed(pygame.K_DOWN) and self.direction != UP:
            self.direction = DOWN
        elif self.input_manager.pressed(pygame.K_LEFT) and self.direction != RIGHT:
            self.direction = LEFT
        elif self.input_manager.pressed(pygame.K_RIGHT) and self.direction != LEFT:
            self.direction = RIGHT

    def update_snake_direction(self, head_direction: str) -> None:
        """Update the direction of each segment of the snake."""
        for index in reversed(range(len(self.snake))):
            self.snake[index].direction = self.snake[index - 1].direction
        self.snake[0].direction = head_direction

    def move_snake(self) -> None:
        """Update the position of every segment of the snake."""
        for segment in self.snake:
            self.move_segment(segment)

    def move_segment(self, segment: Segment) -> None:
        """Update the position of a single segment of the snake."""
        move_amount = {
            UP: (0, -CELL_SIZE[1]),
            DOWN: (0, CELL_SIZE[1]),
            LEFT: (-CELL_SIZE[0], 0),
            RIGHT: (CELL_SIZE[0], 0),
        }.get(segment.direction, (0, 0))
        segment.rect.move_ip(move_amount)

    def head_segment_collided_with_extender(self) -> bool:
        """Return whether the snakes head collided with an extending segment."""
        return self.snake[0].rect.colliderect(self.extender)

    def add_segment_to_snake(self) -> None:
        """Add a segment to the back of the snakes body."""
        topleft = {
            UP: (self.snake[-1].rect.x, self.snake[-1].rect.y + CELL_SIZE[1]),
            DOWN: (self.snake[-1].rect.x, self.snake[-1].rect.y - CELL_SIZE[1]),
            LEFT: (self.snake[-1].rect.x + CELL_SIZE[0], self.snake[-1].rect.y),
            RIGHT: (self.snake[-1].rect.x - CELL_SIZE[0], self.snake[-1].rect.y),
        }.get(self.snake[-1].direction, (0, 0))
        self.snake.append(
            Segment(pygame.Rect(topleft, CELL_SIZE), self.snake[-1].direction)
        )

    def game_over(self) -> bool:
        """Return whether the head of the snake collided
        with its body or the edge of the screen.
        """
        return (
            self.head_segment_collided_with_self() or self.head_segment_out_of_bounds()
        )

    def head_segment_collided_with_self(self) -> bool:
        """Return whether the head of the snake collided with its body."""
        return any(
            [self.snake[0].rect.colliderect(segment) for segment in self.snake[1:]]
        )

    def head_segment_out_of_bounds(self) -> bool:
        """Return whether the head of the snake collided with the edge of the screen."""
        return (
            self.snake[0].rect.x < 0
            or self.snake[0].rect.y < 0
            or self.snake[0].rect.x >= WINDOW_SIZE[0]
            or self.snake[0].rect.y >= WINDOW_SIZE[1]
        )

    def render(self) -> None:
        """Draw everything to screen."""
        self.displaysurf.fill(BLACK)
        for segment in self.snake:
            pygame.draw.rect(self.displaysurf, GREEN, segment.rect)
        if self.extender is not None:
            pygame.draw.rect(self.displaysurf, RED, self.extender)
        pygame.display.update()


if __name__ == "__main__":
    Game().main()
