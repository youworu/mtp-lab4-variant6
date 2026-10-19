"""Проверки собственной свёртки и сравнение со стандартной функцией."""

import operator
import unittest
from functools import reduce
from unittest.mock import Mock

from reducing import custom_reduce


class ReduceTests(unittest.TestCase):
    """Порядок вычислений, начальное значение и однократное чтение данных."""

    def test_sum(self):
        self.assertEqual(custom_reduce(operator.add, [1, 2, 3, 4]), 10)

    def test_product(self):
        self.assertEqual(custom_reduce(operator.mul, [1, 2, 3, 4]), 24)

    def test_applies_initial_value_once(self):
        self.assertEqual(custom_reduce(operator.add, [1, 2, 3], 10), 16)

    def test_empty_iterable_returns_initial_value(self):
        initial = []

        self.assertIs(custom_reduce(operator.add, [], initial), initial)
        self.assertEqual(custom_reduce(operator.add, [], 0), 0)

    def test_empty_iterable_without_initial_raises_type_error(self):
        with self.assertRaises(TypeError):
            custom_reduce(operator.add, [])

    def test_single_item_does_not_call_the_function(self):
        combine = Mock()

        self.assertEqual(custom_reduce(combine, [42]), 42)
        combine.assert_not_called()

    def test_none_is_an_explicit_initial_value(self):
        self.assertIsNone(custom_reduce(operator.add, [], None))
        self.assertEqual(
            custom_reduce(lambda result, item: f"{result}:{item}", ["a"], None),
            "None:a",
        )

    def test_reduces_from_left_to_right(self):
        self.assertEqual(custom_reduce(operator.sub, [10, 3, 2]), 5)

    def test_accepts_a_single_pass_generator(self):
        numbers = (number for number in range(1, 5))

        self.assertEqual(custom_reduce(operator.add, numbers), 10)
        self.assertEqual(list(numbers), [])

    def test_can_build_a_string_from_numbers(self):
        self.assertEqual(
            custom_reduce(lambda result, number: result + str(number), [1, 2, 3], ""),
            "123",
        )

    def test_float_sum(self):
        self.assertAlmostEqual(custom_reduce(operator.add, [0.1, 0.2, 0.3]), 0.6)

    def test_propagates_the_original_callback_exception(self):
        expected = ValueError("Ошибка вычисления")

        def fail(first, second):
            raise expected

        with self.assertRaises(ValueError) as error:
            custom_reduce(fail, [1, 2])

        self.assertIs(error.exception, expected)

    def test_matches_standard_reduce(self):
        cases = (
            (operator.add, [1, 2, 3], 0),
            (operator.mul, [2, 3, 4], 1),
            (operator.sub, [10, 3, 2], 100),
            (operator.add, ["a", "b", "c"], ""),
            (operator.add, [], 10),
        )
        for function, values, initial in cases:
            with self.subTest(
                function=function.__name__, values=values, initial=initial
            ):
                self.assertEqual(
                    custom_reduce(function, values, initial),
                    reduce(function, values, initial),
                )


if __name__ == "__main__":
    unittest.main()
