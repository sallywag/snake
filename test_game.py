import unittest

import pygame

import game


class TestUpdateSnakeDirection(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.game = game.Game()

    def test_child_segment_direction_is_set_to_head_segment_direction(self):
        self.game.snake.append(game.Segment(pygame.Rect((0, 0), (0, 0))))
        self.game.snake[0].direction = game.UP
        self.game.update_snake_direction(game.DOWN)
        self.assertEqual(self.game.snake[1].direction, game.UP)

    def test_head_segment_direction_is_set_to_passed_argument(self):
        self.game.update_snake_direction(game.LEFT)
        self.assertEqual(self.game.snake[0].direction, game.LEFT)


class TestMoveSegment(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.game = game.Game()

    def setUp(self):
        self.previous_location = self.game.snake[0].rect.topleft

    def test_head_segment_moves_up_expected_distance(self):
        self.game.snake[0].direction = game.UP
        self.game.move_segment(self.game.snake[0])
        self.assertEqual(
            self.game.snake[0].rect.y, self.previous_location[1] - game.CELL_SIZE[1]
        )
        self.assertEqual(self.game.snake[0].rect.x, self.previous_location[0])

    def test_head_segment_moves_down_expected_distance(self):
        self.game.snake[0].direction = game.DOWN
        self.game.move_segment(self.game.snake[0])
        self.assertEqual(
            self.game.snake[0].rect.y, self.previous_location[1] + game.CELL_SIZE[1]
        )
        self.assertEqual(self.game.snake[0].rect.x, self.previous_location[0])

    def test_head_segment_moves_left_expected_distance(self):
        self.game.snake[0].direction = game.LEFT
        self.game.move_segment(self.game.snake[0])
        self.assertEqual(
            self.game.snake[0].rect.x, self.previous_location[0] - game.CELL_SIZE[0]
        )
        self.assertEqual(self.game.snake[0].rect.y, self.previous_location[1])

    def test_head_segment_moves_right_expected_distance(self):
        self.game.snake[0].direction = game.RIGHT
        self.game.move_segment(self.game.snake[0])
        self.assertEqual(
            self.game.snake[0].rect.x, self.previous_location[0] + game.CELL_SIZE[0]
        )
        self.assertEqual(self.game.snake[0].rect.y, self.previous_location[1])


class TestHeadSegmentCollidedWithExtender(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.game = game.Game()
        cls.game.snake[0].rect.topleft = (32, 32)
        cls.game.extender = pygame.Rect((0, 0), game.CELL_SIZE)

    def test_returns_false_when_extender_is_not_colliding_with_head_segment(self):
        self.game.extender.topleft = (0, 0)
        self.assertFalse(self.game.head_segment_collided_with_extender())

    def test_returns_true_when_extender_is_colliding_with_head_segment(self):
        self.game.extender.topleft = (32, 32)
        self.assertTrue(self.game.head_segment_collided_with_extender())


class TestHeadSegmentCollidedWithSelf(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.game = game.Game()
        cls.game.snake[0].rect.topleft = (0, 0)

    def test_returns_false_when_head_segment_has_no_child_segments(self):
        self.assertFalse(self.game.head_segment_collided_with_self())

    def test_returns_false_when_head_segment_has_a_child_segment_at_another_location(
        self,
    ):
        self.game.snake.append(game.Segment(pygame.Rect((32, 0), game.CELL_SIZE)))
        self.assertFalse(self.game.head_segment_collided_with_self())

    def test_returns_true_when_head_segment_has_a_child_segment_at_the_same_location(
        self,
    ):
        self.game.snake.append(game.Segment(pygame.Rect((0, 0), game.CELL_SIZE)))
        self.assertTrue(self.game.head_segment_collided_with_self())


class TestHeadSegmentOutOfBounds(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.game = game.Game()

    def test_returns_false_when_head_segment_is_in_bounds(self):
        self.game.snake[0].rect.topleft = (32, 32)
        self.assertFalse(self.game.head_segment_out_of_bounds())

    def test_returns_false_when_head_segments_top_is_at_top_boundary(self):
        self.game.snake[0].rect.topleft = (32, 0)
        self.assertFalse(self.game.head_segment_out_of_bounds())

    def test_returns_true_when_head_segment_is_past_top_boundary(self):
        self.game.snake[0].rect.topleft = (0, -32)
        self.assertTrue(self.game.head_segment_out_of_bounds())

    def test_returns_false_when_head_segments_left_is_at_left_boundary(self):
        self.game.snake[0].rect.topleft = (0, 32)
        self.assertFalse(self.game.head_segment_out_of_bounds())

    def test_returns_true_when_head_segment_is_past_left_boundary(self):
        self.game.snake[0].rect.topleft = (-32, 32)
        self.assertTrue(self.game.head_segment_out_of_bounds())

    def test_return_true_when_head_segments_top_is_at_bottom_boundary(self):
        self.game.snake[0].rect.topleft = (32, game.WINDOW_SIZE[1])
        self.assertTrue(self.game.head_segment_out_of_bounds())

    def test_returns_true_when_head_segment_is_past_bottom_boundary(self):
        self.game.snake[0].rect.topleft = (32, game.WINDOW_SIZE[1] + 32)
        self.assertTrue(self.game.head_segment_out_of_bounds())

    def test_returns_true_when_head_segments_left_is_at_right_boundary(self):
        self.game.snake[0].rect.topleft = (game.WINDOW_SIZE[0], 32)
        self.assertTrue(self.game.head_segment_out_of_bounds())

    def test_returns_true_when_head_segment_is_past_right_boundary(self):
        self.game.snake[0].rect.topleft = (game.WINDOW_SIZE[0] + 32, 32)
        self.assertTrue(self.game.head_segment_out_of_bounds())


class TestGameOver(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.game = game.Game()
        cls.game.snake.append(game.Segment(pygame.Rect((0, 0), game.CELL_SIZE)))

    def setUp(self):
        self.game.snake[0].rect.topleft = (0, 0)
        self.game.snake[1].rect.topleft = (32, 0)

    def test_returns_false_when_head_segment_did_not_go_out_of_bounds_or_collide_with_self(
        self,
    ):
        self.assertFalse(self.game.game_over())

    def test_returns_true_when_only_head_segment_out_of_bounds(self):
        self.game.snake[0].rect.topleft = (-32, -32)
        self.assertTrue(self.game.game_over())

    def test_returns_true_when_only_head_segment_collided_with_self(self):
        self.game.snake[1].rect.topleft = (0, 0)
        self.assertTrue(self.game.game_over())

    def test_returns_true_when_head_segment_out_of_bounds_and_collided_with_self(self):
        self.game.snake[0].rect.topleft = (-32, -32)
        self.game.snake[1].rect.topleft = (-32, -32)
        self.assertTrue(self.game.game_over())


class TestAddSegmentToSnake(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.game = game.Game()

    def setUp(self):
        self.game.snake = [game.Segment(pygame.Rect((32, 32), game.CELL_SIZE))]

    def test_segment_is_added_to_snake_if_head_segment_direction_is_up(self):
        self.game.snake[0].direction = game.UP
        self.game.add_segment_to_snake()
        self.assertIsInstance(self.game.snake[1], game.Segment)

    def test_segment_is_added_to_snake_if_head_segment_direction_is_down(self):
        self.game.snake[0].direction = game.DOWN
        self.game.add_segment_to_snake()
        self.assertIsInstance(self.game.snake[1], game.Segment)

    def test_segment_is_added_to_snake_if_head_segment_direction_is_left(self):
        self.game.snake[0].direction = game.LEFT
        self.game.add_segment_to_snake()
        self.assertIsInstance(self.game.snake[1], game.Segment)

    def test_segment_is_added_to_snake_if_head_segment_direction_is_right(self):
        self.game.snake[0].direction = game.RIGHT
        self.game.add_segment_to_snake()
        self.assertIsInstance(self.game.snake[1], game.Segment)

    def test_added_segment_is_above_head_segment(self):
        self.game.snake[0].direction = game.DOWN
        self.game.add_segment_to_snake()
        self.assertLess(self.game.snake[1].rect.y, self.game.snake[0].rect.y)

    def test_added_segment_is_below_head_segment(self):
        self.game.snake[0].direction = game.UP
        self.game.add_segment_to_snake()
        self.assertGreater(self.game.snake[1].rect.y, self.game.snake[0].rect.y)

    def test_added_segment_is_to_the_left_of_head_segment(self):
        self.game.snake[0].direction = game.RIGHT
        self.game.add_segment_to_snake()
        self.assertLess(self.game.snake[1].rect.x, self.game.snake[0].rect.x)

    def test_added_segment_is_to_the_right_of_head_segment(self):
        self.game.snake[0].direction = game.LEFT
        self.game.add_segment_to_snake()
        self.assertGreater(self.game.snake[1].rect.x, self.game.snake[0].rect.x)

    def test_added_segment_above_head_segment_is_in_the_correct_location(self):
        self.game.snake[0].direction = game.DOWN
        self.game.add_segment_to_snake()
        self.assertEqual(
            self.game.snake[1].rect.y, self.game.snake[0].rect.y - game.CELL_SIZE[1]
        )
        self.assertEqual(self.game.snake[1].rect.x, self.game.snake[0].rect.x)

    def test_added_segment_below_head_segment_is_in_the_correct_location(self):
        self.game.snake[0].direction = game.UP
        self.game.add_segment_to_snake()
        self.assertEqual(
            self.game.snake[1].rect.y, self.game.snake[0].rect.y + game.CELL_SIZE[1]
        )
        self.assertEqual(self.game.snake[1].rect.x, self.game.snake[0].rect.x)

    def test_added_segment_to_the_left_of_head_segment_is_in_the_correct_location(self):
        self.game.snake[0].direction = game.RIGHT
        self.game.add_segment_to_snake()
        self.assertEqual(
            self.game.snake[1].rect.x, self.game.snake[0].rect.x - game.CELL_SIZE[0]
        )
        self.assertEqual(self.game.snake[1].rect.y, self.game.snake[0].rect.y)

    def test_added_segment_to_the_right_of_head_segment_is_in_the_correct_location(
        self,
    ):
        self.game.snake[0].direction = game.LEFT
        self.game.add_segment_to_snake()
        self.assertEqual(
            self.game.snake[1].rect.x, self.game.snake[0].rect.x + game.CELL_SIZE[0]
        )
        self.assertEqual(self.game.snake[1].rect.y, self.game.snake[0].rect.y)

    def test_added_segment_above_head_segment_is_the_correct_direction(self):
        self.game.snake[0].direction = game.DOWN
        self.game.add_segment_to_snake()
        self.assertEqual(self.game.snake[1].direction, self.game.snake[0].direction)

    def test_added_segment_below_head_segment_is_the_correct_direction(self):
        self.game.snake[0].direction = game.UP
        self.game.add_segment_to_snake()
        self.assertEqual(self.game.snake[1].direction, self.game.snake[0].direction)

    def test_added_segment_to_the_left_of_head_segment_is_the_correct_direction(self):
        self.game.snake[0].direction = game.RIGHT
        self.game.add_segment_to_snake()
        self.assertEqual(self.game.snake[1].direction, self.game.snake[0].direction)

    def test_added_segment_to_the_right_of_head_segment_is_the_correct_direction(self):
        self.game.snake[0].direction = game.LEFT
        self.game.add_segment_to_snake()
        self.assertEqual(self.game.snake[1].direction, self.game.snake[0].direction)

    def test_segment_is_added_to_the_tail_of_the_tail_of_head_segment(self):
        self.game.snake[0].direction = game.UP
        self.game.add_segment_to_snake()
        self.game.add_segment_to_snake()
        self.assertIsInstance(self.game.snake[2], game.Segment)

    def test_added_segment_is_the_same_size_as_head_segment(self):
        self.game.snake[0].direction = game.UP
        self.game.add_segment_to_snake()
        self.assertEqual(self.game.snake[1].rect.size, self.game.snake[0].rect.size)
