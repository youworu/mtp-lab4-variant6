"""Проверки генератора простых чисел."""

import unittest
from itertools import islice
from types import GeneratorType

from numbers_tasks import prime_numbers


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


if __name__ == "__main__":
    unittest.main()
