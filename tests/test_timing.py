"""Проверки декоратора без ожиданий и зависимости от скорости компьютера."""

import unittest
from unittest.mock import patch

from timing import time_execution


class TimingTests(unittest.TestCase):
    """Результат, аргументы, метаданные и исключения исходной функции."""

    def test_returns_the_original_object(self):
        expected = [1, 2, 3]

        @time_execution
        def get_numbers():
            return expected

        self.assertIs(get_numbers(), expected)

    def test_passes_positional_and_keyword_arguments(self):
        @time_execution
        def add(first, second, *, multiplier=1):
            return (first + second) * multiplier

        self.assertEqual(add(2, 3, multiplier=4), 20)

    def test_preserves_function_metadata(self):
        def original(number):
            """Описание функции для проверки wraps."""
            return number

        decorated = time_execution(original)

        self.assertEqual(decorated.__name__, "original")
        self.assertEqual(decorated.__doc__, original.__doc__)
        self.assertIs(decorated.__wrapped__, original)

    def test_logs_elapsed_time(self):
        @time_execution
        def calculate():
            return 42

        with patch("timing.perf_counter", side_effect=[10.0, 10.25]):
            with self.assertLogs("timing", level="INFO") as captured:
                result = calculate()

        self.assertEqual(result, 42)
        self.assertIn("calculate: 0.250000 с", captured.output[0])

    def test_logs_time_and_propagates_the_same_exception(self):
        expected = ValueError("Неверный аргумент")

        @time_execution
        def fail():
            raise expected

        with patch("timing.perf_counter", side_effect=[20.0, 20.5]):
            with self.assertLogs("timing", level="INFO") as captured:
                with self.assertRaises(ValueError) as error:
                    fail()

        self.assertIs(error.exception, expected)
        self.assertIn("fail: 0.500000 с", captured.output[0])


if __name__ == "__main__":
    unittest.main()
