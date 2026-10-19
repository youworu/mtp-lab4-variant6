"""Проверки генератора простых чисел и фильтрации чётных чисел."""

import unittest
from itertools import islice
from types import GeneratorType

from numbers_tasks import filter_even_numbers, prime_numbers


class PrimeNumbersTests(unittest.TestCase):
    """Границы диапазона, ленивое получение чисел и неверный ввод."""

    def test_returns_a_generator(self):
        self.assertIsInstance(prime_numbers(10), GeneratorType)

    def test_primes_up_to_thirty(self):
        self.assertEqual(
            list(prime_numbers(30)), [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
        )

    def test_prime_limit_is_included(self):
        self.assertEqual(list(prime_numbers(7)), [2, 3, 5, 7])
        self.assertEqual(list(prime_numbers(2)), [2])

    def test_limits_below_two_produce_no_values(self):
        for limit in (0, 1):
            with self.subTest(limit=limit):
                self.assertEqual(list(prime_numbers(limit)), [])

    def test_squares_are_not_prime(self):
        primes = list(prime_numbers(49))

        for square in (4, 9, 25, 49):
            with self.subTest(square=square):
                self.assertNotIn(square, primes)

    def test_unbounded_generator_can_be_consumed_in_parts(self):
        primes = prime_numbers()

        self.assertEqual(list(islice(primes, 5)), [2, 3, 5, 7, 11])
        self.assertEqual(list(islice(primes, 3)), [13, 17, 19])
        primes.close()

    def test_negative_limit_is_rejected(self):
        with self.assertRaises(ValueError):
            list(prime_numbers(-1))

    def test_limit_must_be_an_integer(self):
        for limit in (2.5, "10", True):
            with self.subTest(limit=limit):
                with self.assertRaises(TypeError):
                    list(prime_numbers(limit))


class EvenNumbersTests(unittest.TestCase):
    """Сохранение порядка, повторов и исходного списка."""

    def test_filters_even_numbers(self):
        self.assertEqual(filter_even_numbers([1, 2, 3, 4, 5, 6]), [2, 4, 6])

    def test_preserves_negative_numbers_zero_and_duplicates(self):
        self.assertEqual(filter_even_numbers([-4, -3, 0, 2, 2]), [-4, 0, 2, 2])

    def test_empty_input_and_odd_numbers(self):
        self.assertEqual(filter_even_numbers([]), [])
        self.assertEqual(filter_even_numbers([1, 3, 5]), [])

    def test_does_not_change_the_original_list(self):
        numbers = [1, 2, 3, 4]

        filter_even_numbers(numbers)

        self.assertEqual(numbers, [1, 2, 3, 4])

    def test_accepts_a_generator(self):
        self.assertEqual(filter_even_numbers(number for number in range(6)), [0, 2, 4])


if __name__ == "__main__":
    unittest.main()
