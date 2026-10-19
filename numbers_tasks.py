"""Генерация простых чисел и фильтрация числовых последовательностей."""

from collections.abc import Iterable, Iterator
from math import isqrt


def prime_numbers(limit: int | None = None) -> Iterator[int]:
    """Выдаёт простые числа до limit включительно или без верхней границы."""
    if limit is not None:
        if type(limit) is not int:
            raise TypeError("Верхняя граница должна быть целым числом")
        if limit < 0:
            raise ValueError("Верхняя граница не должна быть отрицательной")

    number = 2
    while limit is None or number <= limit:
        if all(number % divisor != 0 for divisor in range(2, isqrt(number) + 1)):
            yield number
        number += 1


def filter_even_numbers(numbers: Iterable[int]) -> list[int]:
    """Возвращает чётные числа в исходном порядке через filter."""
    return list(filter(lambda number: number % 2 == 0, numbers))
